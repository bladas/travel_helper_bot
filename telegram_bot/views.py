import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .bot import bot
from telegram import Update
from .dispatcher import dispatcher


@csrf_exempt
def webhook(request):
    try:
        update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)
        dispatcher.process_update(update)
    except Exception as e:
        print(e)

    return JsonResponse({})
