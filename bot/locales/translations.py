"""
bot/locales/translations.py — All UI strings in 3 languages.
Add new keys here; never hardcode text in handlers.
"""

TEXTS = {
    "uz": {
        # Onboarding
        "choose_language":      "🌐 Tilni tanlang / Choose language / Выберите язык:",
        "welcome_new":          "👋 Xush kelibsiz! Keling, ro'yxatdan o'tamiz.\n\n<b>Ismingizni</b> kiriting:",
        "welcome_back":         "👋 Qaytib keldingiz, <b>{name}</b>! Quyidagi menyudan foydalaning.",
        "ask_first_name":       "✏️ <b>Ismingizni</b> kiriting:",
        "ask_last_name":        "✏️ <b>Familiyangizni</b> kiriting:",
        "ask_phone":            "📱 Telefon raqamingizni ulashing:",
        "wrong_phone":          "⚠️ Iltimos, tugma orqali o'z raqamingizni yuboring.",
        "name_too_long":        "⚠️ Ism juda uzun. Qaytadan kiriting:",
        "captcha_question":     "🤖 Siz robot emasligingizni tasdiqlang:\n\n<b>{a} + {b} = ?</b>",
        "captcha_wrong":        "❌ Noto'g'ri javob. Qaytadan urinib ko'ring:\n\n<b>{a} + {b} = ?</b>",
        "captcha_not_number":   "⚠️ Faqat raqam kiriting.",

        # Channel gate
        "join_channel":         "📢 Referalni tasdiqlash uchun kanalga qo'shiling:\n👉 <b>{channel}</b>\n\nQo'shilgach, tugmani bosing:",
        "not_joined":           "❌ Siz hali kanalga qo'shilmadingiz.\n👉 <b>{channel}</b>\n\nQo'shiling va qaytadan tekshiring:",
        "joined_confirmed":     "🎉 Kanal a'zoligi tasdiqlandi! Referal hisobga olindi.",
        "joined_no_ref":        "✅ Kanal a'zoligi tasdiqlandi!",

        # Registration complete
        "registered":           (
            "🎊 Ro'yxatdan o'tdingiz, <b>{name}</b>!\n\n"
            "🔗 Sizning referal havolangiz:\n<code>{link}</code>\n\n"
            "Do'stlaringizga ulashing va har bir qo'shilgan uchun <b>+1 kredit</b> oling!"
        ),

        # Main menu buttons
        "btn_link":             "🔗 Referal havola",
        "btn_stats":            "📊 Mening natijalarim",
        "btn_top":              "🏆 Top referallar",
        "btn_help":             "❓ Yordam",
        "btn_language":         "🌐 Til",

        # Referral link
        "your_link":            "🔗 <b>Sizning referal havolangiz</b>\n\n<code>{link}</code>\n\n👥 Do'stlaringizga yuboring!",
        "qr_caption":           "📱 QR kodni skanerlang yoki havolani ulashing:\n<code>{link}</code>",

        # Stats
        "stats":                (
            "📊 <b>Sizning natijalaringiz</b>\n\n"
            "👤 Ism: <b>{full_name}</b>\n"
            "🆔 Username: <b>{username}</b>\n"
            "💎 Kredit (referal): <b>{count}</b>\n"
            "🏅 Nishon: <b>{badge}</b>\n"
            "📈 Reyting: <b>#{rank}</b>\n"
            "📅 A'zo bo'lgan sana: <b>{date}</b>\n\n"
            "{milestone_text}"
            "🔗 Havolangiz:\n<code>{link}</code>"
        ),
        "milestone_next":       "🎯 Keyingi nishon: yana <b>{needed}</b> referal → {emoji} {name}\n\n",
        "milestone_max":        "🏆 Siz maksimal darajaga yetdingiz!\n\n",

        # Leaderboard
        "top_title":            "🏆 <b>Top Referallar</b>\n",
        "top_empty":            "📭 Hali referal yo'q. Birinchi bo'ling!",
        "top_row":              "{pos} {display} — <b>{count}</b> {badge}",

        # Notifications
        "notif_new_referral":   "🎉 Yangi referal! <b>{name}</b> sizning havolangiz orqali qo'shildi.\n💎 Jami: <b>{total}</b> referal {badge}",
        "milestone_reached":    "🎊 Tabriklaymiz! Siz <b>{emoji} {name}</b> nishoniga erishdingiz!",

        # Help
        "help":                 (
            "❓ <b>Yordam</b>\n\n"
            "🔗 /start — Botni ishga tushirish\n"
            "📊 /stats — Natijalaringizni ko'rish\n"
            "🏆 /top — Top referallar ro'yxati\n"
            "🌐 /language — Tilni o'zgartirish\n\n"
            "📢 Referal tizimi:\n"
            "1. Havolangizni oling\n"
            "2. Do'stlaringizga yuboring\n"
            "3. Ular kanalga qo'shilganda +1 kredit olasiz\n\n"
            "🏅 Nishonlar:\n"
            "🥉 5 referal → Bronze\n"
            "🥈 15 referal → Silver\n"
            "🥇 30 referal → Gold\n"
            "💎 50 referal → Diamond"
        ),

        # Admin
        "not_admin":            "⛔ Sizda admin huquqlari yo'q.",
        "broadcast_usage":      "📢 Foydalanish: /broadcast &lt;xabar matni&gt;",
        "broadcast_done":       "✅ Xabar {count} foydalanuvchiga yuborildi.",
        "ban_usage":            "🔨 Foydalanish: /ban &lt;user_id&gt;",
        "ban_done":             "✅ Foydalanuvchi {user_id} bloklandi.",
        "unban_done":           "✅ Foydalanuvchi {user_id} blokdan chiqarildi.",
        "admin_panel":          (
            "🔧 <b>Admin Panel</b>\n\n"
            "👥 Jami foydalanuvchilar: <b>{users}</b>\n"
            "🔗 Jami referallar: <b>{referrals}</b>\n"
            "📅 Bugungi yangi foydalanuvchilar: <b>{today_users}</b>\n"
            "📅 Bugungi referallar: <b>{today_refs}</b>\n\n"
            "Buyruqlar:\n"
            "/broadcast &lt;matn&gt; — Hammaga xabar yuborish\n"
            "/ban &lt;user_id&gt; — Foydalanuvchini bloklash\n"
            "/unban &lt;user_id&gt; — Blokni olib tashlash\n"
            "/export_users — CSV yuklab olish\n"
            "/export_referrals — CSV yuklab olish"
        ),

        # Misc
        "not_registered":       "⚠️ Siz ro'yxatdan o'tmagansiz. /start buyrug'ini yuboring.",
        "banned":               "⛔ Siz botdan bloklangansiz.",
        "verify_btn":           "✅ Qo'shildim — Tekshirish",
        "share_phone_btn":      "📱 Telefon raqamni ulashish",
    },

    "ru": {
        "choose_language":      "🌐 Tilni tanlang / Choose language / Выберите язык:",
        "welcome_new":          "👋 Добро пожаловать! Давайте зарегистрируемся.\n\n<b>Введите ваше имя:</b>",
        "welcome_back":         "👋 С возвращением, <b>{name}</b>! Используйте меню ниже.",
        "ask_first_name":       "✏️ Введите ваше <b>имя</b>:",
        "ask_last_name":        "✏️ Введите вашу <b>фамилию</b>:",
        "ask_phone":            "📱 Поделитесь номером телефона:",
        "wrong_phone":          "⚠️ Пожалуйста, используйте кнопку для отправки номера.",
        "name_too_long":        "⚠️ Имя слишком длинное. Попробуйте снова:",
        "captcha_question":     "🤖 Подтвердите, что вы не робот:\n\n<b>{a} + {b} = ?</b>",
        "captcha_wrong":        "❌ Неверный ответ. Попробуйте снова:\n\n<b>{a} + {b} = ?</b>",
        "captcha_not_number":   "⚠️ Введите только число.",
        "join_channel":         "📢 Для подтверждения реферала вступите в канал:\n👉 <b>{channel}</b>\n\nПосле вступления нажмите кнопку:",
        "not_joined":           "❌ Вы ещё не вступили в канал.\n👉 <b>{channel}</b>\n\nВступите и проверьте снова:",
        "joined_confirmed":     "🎉 Членство подтверждено! Реферал засчитан.",
        "joined_no_ref":        "✅ Членство в канале подтверждено!",
        "registered":           (
            "🎊 Регистрация завершена, <b>{name}</b>!\n\n"
            "🔗 Ваша реферальная ссылка:\n<code>{link}</code>\n\n"
            "Поделитесь с друзьями и получайте <b>+1 кредит</b> за каждого!"
        ),
        "btn_link":             "🔗 Реф. ссылка",
        "btn_stats":            "📊 Моя статистика",
        "btn_top":              "🏆 Топ рефералов",
        "btn_help":             "❓ Помощь",
        "btn_language":         "🌐 Язык",
        "your_link":            "🔗 <b>Ваша реферальная ссылка</b>\n\n<code>{link}</code>\n\n👥 Отправьте друзьям!",
        "qr_caption":           "📱 Отсканируйте QR или поделитесь ссылкой:\n<code>{link}</code>",
        "stats":                (
            "📊 <b>Ваша статистика</b>\n\n"
            "👤 Имя: <b>{full_name}</b>\n"
            "🆔 Username: <b>{username}</b>\n"
            "💎 Кредиты (рефералы): <b>{count}</b>\n"
            "🏅 Значок: <b>{badge}</b>\n"
            "📈 Рейтинг: <b>#{rank}</b>\n"
            "📅 Дата регистрации: <b>{date}</b>\n\n"
            "{milestone_text}"
            "🔗 Ваша ссылка:\n<code>{link}</code>"
        ),
        "milestone_next":       "🎯 Следующий значок: ещё <b>{needed}</b> рефералов → {emoji} {name}\n\n",
        "milestone_max":        "🏆 Вы достигли максимального уровня!\n\n",
        "top_title":            "🏆 <b>Топ Рефералов</b>\n",
        "top_empty":            "📭 Рефералов пока нет. Будьте первым!",
        "top_row":              "{pos} {display} — <b>{count}</b> {badge}",
        "notif_new_referral":   "🎉 Новый реферал! <b>{name}</b> присоединился по вашей ссылке.\n💎 Всего: <b>{total}</b> рефералов {badge}",
        "milestone_reached":    "🎊 Поздравляем! Вы достигли значка <b>{emoji} {name}</b>!",
        "help":                 (
            "❓ <b>Помощь</b>\n\n"
            "🔗 /start — Запустить бота\n"
            "📊 /stats — Ваша статистика\n"
            "🏆 /top — Топ рефералов\n"
            "🌐 /language — Сменить язык\n\n"
            "📢 Реферальная система:\n"
            "1. Получите свою ссылку\n"
            "2. Отправьте друзьям\n"
            "3. Когда они вступят в канал — вы получите +1 кредит\n\n"
            "🏅 Значки:\n"
            "🥉 5 рефералов → Bronze\n"
            "🥈 15 рефералов → Silver\n"
            "🥇 30 рефералов → Gold\n"
            "💎 50 рефералов → Diamond"
        ),
        "not_admin":            "⛔ У вас нет прав администратора.",
        "broadcast_usage":      "📢 Использование: /broadcast &lt;текст сообщения&gt;",
        "broadcast_done":       "✅ Сообщение отправлено {count} пользователям.",
        "ban_usage":            "🔨 Использование: /ban &lt;user_id&gt;",
        "ban_done":             "✅ Пользователь {user_id} заблокирован.",
        "unban_done":           "✅ Пользователь {user_id} разблокирован.",
        "admin_panel":          (
            "🔧 <b>Админ Панель</b>\n\n"
            "👥 Всего пользователей: <b>{users}</b>\n"
            "🔗 Всего рефералов: <b>{referrals}</b>\n"
            "📅 Новых сегодня: <b>{today_users}</b>\n"
            "📅 Рефералов сегодня: <b>{today_refs}</b>\n\n"
            "Команды:\n"
            "/broadcast &lt;текст&gt; — Рассылка всем\n"
            "/ban &lt;user_id&gt; — Заблокировать\n"
            "/unban &lt;user_id&gt; — Разблокировать\n"
            "/export_users — Скачать CSV\n"
            "/export_referrals — Скачать CSV"
        ),
        "not_registered":       "⚠️ Вы не зарегистрированы. Отправьте /start.",
        "banned":               "⛔ Вы заблокированы в боте.",
        "verify_btn":           "✅ Вступил — Проверить",
        "share_phone_btn":      "📱 Поделиться номером",
    },

    "en": {
        "choose_language":      "🌐 Tilni tanlang / Choose language / Выберите язык:",
        "welcome_new":          "👋 Welcome! Let's get you registered.\n\nPlease enter your <b>first name</b>:",
        "welcome_back":         "👋 Welcome back, <b>{name}</b>! Use the menu below.",
        "ask_first_name":       "✏️ Enter your <b>first name</b>:",
        "ask_last_name":        "✏️ Enter your <b>last name</b>:",
        "ask_phone":            "📱 Share your phone number:",
        "wrong_phone":          "⚠️ Please use the button to share your phone number.",
        "name_too_long":        "⚠️ Name is too long. Please try again:",
        "captcha_question":     "🤖 Confirm you're human:\n\n<b>{a} + {b} = ?</b>",
        "captcha_wrong":        "❌ Wrong answer. Try again:\n\n<b>{a} + {b} = ?</b>",
        "captcha_not_number":   "⚠️ Please enter a number only.",
        "join_channel":         "📢 To confirm your referral, join our channel:\n👉 <b>{channel}</b>\n\nAfter joining, tap the button:",
        "not_joined":           "❌ You haven't joined the channel yet.\n👉 <b>{channel}</b>\n\nJoin and verify again:",
        "joined_confirmed":     "🎉 Channel membership confirmed! Referral credited.",
        "joined_no_ref":        "✅ Channel membership verified!",
        "registered":           (
            "🎊 Registration complete, <b>{name}</b>!\n\n"
            "🔗 Your referral link:\n<code>{link}</code>\n\n"
            "Share it with friends and earn <b>+1 credit</b> per person!"
        ),
        "btn_link":             "🔗 Referral Link",
        "btn_stats":            "📊 My Stats",
        "btn_top":              "🏆 Top Referrers",
        "btn_help":             "❓ Help",
        "btn_language":         "🌐 Language",
        "your_link":            "🔗 <b>Your Referral Link</b>\n\n<code>{link}</code>\n\n👥 Share it with friends!",
        "qr_caption":           "📱 Scan QR code or share the link:\n<code>{link}</code>",
        "stats":                (
            "📊 <b>Your Stats</b>\n\n"
            "👤 Name: <b>{full_name}</b>\n"
            "🆔 Username: <b>{username}</b>\n"
            "💎 Credits (Referrals): <b>{count}</b>\n"
            "🏅 Badge: <b>{badge}</b>\n"
            "📈 Rank: <b>#{rank}</b>\n"
            "📅 Member since: <b>{date}</b>\n\n"
            "{milestone_text}"
            "🔗 Your link:\n<code>{link}</code>"
        ),
        "milestone_next":       "🎯 Next badge: <b>{needed}</b> more referrals → {emoji} {name}\n\n",
        "milestone_max":        "🏆 You've reached the maximum level!\n\n",
        "top_title":            "🏆 <b>Top Referrers</b>\n",
        "top_empty":            "📭 No referrals yet. Be the first!",
        "top_row":              "{pos} {display} — <b>{count}</b> {badge}",
        "notif_new_referral":   "🎉 New referral! <b>{name}</b> joined using your link.\n💎 Total: <b>{total}</b> referrals {badge}",
        "milestone_reached":    "🎊 Congratulations! You've earned the <b>{emoji} {name}</b> badge!",
        "help":                 (
            "❓ <b>Help</b>\n\n"
            "🔗 /start — Start the bot\n"
            "📊 /stats — View your stats\n"
            "🏆 /top — Top referrers leaderboard\n"
            "🌐 /language — Change language\n\n"
            "📢 How referrals work:\n"
            "1. Get your unique link\n"
            "2. Share it with friends\n"
            "3. When they join the channel, you earn +1 credit\n\n"
            "🏅 Badges:\n"
            "🥉 5 referrals → Bronze\n"
            "🥈 15 referrals → Silver\n"
            "🥇 30 referrals → Gold\n"
            "💎 50 referrals → Diamond"
        ),
        "not_admin":            "⛔ You don't have admin rights.",
        "broadcast_usage":      "📢 Usage: /broadcast &lt;message text&gt;",
        "broadcast_done":       "✅ Message sent to {count} users.",
        "ban_usage":            "🔨 Usage: /ban &lt;user_id&gt;",
        "ban_done":             "✅ User {user_id} has been banned.",
        "unban_done":           "✅ User {user_id} has been unbanned.",
        "admin_panel":          (
            "🔧 <b>Admin Panel</b>\n\n"
            "👥 Total users: <b>{users}</b>\n"
            "🔗 Total referrals: <b>{referrals}</b>\n"
            "📅 New users today: <b>{today_users}</b>\n"
            "📅 Referrals today: <b>{today_refs}</b>\n\n"
            "Commands:\n"
            "/broadcast &lt;text&gt; — Send to all users\n"
            "/ban &lt;user_id&gt; — Ban a user\n"
            "/unban &lt;user_id&gt; — Unban a user\n"
            "/export_users — Download CSV\n"
            "/export_referrals — Download CSV"
        ),
        "not_registered":       "⚠️ You are not registered. Send /start to begin.",
        "banned":               "⛔ You have been banned from this bot.",
        "verify_btn":           "✅ I've Joined — Verify Me",
        "share_phone_btn":      "📱 Share My Phone Number",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Translate a key into the given language, with optional format args."""
    lang = lang if lang in TEXTS else "en"
    text = TEXTS[lang].get(key, TEXTS["en"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text
