from .bot import bot
from .state import (
    START_STATE, CONTACT_STATE, LOCATION_STATE, TRAVEL_STATE,
)
from .handlers import (
    start_handler, start_parsing_handler, contact_handler, location_handler, region_handler, travel_handler,
)

from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    Dispatcher,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    PicklePersistence,
    PreCheckoutQueryHandler,
)

dispatcher = Dispatcher(
    bot,
    workers=0,
    update_queue=None,
    persistence=PicklePersistence("telegram_bot/state"),
)

# Handle start command

start_command_handler = CommandHandler("start", start_handler)
start_parsing = CommandHandler("start_parsing", start_parsing_handler)
region_callback = CallbackQueryHandler(callback=region_handler)

dispatcher.add_handler(
    ConversationHandler(
        name="main",
        persistent=True,
        entry_points=[CommandHandler("start", start_handler)],
        states={
            START_STATE: [
                start_command_handler,
                start_parsing,
                # MessageHandler(filters=Filters.text, callback=conversation_handler),
            ],
            CONTACT_STATE: [
                start_command_handler,
                start_parsing,
                MessageHandler(filters=Filters.contact, callback=contact_handler)
            ],
            LOCATION_STATE: [
                start_command_handler,
                start_parsing,
                region_callback,
                MessageHandler(filters=Filters.location, callback=location_handler)
            ],
            TRAVEL_STATE: [
                start_command_handler,
                start_parsing,
                CallbackQueryHandler(callback=travel_handler)
            ]
        },
        fallbacks=[CommandHandler("start", start_handler)],
    )
)
