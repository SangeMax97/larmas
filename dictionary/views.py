from django.shortcuts import render, redirect
from django.views import generic
# from corpus.models import English, IsiXhosa, Sesotho
from corpus.models import Language, LanguageMetadata, SpeechMetadata, SignMetadata, Index
from corpus.models import levenshtein
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from collections import defaultdict
import json
from random import sample

filter_global = 'a'

def to_struct(language):
    result = defaultdict(list)
    grouped = defaultdict(list)

    if(len(language) ==0):
        return {}
        
    for language in language:
        for meta in language.text_metadata.filter(text__text=language.text):
            key = meta.part_of_speech 
            value = meta
            grouped[key].append(value)
        result[language].append(grouped.items())
        grouped = defaultdict(list)

    context = {
        'result': result.items()
    }
    return context

def get_prompt(prompt):
    Language.filter

def get_dictionary(lang='', prompt='', filter_=None):
    result = defaultdict(list)
    grouped = defaultdict(list)
    language = 0
    if(lang==''):
        lang = 'All languages'
    if(prompt != ''):
        language = Language.objects.filter(text=prompt)
        print(language)
        print('--------------')
        lang = ''
        if(len(language) != 0): lang = language[0].language

        for l in language:
            l.num_searches += 1
            l.save()
    else:
        language = Language.objects.filter(language=lang)

    if(filter_):
        print('filtering: ' + str(filter_))
        language = language.filter(text__startswith=filter_)
    
    language_copy = language
     
    if(len(language) ==0):
        return {}, language_copy
    

    context = to_struct(language)
    context['language'] = lang
    context['prompt'] = prompt
        
    return context, language_copy

# Create your views here.

def change_filter(request):
    global filter_global
    filter_global = request.POST.get('filter_', '').lower()
    print(filter_global)
    print(filter_global)
    print(filter_global)
    return HttpResponse('done')

def dict_2(request):
        
    context, language = get_dictionary()

    # indices = open('IsiXhosa_index.json').read()
    # indices = json.loads(indices)

    # a = ['1', '2', '3', '4']
    # print(sample(a, k=2))

    # context = to_struct(language)
    # context['language'] = 'All languages'
    # context['prompt'] = prompt
        
    # return context, language_copy

    return render(request, 'dictionary/index.html', context)

def dictionary(request, language):

    context, language = get_dictionary(lang=language)
    
    return render(request, 'dictionary/index.html', context)

def audio(request):

    # languages = ['English', 'IsiXhosa', 'Sesotho']

    # result = []

    # for i in languages:
    #     context_, language_ = get_dictionary(lang=i)
    #     result.append(context_) 

    # Unlabelled = to_struct(Language.objects.filter(~(Q(language='English') | Q(language='IsiXhosa') | Q(language='Sesotho'))))    
    # if(len(Unlabelled) != 0):
    #     Unlabelled['language'] = 'Unlabelled'
    #     result.append(Unlabelled)
    #     languages.append('Unlabelled')

    # print(Unlabelled)
    
    # context = {
    #     'response': result,
    #     'languages': languages,
    #     'corpus': Language.objects.all().values('text', 'language')
    # }

    # context = {
    #     'English': {
    #         'response': result[0],
    #         'corpus' : Language.objects.filter(Q(language='English')).values('text', 'language')
    #     },
    #     'Sesotho': {
    #         'response': result[2],
    #         'corpus' : Language.objects.filter(Q(language='Sesotho')).values('text', 'language')
    #     },
    #     'IsiXhosa': {
    #         'response': result[1],
    #         'corpus' : Language.objects.filter(Q(language='IsiXhosa')).values('text', 'language')
    #     },
    #     'Unlabelled': {
    #         'response': result[3],
    #         'corpus' : Language.objects.filter(~(Q(language='English') | Q(language='IsiXhosa') | Q(language='Sesotho'))).values('text', 'language')
    #     },
    # }
    
    # print(result[3])
    # return JsonResponse()

    return render(request, 'dictionary/audio.html')


def video(request):

    # languages = ['English', 'IsiXhosa', 'Sesotho']

    # result = []

    # for i in languages:
    #     context_, language_ = get_dictionary(lang=i)
    #     result.append(context_) 

    # Unlabelled = to_struct(Language.objects.filter(~(Q(language='English') | Q(language='IsiXhosa') | Q(language='Sesotho'))))    
    # if(len(Unlabelled) != 0):
    #     Unlabelled['language'] = 'Unlabelled'
    #     result.append(Unlabelled)
    #     languages.append('Unlabelled')

    # print(Unlabelled)
    
    # context = {
    #     'response': result,
    #     'languages': languages,
    #     'corpus': Language.objects.all().values('text', 'language')
    # }

    # context = {
    #     'English': {
    #         'response': result[0],
    #         'corpus' : Language.objects.filter(Q(language='English')).values('text', 'language')
    #     },
    #     'Sesotho': {
    #         'response': result[2],
    #         'corpus' : Language.objects.filter(Q(language='Sesotho')).values('text', 'language')
    #     },
    #     'IsiXhosa': {
    #         'response': result[1],
    #         'corpus' : Language.objects.filter(Q(language='IsiXhosa')).values('text', 'language')
    #     },
    #     'Unlabelled': {
    #         'response': result[3],
    #         'corpus' : Language.objects.filter(~(Q(language='English') | Q(language='IsiXhosa') | Q(language='Sesotho'))).values('text', 'language')
    #     },
    # }
    
    # print(result[3])
    # return JsonResponse()

    return render(request, 'dictionary/video.html')


