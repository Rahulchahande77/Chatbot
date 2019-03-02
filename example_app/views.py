import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
from chatterbot.comparisons import levenshtein_distance

class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)
    chatterbot.set_trainer(ChatterBotCorpusTrainer)
    chatterbot.train("chatterbot.corpus.english")

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.read().decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(
            input_data,
            input_data.get('conversation', 'default')
        )
        response_data = response.serialize()
        print("response_data = ",response_data)

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })

def train_request(request):
    try:
        data = json.loads(request.body)
        chatterbot = ChatBot(**settings.CHATTERBOT)
        chatterbot.set_trainer(ListTrainer)
        chatterbot.train([
            data['inputText'],
            data['outputText'],
        ])
        return JsonResponse({'text': 'Ok, now I get that, let us move forword'})
    except:
        return JsonResponse({'text': "Sorry I couldn't store your statements please train me again"})

