from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext


def parse_google_response(response):
    address = {
        "city": None,
        "street": None,
        "house": None,
        "post_index": None,
        "google_place_id": None,
    }
    address_components = response[0].get("address_components")
    for component in address_components:
        list_of_types = component.get("types")
        if (
                "route" in list_of_types
                or "point_of_interest" in list_of_types
                and "establishment" in list_of_types
        ):
            address["street"] = component.get("long_name")
        if "street_number" in list_of_types:
            address["house"] = component.get("long_name")
        if "locality" in list_of_types and "political" in list_of_types:
            address["city"] = component.get("long_name")
        if "postal_code" in list_of_types:
            address["post_index"] = component.get("long_name")
    address["google_place_id"] = response[0].get("place_id")
    return address


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def remove_last_message(context: CallbackContext):
    try:
        context.bot.delete_message(
            context.chat_data["id"], context.user_data["last_message_id"]
        )
    except:
        pass


def remove_last_inline_messages(context: CallbackContext):
    if "last_messages_ids" not in context.user_data:
        return
    for message_id in context.user_data["last_messages_ids"]:
        try:
            context.bot.delete_message(context.chat_data["id"], message_id)
        except:
            pass
    context.user_data["last_messages_ids"].clear()


def send_chunked_message(
        user_id,
        bot,
        context,
        buttons: list,
        photo=None,
        text: str = "...",
        limit: int = 45,
        chunk: int = 3,
):
    if "last_messages_ids" not in context.user_data:
        context.user_data["last_messages_ids"] = []

    if len(buttons) > limit:
        first = True
        for x in range(0, len(buttons), limit):
            reply_markup = InlineKeyboardMarkup(
                list(chunks(buttons[x: x + limit], chunk))
            )
            if first and photo:
                message = bot.send_photo(
                    user_id,
                    # get_photo(photo_url),
                    reply_markup=reply_markup,
                )
            else:
                message = bot.send_message(
                    user_id,
                    text=text,
                    reply_markup=reply_markup,
                )
            first = False
            context.user_data["last_messages_ids"].append(message.message_id)
    else:
        if photo:
            message = bot.send_photo(
                user_id,
                photo,
                # get_photo(photo_url),
                reply_markup=InlineKeyboardMarkup(list(chunks(buttons, chunk))),
            )
        else:
            message = bot.send_message(
                user_id,
                text=text,
                reply_markup=InlineKeyboardMarkup(list(chunks(buttons, chunk))),
            )
        context.user_data["last_messages_ids"].append(message.message_id)
        context.chat_data["id"] = message.chat_id