def index(request):
    global filter_global
    
    languages = ['English', 'IsiXhosa', 'Sesotho']

    id_tuple = []
    result = []

    indices = open('/Users/sange/Work/msc_apps-master/dictionary/IsiXhosa_index.json').read()
    indices = json.loads(indices)

    index = indices[filter_global]
    index = sample(index, 50)

    language = Language.objects.filter(id__in=index)
    language = to_struct(language)
    language['language'] = 'IsiXhosa'

    result.append(language) 

    indices = open('/Users/sange/Work/msc_apps-master/dictionary/English_index.json').read()
    indices = json.loads(indices)

    index = indices[filter_global]
    print(len(index))
    index = sample(index, 50)

    language = Language.objects.filter(id__in=index)
    language = to_struct(language)
    language['language'] = 'English'

    result.append(language) 

    language = {}
    language['language'] = 'Sesotho'

    result.append(language) 

    Unlabelled = to_struct(
        Language.objects.filter(~(Q(language='English') | Q(language='IsiXhosa') | Q(language='Sesotho'))).filter(single_word=True)
    )    
    if(len(Unlabelled) != 0):
        Unlabelled['language'] = 'Unlabelled'
        result.append(Unlabelled)
        languages.append('Unlabelled')

    print(Unlabelled)
    
    context = {
        'response': result,
        'languages': languages,
    }

    # print(Unlabelled)


    # context = {
    #     'English': {
    #         'response': result[0],
    #         'corpus' : Language.objects.filter(Q(language='English')).values('text', 'language')
    #     },
    #     'Sesotho': {
    #         'response': result[2],
    #         'corpus' : Language.objects.filter(Q(language='Sesotho')).values('text', 'language')
    #     },
    #     'IsiXhosa': {
    #         'response': result[1],
    #         'corpus' : Language.objects.filter(Q(language='IsiXhosa')).values('text', 'language')
    #     },
    #     'Unlabelled': {
    #         'response': result[3],
    #         'corpus' : Language.objects.filter(~(Q(language='English') | Q(language='IsiXhosa') | Q(language='Sesotho'))).values('text', 'language')
    #     },
    # }
    
    # print(result[3])
    # return JsonResponse()

    return render(request, 'dictionary/thesaurus.html', context)

def dictionary_search(request):
    if(request.method == 'GET'):

        prompt = request.GET.get('prompt', '').lower().strip()

        if(prompt ==''): return index(request)

        context, language = get_dictionary(prompt=prompt)

        print(context)
        print()
        print()
        print(list(language.values('text')))

        res = map(lambda x: x['text'], list(language.values('text')))

        print(':::::')
        print(list(res))
        print(':::::')
        result = list(map(lambda x: x[1], filter(lambda x: x[0]<3,  [levenshtein(prompt, t) for t in res])))

        context['near_matches'] = result

        return render(request, 'dictionary/index.html', context)
    return render(request, 'dictionary/index.html')

def add_prompt_first_time(request):
    if(request.method == 'POST'):
      
        language = request.POST.get('Language', '')
        definition = request.POST.get('Definition', '')
        usage = request.POST.get('Usage', '')
        part_of_speech = request.POST.get('POS', '')
        text = request.POST.get('Text', '').lower()

        if(definition == '' or usage == '' or part_of_speech == '' or text == '' or language == ''):
            return render(request, 'dictionary/index.html')

        prompt = Language.objects.create(
            text = text,
            language = language
        )

        metadata = LanguageMetadata(
            text = prompt,
            user = request.user,
            definition = definition,
            usage = usage,
            part_of_speech = part_of_speech
        )
        metadata.save()
    
    return render(request, 'dictionary/index.html')

def add_prompt(request):
    if(request.method == 'POST'):
        # print(request.POST)
        definition = request.POST.get('Definition', '')
        usage = request.POST.get('Usage', '')
        part_of_speech = request.POST.get('POS', '')
        text = request.POST.get('Text', '')

        if(definition == '' or usage == '' or part_of_speech == '' or text == ''):
            return render(request, 'dictionary/index.html')

        prompt = Language.objects.filter(text=text)[0]
        metadata = LanguageMetadata(
            text = prompt,
            user = request.user,
            definition = definition,
            usage = usage,
            part_of_speech = part_of_speech
        )
        metadata.save()
    
    return render(request, 'dictionary/index.html')

