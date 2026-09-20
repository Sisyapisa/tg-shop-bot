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
