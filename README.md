# 🛍 Telegram Shop Bot

> Полноценный Telegram-бот магазина с каталогом, корзиной, оплатой и админ-панелью. Готов к запуску и продаже.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?logo=telegram&logoColor=white)](https://docs.aiogram.dev)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Возможности

### 👤 Для пользователя

- 📦 **Каталог** с категориями и товарами (из базы данных)
- 🛒 **Покупка** товаров за внутренние монеты
- 💳 **Пополнение баланса** (готово к интеграции с ЮKassa / Telegram Payments)
- 👤 **Профиль** с балансом и ID
- 📋 **История заказов** — все покупки с датами и суммами
- 🎯 **Интуитивный интерфейс** — inline-кнопки, FSM-диалоги

### 🔧 Для администратора

- 📊 **Статистика** — юзеры, заказы, общая сумма
- 📦 **Все заказы** — последние 10 с деталями
- 👥 **Список юзеров** — имена, username, баланс
- 🔔 **Уведомления** о новых заказах в реальном времени
- 🔐 **Защита** — админ-панель доступна только ADMIN_ID

### 🛠 Технические фишки

- ⚡ **Асинхронность** — aiogram 3.x + aiosqlite
- 🗄 **SQLAlchemy 2.0** — современный ORM с типами
- 🏗 **Чистая архитектура** — handlers / repositories / models
- 🔄 **Middleware** для сессии БД — одна сессия на запрос
- ✅ **Валидация** баланса перед покупкой
- 🎨 **CallbackData фабрики** — типобезопасные кнопки

---

## 🛠 Стек технологий

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.12+ | Язык |
| **aiogram** | 3.x | Telegram Bot API |
| **SQLAlchemy** | 2.0 | ORM |
| **aiosqlite** | 0.20+ | Async SQLite |
| **python-dotenv** | 1.0+ | Загрузка `.env` |

---

## 📁 Структура проекта

```
Tg/
├── Handlers/              # Обработчики (роутеры)
│   ├── start.py          # /start
│   ├── info.py           # "О нас"
│   ├── Catalog.py        # Каталог и покупка
│   ├── profile.py        # Профиль и заказы
│   └── admin.py          # Админ-панель
│
├── database/              # Работа с БД
│   ├── models/           # SQLAlchemy модели
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── item.py
│   │   └── order.py
│   └── __init__.py       # Экспорт моделей
│
├── repositories/          # CRUD-репозитории
│   ├── user.py
│   ├── categories.py
│   ├── item.py
│   └── order.py
│
├── keyboards/             # Inline / Reply клавиатуры
│   ├── menu.py
│   ├── catalog.py
│   ├── profile.py
│   └── admin.py
│
├── filters/               # Кастомные фильтры
│   ├── is_admin.py       # Проверка админа
│   └── check_buy_item.py # Проверка баланса
│
├── middlewares/           # Middleware
│   └── session.py        # Сессия БД в data
│
├── states/                # FSM-состояния
│   └── profile.py
│
├── utils/                 # Утилиты
│   └── notify.py         # Уведомления админу
│
├── main.py                # Точка входа
├── .env                   # Токены (не в Git!)
├── .gitignore
└── requirements.txt
```
---

## ⚙️ Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Sisyapisa/tg-shop-bot.git
cd tg-shop-bot

```

### 2. Создай виртуальное окружение

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / Mac:
source venv/bin/activate
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

### 4. Создай `.env`

```env
BOT_TOKEN=твой_токен_от_BotFather
ADMIN_ID=твой_telegram_id
```

**Где взять:**
- `BOT_TOKEN` — [@BotFather](https://t.me/BotFather) → `/newbot`
- `ADMIN_ID` — [@userinfobot](https://t.me/userinfobot)

### 5. Запусти

```bash
python main.py
```

---

## 📸 Скриншоты

| Каталог | Карточка товара |
|---------|-----------------|
| ![](screenshots/catalog.png) | ![](screenshots/item.png) |

| Профиль | Админ-панель |
|---------|--------------|
| ![](screenshots/profile.png) | ![](screenshots/admin.png) |

---

## 🎯 Что можно добавить

- [ ] Интеграция с **ЮKassa** (реальная оплата)
- [ ] **Корзина** (несколько товаров в заказе)
- [ ] **CRUD товаров** через админку
- [ ] **Пагинация** в заказах и юзерах
- [ ] **Промокоды** и скидки
- [ ] **Webhook** вместо polling

---

## 💼 Для чего подходит

Этот бот — **готовое решение** для:

- 🛍 **Интернет-магазинов** в Telegram
- 🎁 **Продажи цифровых товаров**
- 🍕 **Доставки еды**
- 👟 **Магазинов одежды / обуви**
- 📚 **Продажи курсов / книг**

**Легко адаптируется** под любой бизнес: меняешь категории и товары в БД — и бот готов.

---

## 👨‍💻 Автор

**Матвей** — Python-разработчик Telegram-ботов

- 📱 Telegram: [@pipapupapipu]
- 💻 GitHub: [@Sisyapisa](https://github.com/Sisyapisa)

**Нужен бот?** Пиши в Telegram — обсудим!

---

## 📄 Лицензия

MIT — используй **свободно**, в том числе **в коммерческих целях**.

---

⭐ **Понравился проект?** Поставь звезду на GitHub!