def vote(request):
    if(request.method == 'POST'):
        text = request.POST.get('prompt', '')
        vote = request.POST.get('vote', '')
        vote_category = request.POST.get('vote_category', '')
        media = request.POST.get('media', '')

        # print(text)
        # print(vote)
        # print(vote_category)
        # print(media)

        if(media != ''):
            if(vote_category == 'speech_accuracy'):    
                speech = SpeechMetadata.objects.get(audio=media)
                if(vote == 'Yes'):
                    speech.pronounciation_is_accurate_num_votes += 1       
                elif(vote == 'No'):
                    speech.pronounciation_is_not_accurate_num_votes += 1
                elif(vote == 'Not Sure'):
                    speech.pronounciation_accuracy_not_sure_num_votes += 1
                speech.save()

            elif(vote_category == 'sign_accuracy'):
                sign = SignMetadata.objects.get(video=media)
                if(vote == 'Yes'):
                    sign.sign_is_accurate_num_votes += 1       
                elif(vote == 'No'):
                    sign.sign_is_not_accurate_num_votes += 1
                elif(vote == 'Not Sure'):
                    sign.sign_accuracy_not_sure_num_votes += 1
                sign.save()

        elif(text != ''):
            prompt = Language.objects.get(text=text)
            if(vote_category == 'pronounciation'):    
                if(vote == 'Easy'):
                    prompt.pronounciation_is_easy_num_votes += 1       
                elif(vote == 'Average'):
                    prompt.pronounciation_is_average_num_votes += 1
                elif(vote == 'Difficult'):
                    prompt.pronounciation_is_difficult_num_votes += 1
                elif(vote == 'Not Sure'):
                    prompt.pronounciation_not_sure_num_votes += 1

            elif(vote_category == 'sign'):    
                if(vote == 'Easy'):
                    prompt.sign_is_easy_num_votes += 1       
                elif(vote == 'Average'):
                    prompt.sign_is_average_num_votes += 1
                elif(vote == 'Difficult'):
                    prompt.sign_is_difficult_num_votes += 1
                elif(vote == 'Not Sure'):
                    prompt.sign_not_sure_num_votes += 1
            
            elif(vote_category == 'heteronym'):    
                if(vote == 'Yes'):
                    prompt.is_heteronym_num_votes += 1       
                elif(vote == 'No'):
                    prompt.is_not_heteronym_num_votes += 1
                elif(vote == 'Not Sure'):
                    prompt.heteronym_not_sure_num_votes += 1

            elif(vote_category == 'heteronym_sign'):    
                if(vote == 'Yes'):
                    prompt.is_heteronym_sign_num_votes += 1       
                elif(vote == 'No'):
                    prompt.is_not_heteronym_sign_num_votes += 1
                elif(vote == 'Not Sure'):
                    prompt.heteronym_sign_not_sure_num_votes += 1
            prompt.save()

    return render(request, 'dictionary/index.html') 


def qa(request):
    if(request.method == 'POST'):

        print(request.POST)
        print()

        qa_category = request.POST.get('qa_category', '')
        media = request.POST.get('media', '')

        accurate_pronunciation = request.POST.get('accurate_pronunciation','')

        text_offensive = request.POST.get('text_offensive','')
        text_spelling_errors = request.POST.get('text_spelling_errors','')
        
        if qa_category == 'audio':
            audio_plays = request.POST.get('audio_plays','')
            audio_represents_text = request.POST.get('audio_represents_text','')
            audio_clipped = request.POST.get('audio_clipped','')
            audio_offensive = request.POST.get('audio_offensive','')

            speech = SpeechMetadata.objects.get(audio=media)

            if(accurate_pronunciation == 'yes'):
                speech.pronounciation_is_accurate_num_votes += 1       
            elif(accurate_pronunciation == 'no'):
                speech.pronounciation_is_not_accurate_num_votes += 1
            elif(accurate_pronunciation == 'not_sure'):
                speech.pronounciation_accuracy_not_sure_num_votes += 1

            if text_offensive == 'true':
                speech.text_offensive_num_votes += 1  
            if text_spelling_errors == 'true':
                speech.text_spelling_errors_num_votes += 1  
            if audio_plays == 'true':
                speech.audio_plays_num_votes += 1   
            if audio_represents_text == 'true':
                speech.audio_represents_text_num_votes += 1   
            if audio_clipped == 'true':
                speech.audio_clipped_num_votes += 1   
            if audio_offensive == 'true':
                speech.audio_offensive_num_votes += 1      

            speech.save()

        elif qa_category == 'video':
            video_plays = request.POST.get('video_plays','')
            video_represents_text = request.POST.get('video_represents_text','')
            video_clipped = request.POST.get('video_clipped','')
            video_offensive = request.POST.get('video_offensive','')
            text_offensive = request.POST.get('text_offensive','')
            text_spelling_errors = request.POST.get('text_spelling_errors','')

            sign = SignMetadata.objects.get(video=media)

            if(accurate_pronunciation == 'yes'):
                sign.sign_is_accurate_num_votes += 1       
            elif(accurate_pronunciation == 'no'):
                sign.sign_is_not_accurate_num_votes += 1
            elif(accurate_pronunciation == 'not_sure'):
                sign.sign_accuracy_not_sure_num_votes += 1

            if text_offensive == 'true':
                sign.text_offensive_num_votes += 1  
            if text_spelling_errors == 'true':
                sign.text_spelling_errors_num_votes += 1  
            if video_plays == 'true':
                sign.video_plays_num_votes += 1   
            if video_represents_text == 'true':
                sign.video_represents_text_num_votes += 1   
            if video_clipped == 'true':
                sign.video_clipped_num_votes += 1   
            if video_offensive == 'true':
                sign.video_offensive_num_votes += 1 

            sign.save()

    return JsonResponse({'response': 'success'}) 

