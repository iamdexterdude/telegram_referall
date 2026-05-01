# 🤖 Telegram Referral Bot v2

Production-ready Telegram referral bot with full UX improvements.

**Stack:** Python 3.11 · aiogram 3 · SQLAlchemy 2 (async) · SQLite/PostgreSQL

---

## ✨ What's New in v2

| Feature | Description |
|---|---|
| 🌐 3 Languages | Uzbek, Russian, English — user picks on first start |
| 🤖 Captcha | Math question blocks bot abuse during registration |
| 🔔 Live notifications | Referrer gets instant message when someone joins via their link |
| 🏅 Badge system | Bronze → Silver → Gold → Diamond milestones with announcements |
| 📈 Rank display | User sees their exact leaderboard position in /stats |
| 🔄 Inline refresh | Stats and leaderboard update in-place with a button |
| 📱 QR codes | Bot generates a scannable QR for your referral link |
| 📤 Share button | Inline share button sends your link directly to any chat |
| 🔨 Ban system | Admins can ban/unban users from earning referrals |
| 📢 Broadcast | Admin sends a message to all registered users |
| 📊 Admin dashboard | Live stats: users today, referrals today, totals |

---

## 📁 Project Structure

```
referral_bot_v2/
├── main.py
├── config.py                        # Settings + badge/milestone logic
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── bot/
    ├── locales/
    │   └── translations.py          # All UI text in uz/ru/en
    ├── database/
    │   ├── models.py                # User, Referral ORM models
    │   └── engine.py                # Async engine + init_db()
    ├── handlers/
    │   ├── start.py                 # Language → Captcha → Register → Channel gate
    │   ├── menu.py                  # Link · Stats · Top · Help · QR · Callbacks
    │   └── admin.py                 # Admin panel, broadcast, ban, CSV export
    ├── services/
    │   ├── user_service.py          # User CRUD, rank, ban, leaderboard
    │   ├── referral_service.py      # Channel check, confirm referral, notify
    │   └── qr_service.py           # In-memory QR code generation
    ├── middlewares/
    │   ├── db_session.py            # Injects AsyncSession into every handler
    │   └── ban_check.py             # Blocks banned users at middleware level
    ├── keyboards/
    │   └── keyboards.py             # All inline + reply keyboards, language-aware
    └── utils/
        ├── helpers.py               # Code generator, link builder, captcha gen
        └── states.py                # FSM: LangSelect, Captcha, Registration, Channel
```

---

## ⚙️ Setup

### 1 — Install Python 3.11.9
Download from: https://www.python.org/downloads/release/python-3119/
➜ Windows installer (64-bit) → ✅ Add to PATH → Install Now

### 2 — Install dependencies
```bash
cd referral_bot_v2
py -3.11 -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 3 — Configure .env
```bash
copy .env.example .env
```
Fill in these values:
```env
BOT_TOKEN=your_token_from_botfather
BOT_USERNAME=your_bot_username_no_at_sign
CHANNEL_ID=@your_channel
ADMIN_IDS=your_telegram_numeric_id
```

### 4 — Make bot admin of your channel
Telegram → Channel → Edit → Administrators → Add your bot

### 5 — Run
```bash
python main.py
```

---

## 👤 User Flow

```
/start
  └── Choose Language (🇺🇿 / 🇷🇺 / 🇬🇧)
        └── Captcha (3 + 7 = ?)
              └── Enter First Name
                    └── Enter Last Name
                          └── Share Phone Number
                                └── [If referred] Join Channel → Verify
                                      └── Main Menu ✅
```

---

## 🏅 Badge Milestones

| Referrals | Badge |
|---|---|
| 5  | 🥉 Bronze |
| 15 | 🥈 Silver |
| 30 | 🥇 Gold |
| 50 | 💎 Diamond |

When a user hits a milestone, they get an instant congratulations message.

---

## 🔧 Admin Commands

| Command | Description |
|---|---|
| `/admin` | Dashboard: users, referrals, today's stats |
| `/broadcast <text>` | Send message to all users |
| `/ban <user_id>` | Ban a user |
| `/unban <user_id>` | Unban a user |
| `/export_users` | Download users CSV |
| `/export_referrals` | Download referrals CSV |

---

## 🗄️ Database Schema

```sql
CREATE TABLE users (
    id             INTEGER PRIMARY KEY,
    user_id        BIGINT UNIQUE NOT NULL,
    username       VARCHAR(64),
    first_name     VARCHAR(128) NOT NULL,
    last_name      VARCHAR(128),
    phone_number   VARCHAR(32),
    referral_code  VARCHAR(16) UNIQUE NOT NULL,
    referral_count INTEGER DEFAULT 0,
    referred_by    BIGINT,
    language       VARCHAR(4) DEFAULT 'en',
    is_banned      BOOLEAN DEFAULT FALSE,
    link_clicks    INTEGER DEFAULT 0,
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE referrals (
    id               INTEGER PRIMARY KEY,
    referrer_id      BIGINT NOT NULL,
    referred_user_id BIGINT UNIQUE NOT NULL,   -- one referral per user, enforced at DB level
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🐘 Switch to PostgreSQL
Just change one line in `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/referral_bot
```
Then: `pip install asyncpg` and restart. No code changes needed.
