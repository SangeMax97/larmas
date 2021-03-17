from django.shortcuts import render
from django.http import JsonResponse

from collections import defaultdict

# from sentence_parser.models import Text
from corpus.models import Language, SpeechMetadata, SignMetadata
from django.db.models import Max
import random

def get_random(things):
    max_id = eval(things).objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        t = eval(things).objects.filter(pk=pk).first()
        if t:
            return t

# Create your views here.
def index(request):
    # print('index')
    # print(request.GET)
    text = get_random('Language')
    return render(request, 'translate_text/index.html', {'text': text})

def add_translation(request):
    print('add_translation')

    if(request.method == 'POST'):
        print(request.POST)
        language = request.POST.get('language', '')
        text = request.POST.get('text', '')
        translation = request.POST.get('translation', '')

        if(language == ''):
            return JsonResponse({'response': 'Please specify target language.'})
        if(translation == ''): 
            return JsonResponse({'response': 'Translation is empty.'})

        prompt = Language.objects.get(text=text)
        prompt.translations.get_or_create(text=translation, language=language)
        return JsonResponse({'response': 'Translation has been added, Thank you for your contribution! Feel free to add more.'})


    text = get_random('Language')
    return render(request, 'translate_text/index.html', {'text': text})

def search_translation(request):
    print('search_translation')

    if(request.method == 'POST'):
        print(request.POST)
        language = request.POST.get('language', '')
        text = request.POST.get('text', '')

        if(text == ''): 
            return JsonResponse({'response': 'Text to translate is empty.'})

        try:
            prompt = Language.objects.get(text=text)
        except:
            return JsonResponse({'response': 'No translations found for text'})
        
        if(language == ''):
            translations = prompt.translations.all().values('text', 'language')
            
        else:
            translations = prompt.translations.filter(language=language).values('text', 'language')

        context = defaultdict(list)
        for translation in translations:
            t = translation['text']
            l = translation['language']
            
            print(translation)
            print(t)
            print(l)

            print()
            context[l].append(t)
        return JsonResponse({'translations': context})

    text = get_random('Language')
    return render(request, 'translate_text/index.html', {'text': text})


from django.core.serializers import serialize

def get_text(request):
    language = request.POST.get('language', 'Language')

    text = get_random(language)

    data = serialize("json", [text], fields=('language', 'text'))


    print(data)


    return JsonResponse({'text': data}, safe=False)


def get_audio(request):
    speech = get_random('SpeechMetadata')

    audio = speech.audio
    audio = str(audio)
    text  = speech.text

    data = serialize("json", [text], fields=('language', 'text'))
    print(audio)

    return JsonResponse({'text': data, 'audio':audio}, safe=False)


def get_video(request):
    sign = get_random('SignMetadata')

    video = sign.video
    video = str(video)
    text  = sign.text

    data = serialize("json", [text], fields=('language', 'text'))
    print(video)

    return JsonResponse({'text': data, 'video':video}, safe=False)