def get_metadata(request):
    if(request.method == 'POST'):
        # print(request.POST)

        text = request.POST.get('prompt', '')
        metadata_category = request.POST.get('metadata_category', '')
        
        # print(text)
        # print(metadata_category)   
       
        if(metadata_category == 'speech'):    
            metadata = SpeechMetadata.objects.filter(text__text=text).values(
                'audio', 'user__gender', 'user__first_language'
            )
            print(metadata)
            return  JsonResponse({'metadata': list(metadata),})
        
        elif(metadata_category == 'sign'):   
            metadata = SignMetadata.objects.filter(text__text=text).values(
                'video', 'user__gender', 'user__first_language'
            )
            return  JsonResponse({'metadata': list(metadata),})
            
    return render(request, 'dictionary/index.html') 

def get_thesaurus(request):
    if(request.method == 'POST'):
        # print(request.POST)

        text = request.POST.get('prompt', '')
        thesaurus = request.POST.get('thesaurus', '')

        if(thesaurus == 'synonym'):    
            synonyms = Language.objects.get(text=text).synonyms.all().values('text')
            return  JsonResponse({'synonyms': list(synonyms),})

        
        elif(thesaurus == 'antonym'):   
            antonyms = Language.objects.get(text=text).antonyms.all().values('text')
            return  JsonResponse({'antonyms': list(antonyms),})

        elif(thesaurus == 'translation'):   
            translations = Language.objects.get(text=text).translations.all().values('text')
            return  JsonResponse({'translations': list(translations),})
        
    return render(request, 'dictionary/index.html') 

def add_thesaurus(request):
    if(request.method == 'POST'):
        # print(request.POST)
        text = request.POST.get('text', '')
        thesaurus = request.POST.get('thesaurus', '')

        synonyms = [request.POST.get('Synonym_1', '') ,  request.POST.get('Synonym_2', ''),  request.POST.get('Synonym_3', '')]
        antonyms = [request.POST.get('Antonym_1', '') ,  request.POST.get('Antonym_2', ''),  request.POST.get('Antonym_3', '')]

        # print(text)
        # print(thesaurus)
        # print(synonyms)

        if(text != ''):
            # need to specify language
            prompt = Language.objects.get(text=text)
            # print(type(prompt), ':', prompt)
            
            if(thesaurus == 'synonym'):    
                for synonym in synonyms:
                    if(synonym != ''):
                        prompt.synonyms.get_or_create(text=synonym, language=prompt.language)

            elif(thesaurus == 'antonym'):   
                for antonym in antonyms:
                    if(antonym != ''):
                        prompt.antonyms.get_or_create(text=antonym, language=prompt.language)

        # elif(thesaurus == 'translation'):   
        #     translations = Language.objects.get(text=text).translations.all().values('text')
        #     return  JsonResponse({'translations': list(translations),})
        
    return render(request, 'dictionary/index.html') 

    
def translate(request):
    try:
        match = request.GET["Text"]
        LanguageText = eval(request.GET["Language1"] +"Text")
        text, created  = LanguageText.objects.get_or_create(text=match)
        context = {
            'prompt': text,
        }

        if(created):
            return render(request, 'dictionary/index.html', context)
        else:
            context = {
                'match': match,   
                'translation': text,
            }
            return render(request, 'dictionary/translate.html', context)
    except Exception as e:
        # print(e)
        return render(request, 'dictionary/translate.html')

def download_corpus(request):
    pass

