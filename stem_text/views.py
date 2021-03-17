from django.shortcuts import render
from django.http import JsonResponse 
from corpus.models import xhosa_stemmer
import nltk
# nltk.download('wordnet')
from nltk.stem.snowball import SnowballStemmer
from sentence_parser.models import Stem
from corpus.models import Language

# Create your views here.
def index(request):
    if(request.method =='POST'):
        print(request.POST)
        vote = request.POST.get('vote', '')
        if(vote != ''):

            prompt = request.POST.get('prompt', '')
            stem = Stem.objects.get(text=Language.objects.filter(text=prompt)[0])
            if(vote == 'Yes'):
                stem.is_stemmed_correctly_num_votes += 1
            elif(vote == 'Not'):
                stem.is_not_stemmed_correctly_num_votes += 1
            elif(vote == 'Not Sure'):
                stem.stemmed_correctly_not_sure_num_votes += 1
            context = {
                'response': 'thank you for voting'
            }
            stem.save()

            return JsonResponse(context)

        text = request.POST.get('text_to_stem', '').lower().strip()
        language = request.POST.get('language', '')
        lemma = text
        context = {}
        if(text == ''):
            context['response'] = 'Please enter a word'
        elif(language == ''):
            context['response'] = 'please specify language and try again'
        elif(language == 'English'):
            englishStemmer = SnowballStemmer("english")
            lemma = englishStemmer.stem(text)

            print(lemma)

        elif(language == 'IsiXhosa'):
            lemma = xhosa_stemmer(text)
        context['result'] = lemma
        context['text'] = text

        print(text)
        
        text = Language.objects.get_or_create(text=text, language=language)

        print(text)
        
        if(len(text) > 0):          
            stem, created = Stem.objects.get_or_create(
                text = text[0],
                stem = lemma
            )
        return JsonResponse(context)

    return render(request, 'stem_text/stem.html')

# def stem_vote

# def stem_word(request):
#     if(request.method =='POST'):
#         text = request.POST.get('text_to_stem', '').lower().strip()
#         language = request.POST.get('language', '')
#         lemma = text
#         context = {}
#         if(text == ''):
#             context['response'] = 'Please enter a word'
#         elif(language == ''):
#             context['response'] = 'please specify language and try again'
#         elif(language == 'English'):
#             lemmatizer = WordNetLemmatizer()
#             lemma = lemmatizer.lemmatize(text)
#         elif(language == 'IsiXhosa'):
#             lemmatizer = WordNetLemmatizer()
#             lemma = lemmatizer.lemmatize(text)
        
#         context['result'] = lemma
#         context['text'] = text
        
#         return render(request, 'stem_text/stem.html', context)
#     return render(request, 'stem_text/stem.html')
