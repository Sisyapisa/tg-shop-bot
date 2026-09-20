from aiogram import Bot

async def notify_admin(bot: Bot, admin_id: int, text: str):
    if not admin_id:
        return
    try:
        await bot.send_message(admin_id, text, parse_mode='html')
    except Exception as e:
        print(f"Не удалось отправить админу {e}")