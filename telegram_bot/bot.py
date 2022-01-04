from telegram import Bot
from django.conf import settings

bot = Bot(settings.TELEGRAM_BOT["TOKEN"])
if bot.getWebhookInfo().url != settings.TELEGRAM_BOT["WEBHOOK_URL"]:
    bot.set_webhook(settings.TELEGRAM_BOT["WEBHOOK_URL"])
