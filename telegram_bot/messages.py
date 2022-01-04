import json

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ChosenInlineResult,
    InlineKeyboardButton,
)
from telegram.ext import CallbackContext

from telegram_bot.bot import bot
from telegram_bot.config import send_chunked_message
from travel_app.models import Region, Location


def send_text_message(context: CallbackContext, user_id: int, text):
    message = bot.send_message(
        user_id,
        text=text,
    )

    context.chat_data["id"] = message.chat_id
    context.user_data["last_message_id"] = message.message_id


def send_contact_message(user_id: int, context) -> None:
    share_contact_button = KeyboardButton(
        "Поділитись контактом", request_contact=True
    )
    keyboard = ReplyKeyboardMarkup([[share_contact_button]])

    if "last_messages_ids" not in context.user_data:
        context.user_data["last_messages_ids"] = []

    message = bot.send_message(
        user_id,
        reply_markup=keyboard,
        text="Поділитись контактом",
    )
    context.user_data["last_messages_ids"].append(message.message_id)
    context.chat_data["id"] = message.chat_id


def send_location_message(user_id: int, context) -> None:
    find_address_where_button = KeyboardButton(
        "Поділитись геопозицією",
        request_location=True,

    )
    keyboard = ReplyKeyboardMarkup([[find_address_where_button]])
    if "last_messages_ids" not in context.user_data:
        context.user_data["last_messages_ids"] = []

    message = bot.send_message(user_id, reply_markup=keyboard, text="Поділитись геопозицією")
    context.user_data["last_messages_ids"].append(message.message_id)
    context.chat_data["id"] = message.chat_id


def send_regions_buttons(user_id: int, context) -> None:
    variant_buttons = [
        InlineKeyboardButton(
            text=region.name,
            callback_data=json.dumps(
                {"region": region.id}
            )
        )
        for region in Region.objects.all()
    ]
    send_chunked_message(
        user_id=user_id,
        bot=bot,
        buttons=variant_buttons,
        chunk=3,
        text="Виберіть регіон для подорожі",
        context=context
    )


def send_locations_message(user_id: int, context, region) -> None:
    variant_buttons = [
        InlineKeyboardButton(
            text=location.name,
            callback_data=json.dumps(
                {"location": location.id}
            )
        )
        for location in Location.objects.filter(region=region)
    ]
    send_chunked_message(
        user_id=user_id,
        bot=bot,
        buttons=variant_buttons,
        chunk=1,
        text="Виберіть цікаве для вас місце",
        context=context
    )
