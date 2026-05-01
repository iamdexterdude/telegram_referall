"""
bot/handlers/start.py — /start, language selection, captcha, registration, channel gate.
"""
from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Contact, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.keyboards import (
    join_verify_keyboard,
    language_keyboard,
    main_menu_keyboard,
    remove_keyboard,
    request_contact_keyboard,
)
from bot.locales.translations import t
from bot.services.referral_service import (
    confirm_referral,
    is_member_of_channel,
    referral_already_exists,
)
from bot.services.user_service import (
    create_user,
    get_user,
    get_user_by_code,
    update_language,
)
from bot.utils.helpers import build_referral_link, generate_captcha
from bot.utils.states import Captcha, ChannelVerification, LangSelect, Registration
from config import config

logger = logging.getLogger(__name__)
router = Router(name="start")


# ─────────────────────────────────────────────────────────────────────────────
#  /start
# ─────────────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    user_id = message.from_user.id
    args = message.text.split(maxsplit=1)[1].strip() if len(message.text.split()) > 1 else ""

    existing = await get_user(session, user_id)
    if existing:
        await message.answer(
            t(existing.language, "welcome_back", name=existing.first_name),
            reply_markup=main_menu_keyboard(existing.language),
            parse_mode="HTML",
        )
        return

    # New user — store referral code, go to language selection
    await state.update_data(referral_code=args or None, is_new_registration=True)
    await state.set_state(LangSelect.choosing)
    await message.answer(
        t("en", "choose_language"),
        reply_markup=language_keyboard(),
        parse_mode="HTML",
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Language change from main menu button
# ─────────────────────────────────────────────────────────────────────────────

@router.message(F.text.in_(["🌐 Til", "🌐 Язык", "🌐 Language"]))
async def change_language_menu(message: Message, state: FSMContext, session: AsyncSession) -> None:
    user = await get_user(session, message.from_user.id)
    if not user:
        await message.answer(t("en", "not_registered"), parse_mode="HTML")
        return
    # Use a separate state flag so we know this is NOT a new registration
    await state.clear()
    await state.update_data(is_new_registration=False)
    await state.set_state(LangSelect.choosing)
    await message.answer(t("en", "choose_language"), reply_markup=language_keyboard())


# ─────────────────────────────────────────────────────────────────────────────
#  Language callback — handles BOTH new registration and existing user change
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(LangSelect.choosing, F.data.startswith("lang:"))
async def cb_language_chosen(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    lang = callback.data.split(":")[1]
    data = await state.get_data()
    is_new = data.get("is_new_registration", True)

    await callback.message.edit_reply_markup(reply_markup=None)

    if not is_new:
        # ── Existing user just changing language ──────────────────────────
        await update_language(session, callback.from_user.id, lang)
        await state.clear()
        user = await get_user(session, callback.from_user.id)
        await callback.message.answer(
            t(lang, "welcome_back", name=user.first_name),
            reply_markup=main_menu_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer("✅")
        return

    # ── New user — proceed to captcha ─────────────────────────────────────
    await state.update_data(language=lang)
    a, b, answer = generate_captcha()
    await state.update_data(captcha_answer=answer, captcha_a=a, captcha_b=b)
    await state.set_state(Captcha.solving)
    await callback.message.answer(
        t(lang, "captcha_question", a=a, b=b),
        reply_markup=remove_keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
#  Captcha
# ─────────────────────────────────────────────────────────────────────────────

@router.message(Captcha.solving, F.text)
async def solve_captcha(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")

    if not message.text.strip().isdigit():
        await message.answer(t(lang, "captcha_not_number"), parse_mode="HTML")
        return

    if int(message.text.strip()) != data["captcha_answer"]:
        a2, b2, ans2 = generate_captcha()
        await state.update_data(captcha_answer=ans2, captcha_a=a2, captcha_b=b2)
        await message.answer(t(lang, "captcha_wrong", a=a2, b=b2), parse_mode="HTML")
        return

    await state.set_state(Registration.waiting_for_first_name)
    await message.answer(t(lang, "ask_first_name"), parse_mode="HTML")


# ─────────────────────────────────────────────────────────────────────────────
#  Registration FSM
# ─────────────────────────────────────────────────────────────────────────────

@router.message(Registration.waiting_for_first_name, F.text)
async def reg_first_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    name = message.text.strip()
    if len(name) < 1 or len(name) > 64:
        await message.answer(t(lang, "name_too_long"), parse_mode="HTML")
        return
    await state.update_data(first_name=name)
    await state.set_state(Registration.waiting_for_last_name)
    await message.answer(t(lang, "ask_last_name"), parse_mode="HTML")


@router.message(Registration.waiting_for_last_name, F.text)
async def reg_last_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    name = message.text.strip()
    if len(name) > 64:
        await message.answer(t(lang, "name_too_long"), parse_mode="HTML")
        return
    await state.update_data(last_name=name)
    await state.set_state(Registration.waiting_for_phone)
    await message.answer(
        t(lang, "ask_phone"),
        reply_markup=request_contact_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(Registration.waiting_for_phone, F.contact)
async def reg_phone(message: Message, state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    contact: Contact = message.contact
    data = await state.get_data()
    lang = data.get("language", "en")

    # Guard: already registered (FSM replay / double-submit)
    already = await get_user(session, message.from_user.id)
    if already:
        await state.clear()
        await message.answer(
            t(already.language, "welcome_back", name=already.first_name),
            reply_markup=main_menu_keyboard(already.language),
            parse_mode="HTML",
        )
        return

    if contact.user_id and contact.user_id != message.from_user.id:
        await message.answer(t(lang, "wrong_phone"), parse_mode="HTML")
        return

    referral_code: str | None = data.get("referral_code")
    referrer = None
    if referral_code:
        referrer = await get_user_by_code(session, referral_code)
        if referrer and referrer.user_id == message.from_user.id:
            referrer = None

    user = await create_user(
        session,
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=data["first_name"],
        last_name=data.get("last_name"),
        phone_number=contact.phone_number,
        referred_by=referrer.user_id if referrer else None,
        language=lang,
    )

    await state.clear()

    if referrer:
        await state.update_data(referrer_id=referrer.user_id, language=lang)
        await state.set_state(ChannelVerification.waiting_for_join)
        await message.answer(
            t(lang, "join_channel", channel=config.channel_id),
            reply_markup=join_verify_keyboard(lang),
            parse_mode="HTML",
        )
    else:
        await _finish_onboarding(message, user, lang)


@router.message(Registration.waiting_for_phone)
async def reg_phone_wrong_type(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    await message.answer(
        t(lang, "wrong_phone"),
        reply_markup=request_contact_keyboard(lang),
        parse_mode="HTML",
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Channel verification
# ─────────────────────────────────────────────────────────────────────────────

@router.message(ChannelVerification.waiting_for_join)
async def verify_channel(message: Message, state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    referrer_id: int | None = data.get("referrer_id")
    user_id = message.from_user.id

    joined = await is_member_of_channel(bot, config.channel_id, user_id)
    if not joined:
        await message.answer(
            t(lang, "not_joined", channel=config.channel_id),
            reply_markup=join_verify_keyboard(lang),
            parse_mode="HTML",
        )
        return

    if referrer_id:
        already = await referral_already_exists(session, user_id)
        if not already:
            referred_name = message.from_user.first_name or "Someone"
            await confirm_referral(
                session, bot,
                referrer_id=referrer_id,
                referred_user_id=user_id,
                referred_name=referred_name,
            )
            await message.answer(t(lang, "joined_confirmed"), parse_mode="HTML")
        else:
            await message.answer(t(lang, "joined_no_ref"), parse_mode="HTML")

    await state.clear()
    user = await get_user(session, user_id)
    await _finish_onboarding(message, user, lang)


# ─────────────────────────────────────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────────────────────────────────────

async def _finish_onboarding(message: Message, user, lang: str) -> None:
    link = build_referral_link(config.bot_username, user.referral_code)
    await message.answer(
        t(lang, "registered", name=user.first_name, link=link),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
