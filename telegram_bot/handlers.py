from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup

from travel_app.services import Parser
from .config import remove_last_message
from .models import TelegramUser
from .state import (
    START_STATE, LOCATION_STATE, CONTACT_STATE, TRAVEL_STATE,
)
from .messages import *


def start_handler(update: Update, context) -> None:
    user_id = update.message.from_user.id
    send_text_message(
        context=context,
        text="Вітаю в помічнику Туриста",
        user_id=user_id,
    )
    if TelegramUser.objects.filter(id=user_id):
        keyboard_deleter = update.message.reply_text(
            "Секундочку...", reply_markup=ReplyKeyboardRemove()
        )
        keyboard_deleter.delete()
        send_location_message(
            user_id=user_id,
            context=context,
        )
        return LOCATION_STATE
    send_contact_message(user_id=user_id, context=context)
    return CONTACT_STATE


def contact_handler(update: Update, context) -> None:
    remove_last_message(context)
    keyboard_deleter = update.message.reply_text(
        "Секундочку...", reply_markup=ReplyKeyboardRemove()
    )
    keyboard_deleter.delete()
    user_id = update.message.from_user.id
    contact = update.effective_message.contact
    user = TelegramUser.init_from_contact(contact)
    user.save()
    send_location_message(
        user_id=user_id,
        context=context,
    )
    return LOCATION_STATE


def start_parsing_handler(update: Update, context) -> None:
    user_id = update.message.from_user.id
    send_text_message(text="Розпочато парсинг локацій", user_id=user_id, context=context)
    Parser.start_parsing()
    send_text_message(text="Парсинг завершився", user_id=user_id, context=context)


def location_handler(update: Update, context):
    # keyboard_deleter = update.message.reply_text(
    #     "Секундочку...", reply_markup=ReplyKeyboardRemove()
    # )
    # keyboard_deleter.delete()
    user_id = update.message.from_user.id
    send_regions_buttons(context=context, user_id=user_id)
    location = update.message.location
    telegram_user = TelegramUser.objects.filter(id=user_id).first()
    telegram_user.longitude = location.longitude
    telegram_user.latitude = location.latitude
    telegram_user.save()


def region_handler(update: Update, context):
    remove_last_message(context)
    query = update.callback_query
    data = json.loads(query.data)
    region = Region.objects.get(id=data.get('region'))
    user_id = update.callback_query.from_user.id
    send_locations_message(context=context, user_id=user_id, region=region)
    return TRAVEL_STATE


def travel_handler(update: Update, context):
    user_id = update.callback_query.from_user.id
    remove_last_message(context)
    query = update.callback_query
    data = json.loads(query.data)
    telegram_user = TelegramUser.objects.filter(id=user_id).first()
    location = Location.objects.get(id=data.get('location'))
    finish_location = location.name.replace(" ", "-")
    send_text_message(text=f'Посилання на маршрут: \n google.com/maps/dir/{telegram_user.latitude},+{telegram_user.longitude}/{finish_location}/',
                      user_id=user_id, context=context)
    send_location_message(
        user_id=user_id,
        context=context,
    )

    return LOCATION_STATE
