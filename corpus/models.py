from django.db import models
from django.http import JsonResponse, HttpResponse
from user.models import User

import re
import json
import requests
from collections import defaultdict

from bs4 import BeautifulSoup
# Create your models here.

# Corpus Parent Class _____________________________________________________

class Index(models.Model):
    language_choices = (
        ('English','English'),  ('Sesotho','Sesotho'),  ('IsiXhosa','IsiXhosa')
    )
    language = models.CharField(blank=True, max_length=15, choices=language_choices, null=True, default='')

    index_choices = (
        ('a','a'),  ('b','b'),  ('c','c'), ('d','d'),  ('e','e'),  ('f','f'),
        ('g','g'),  ('h','h'),  ('i','i'), ('j','j'),  ('k','k'),  ('l','l'),
        ('m','m'),  ('n','n'),  ('o','o'), ('p','p'),  ('q','q'),  ('r','r'),
        ('s','s'),  ('t','t'),  ('u','u'), ('v','v'),  ('w','w'),  ('x','x'),
        ('y','y'),  ('z','z')
    )
    index = models.CharField(blank=True, max_length=2, choices=index_choices, null=True, default='')
    start = models.IntegerField(blank=True, default=0)   
    end = models.IntegerField(blank=True, default=0)   

    class Meta:
        verbose_name = 'Index'
        verbose_name_plural = 'Indices'

    def __str__(self):
        return self.index

class Language(models.Model):
    text         = models.TextField()
    synonyms     = models.ManyToManyField('self', blank=True)
    antonyms     = models.ManyToManyField('self', blank=True)
    translations = models.ManyToManyField('self', blank=True)

    # base_form   = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='base')
    # past_simple = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='past')
    
    language_choices = (
        ('English','English'),  ('Sesotho','Sesotho'),  ('IsiXhosa','IsiXhosa')
    )
    language = models.CharField(blank=True, max_length=15, choices=language_choices, null=True, default='')

    # other fields

    single_word = models.BooleanField(default=False)

    # TEXT
    num_searches = models.IntegerField(blank=True, default=0)   

    # SPEECH
    pronounciation_is_easy_num_votes      = models.IntegerField(blank=True, default=0)   
    pronounciation_is_average_num_votes   = models.IntegerField(blank=True, default=0)   
    pronounciation_is_difficult_num_votes = models.IntegerField(blank=True, default=0)   
    pronounciation_not_sure_num_votes     = models.IntegerField(blank=True, default=0)  

    is_heteronym_num_votes       = models.IntegerField(blank=True, default=0)   
    is_not_heteronym_num_votes   = models.IntegerField(blank=True, default=0)   
    heteronym_not_sure_num_votes = models.IntegerField(blank=True, default=0)  

    # SIGN
    sign_is_easy_num_votes      = models.IntegerField(blank=True, default=0)   
    sign_is_average_num_votes   = models.IntegerField(blank=True, default=0)   
    sign_is_difficult_num_votes = models.IntegerField(blank=True, default=0)   
    sign_not_sure_num_votes     = models.IntegerField(blank=True, default=0)  

    is_heteronym_sign_num_votes       = models.IntegerField(blank=True, default=0)   
    is_not_heteronym_sign_num_votes   = models.IntegerField(blank=True, default=0)   
    heteronym_sign_not_sure_num_votes = models.IntegerField(blank=True, default=0)  

    class Meta:
        verbose_name = 'All'
        verbose_name_plural = 'All'

    def __str__(self):
        return self.text

    def get_metadata(self):
        return self.text_metadata.all().first()
    
    def get_metadata_all(self):
        return self.text_metadata.all()
    
# Corpus Child Classes _____________________________________________________

# class English(Language):
#     class Meta:
#         verbose_name = 'English'
#         verbose_name_plural = 'English'

# class Sesotho(Language):
#     class Meta:
#         verbose_name = 'Sesotho'
#         verbose_name_plural = 'Sesotho'

# class IsiXhosa(Language):
#     class Meta:
#         verbose_name = 'IsiXhosa'
#         verbose_name_plural = 'IsiXhosa'

# Metadata Class _____________________________________________________
class LanguageMetadata(models.Model):
    text = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="text_metadata")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="text_user", blank=True, null=True) 
    # add more fields: synonyms, translations, antonyms, etc
    definition = models.TextField(null=True, blank=True)
    usage = models.TextField(null=True, blank=True)
    pos_choices = (
        ('verb', 'verb'), ('noun', 'noun'), ('adjective', 'adjective'),
        ('adverb', 'adverb'), ('pronoun', 'pronoun'), ('preposition', 'preposition'),
        ('conjunction', 'conjunction'), ('particle', 'particle'), ('article', 'article'),
        ('interjection', 'interjection'), ('exclamation', 'exclamation'), 
        ('possessive determiner', 'possessive determiner'),

    )
    part_of_speech = models.CharField(max_length=50, choices=pos_choices, null=True, blank=True)
    
    tense_choices = (('n/a', 'n/a'), ('past', 'past'), ('present', 'present'), ('future', 'future'))
    tense = models.CharField(max_length=50, choices=tense_choices, null=True, blank=True)
    
    # root = models.ForeignKey(Language, on_delete=models.CASCADE)
    # 
    def as_json(self):
        return {
            'definition' : self.definition,
            'usage' : self.usage,
        }

    class Meta:
        verbose_name = 'Text Metadata'
        verbose_name_plural = 'Text Metadata'
    
    def __str__(self):
        return 'Text Metadata: ' + self.text.text +', from '+ str(self.user)

class SpeechMetadata(models.Model):
    text  = models.ForeignKey(Language, on_delete=models.CASCADE)
    audio = models.FileField(null=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="speech_user", null=True)           

    translations    = models.ManyToManyField('self', blank=True)
   
    pronounciation_is_accurate_num_votes       = models.IntegerField(blank=True, default=0)   
    pronounciation_is_not_accurate_num_votes   = models.IntegerField(blank=True, default=0)   
    pronounciation_accuracy_not_sure_num_votes = models.IntegerField(blank=True, default=0) 

    audio_plays_num_votes = models.IntegerField(blank=True, default=0)  
    audio_represents_text_num_votes   = models.IntegerField(blank=True, default=0)  
    audio_clipped_num_votes   = models.IntegerField(blank=True, default=0)  
    audio_offensive_num_votes = models.IntegerField(blank=True, default=0)  

    text_offensive_num_votes  = models.IntegerField(blank=True, default=0)  
    text_spelling_errors_num_votes = models.IntegerField(blank=True, default=0)  
         
    class Meta:
        verbose_name = 'Speech Metadata'
        verbose_name_plural = 'Speech Metadata'

    def __str__(self):
        return 'Speech Metadata: ' + self.text.text +', from '+ str(self.user)

class SignMetadata(models.Model):
    text = models.ForeignKey(Language, on_delete=models.CASCADE)
    video = models.FileField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sign_user", null=True) 

    sign_is_accurate_num_votes       = models.IntegerField(blank=True, default=0)   
    sign_is_not_accurate_num_votes   = models.IntegerField(blank=True, default=0)   
    sign_accuracy_not_sure_num_votes = models.IntegerField(blank=True, default=0) 

    video_plays_num_votes = models.IntegerField(blank=True, default=0)  
    video_represents_text_num_votes   = models.IntegerField(blank=True, default=0)  
    video_clipped_num_votes   = models.IntegerField(blank=True, default=0)  
    video_offensive_num_votes = models.IntegerField(blank=True, default=0)  

    text_offensive_num_votes  = models.IntegerField(blank=True, default=0)  
    text_spelling_errors_num_votes = models.IntegerField(blank=True, default=0)  

    class Meta:
        verbose_name = 'Sign Metadata'
        verbose_name_plural = 'Sign Metadata'

    def __str__(self):
        return 'Sign Metadata: ' + self.text.text +', from '+ str(self.user)

class Conjugation(models.Model):
    base_form             = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, related_name='base')
    past_simple           = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, related_name='past_simple_form')
    past_participle       = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, related_name='past_singular_form')
    third_person_singular = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, related_name='third_person_singular_form')
    present_participle    = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, related_name='gerund')
    
    def __str__(self):
        return self.base_form.text

# Functions __________________________________________________________
def generate_search(text):
    return Language.objects.filter(text=text).first()

def generate_search_all(text):
    return Language.objects.filter(text=text)

from sentence_parser.models import NGram
def generate_ngrams(text, n, splitter=' ', language=''):
    # Convert to lowercases
    text = text.lower()

    # Replace all none alphanumeric characters with spaces
    if(splitter ==' '): text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Break sentence in the token, remove empty tokens
    tokens = [token for token in text.split(splitter) if token != ""]


    
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    context = []

    for ngram in ngrams:
        text = " ".join(ngram)
        context.append(text)

        if(n != 1):
            ngram, created = NGram.objects.get_or_create(text=text, language=language)
            
            if(created):
                text_l  = text.split(' ')
                ngram.n = len(text_l)
                ngram.frequency = 1
                
                if(len(text_l) == 2):
                    ngram.word_1 = Language.objects.get_or_create(text=text_l[0], language=ngram.language)[0]
                    ngram.word_2 = Language.objects.get_or_create(text=text_l[1], language=ngram.language)[0]
                    
                elif(len(text_l) == 3):
                    ngram.word_1 = Language.objects.get_or_create(text=text_l[0], language=ngram.language)[0]
                    ngram.word_2 = Language.objects.get_or_create(text=text_l[1], language=ngram.language)[0]
                    ngram.word_3 = Language.objects.get_or_create(text=text_l[2], language=ngram.language)[0]

                elif(len(text_l) == 4):
                    ngram.word_1 = Language.objects.get_or_create(text=text_l[0], language=ngram.language)[0]
                    ngram.word_2 = Language.objects.get_or_create(text=text_l[1], language=ngram.language)[0]
                    ngram.word_3 = Language.objects.get_or_create(text=text_l[2], language=ngram.language)[0]
                    ngram.word_4 = Language.objects.get_or_create(text=text_l[3], language=ngram.language)[0]

                elif(len(text_l) == 5):
                    ngram.word_1 = Language.objects.get_or_create(text=text_l[0], language=ngram.language)[0]
                    ngram.word_2 = Language.objects.get_or_create(text=text_l[1], language=ngram.language)[0]
                    ngram.word_3 = Language.objects.get_or_create(text=text_l[2], language=ngram.language)[0]
                    ngram.word_4 = Language.objects.get_or_create(text=text_l[3], language=ngram.language)[0]
                    ngram.word_5 = Language.objects.get_or_create(text=text_l[4], language=ngram.language)[0]
            else:
                ngram.frequency = ngram.frequency + 1
            ngram.save()
        else:
            if(len(text) != 1 and not text.isdigit()):
                x, created = Language.objects.get_or_create(text=text, language=language)
                    
    return context

def chunk(text, n, language):
    error = 0
    if(n == 0):
        meaning = 'choose a value for n'
        error = 1
    elif(text == ''):
        meaning = 'text is empty'
        error = 1
    else:
        meaning = generate_ngrams(text, n, language=language)

    context = {
        'chunk_result': meaning,
        'chunk_error': error
    }
    return JsonResponse(context)

def tokenize(text, splitter):
    error = 0
    if(text == ''):
        meaning = 'text is empty' 
        error = 1
    else:
        meaning = generate_ngrams(text, 1, splitter=splitter)
    context = {
        'tokenize_result': meaning,
        'tokenize_error': error
    }
    return JsonResponse(context)

def search(text, language):
    text = text.strip().lower()
    if(text == '' ):
        return HttpResponse('Please enter a word')

    all  = generate_search_all(text)
    near_matches = False
    if is_empty(all):
        if(language == ''):
            return HttpResponse('could not find '+ text+', please specify language and try again')

        all, near_matches = oxford_dict(text, language)
 
        
    if(len(all)==0):
        return HttpResponse('word not found')

    if(near_matches):
        return JsonResponse({'word': [text], 'near_matches': all})

    if(len(all)==1):
        meaning = defaultdict(list)
        result_json = defaultdict(list)

        for language in all:
            metadata = defaultdict(list)
            for meta in language.text_metadata.filter(text__text=language.text):
                key = meta.part_of_speech 
                value = meta.as_json()
                metadata[key].append(value)
            meaning[language.language].append(metadata)
        
        result_json['word'].append(text)
        result_json['meaning'].append(meaning)
        
        json_data = json.dumps(result_json, indent=2)
        context = json.loads(json_data)
                
        return JsonResponse(context)


def google_dict(text):
    url = f'https://googledictionaryapi.eu-gb.mybluemix.net/?define={text}&lang=en'
    response = requests.get(url)
    if(response.status_code == 404):
        return []
    else:
        context = eval(response.text)[0]
        prompt, created = Language.objects.get_or_create(
            text=context['word'],
            language = 'English'
        )
        meaning = context['meaning']
        for pos in meaning:
            meta = meaning[pos][0]
            metadata = LanguageMetadata(
                text = prompt,
                definition = meta['definition'],
                usage = meta['example'],
                part_of_speech = pos
                
            )
            metadata.save()
        return [prompt]


import numpy as np

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1]), seq2

def oxford_dict(text, language):
    urls = {
        'English': f'https://www.lexico.com/en/definition/{text}',
        'IsiXhosa': f'https://xh.oxforddictionaries.com/translate/isixhosa-english/{text}?locale=en',
        'Sesotho':  f'https://nso.oxforddictionaries.com/translate/northernsotho-english/{text}?locale=en'
    }

    url = urls[language]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text_element = soup.select('span.hw')

    

    if is_empty(text_element):

        prompts = Language.objects.filter(language=language).values('text')
        res = map(lambda x: x['text'], list(prompts))
        result = list(map(lambda x: x[1], filter(lambda x: x[0]<3,  [levenshtein(text, t) for t in res])))
        
        return sorted(result), True
    else:
        prompt, created = Language.objects.get_or_create(
            text= text,
            language = language
        )
        # ul = soup.select('ul.semb li')

        section = soup.select('section.gramb')

        for i in section:
            ul = i.select('ul.semb li')
            pos = i.select('span.pos')[0].get_text()
            for k in ul:
                if(language=='English'):
                    definitions = list(map(return_text, k.select('span.ind')))
                    usage       = list(map(return_text, k.select('div.ex em')))
                else:
                    definitions = list(map(return_text, k.select('div.tr span')))
                    usage       = list(map(return_text, k.select('div.ex em')))
                
                
                if(is_empty(definitions) and is_empty(usage)):
                    pass

                elif(is_empty(definitions)):
                    metadata = LanguageMetadata(
                        text = prompt,
                        usage = usage[0].strip('’ ‘'),
                        part_of_speech = pos
                    )
                    metadata.save()
                
                elif(is_empty(usage)):
                    metadata = LanguageMetadata(
                        text = prompt,
                        definition = definitions[0].strip(),
                        part_of_speech = pos
                    )
                    metadata.save()
                else:
                    metadata = LanguageMetadata(
                        text = prompt,
                        definition = definitions[0].strip(),
                        usage = usage[0].strip('’ ‘'),
                        part_of_speech = pos
                    )
                    metadata.save()         
        
        return [prompt], False

# used on a map function
def return_text(text):
    return text.get_text()

def handle_uploaded_file(name, f):
    if(f !=''):
        with open(name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

def is_empty(context):
    return len(context) == 0

def remove_prefix(word, prefixes):
    for prefix in prefixes:
        if(word.startswith(prefix)):
            return word.replace(prefix, '', 1)
    return word

def remove_suffix(word, suffixes):
    for suffix in suffixes:
        if(word.endswith(suffix)):
            return word.replace(suffix, '', 1)
    return word

def xhosa_stemmer(word):
    word = word.strip().lower()
    # Rule 1
    vowels = ['a', 'e', 'i', 'o', 'u' ]
    if(len(word) < 4):
        print(word + " is too short to be stemmed")
        if(word[0] in vowels):
            stem = word[1:]
            return stem

    # Rule 2
    type1_prefixes = ["asingo", "ayingo", "nga", "asi", "ku", "em", "en"]
    type1_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type1_prefixes)
    stem = remove_suffix(stem, type1_suffixes)
    if(stem != word): return stem

    # Rule 3
    type2_prefixes = ["um"]
    type2_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type2_prefixes)
    stem = remove_suffix(stem, type2_suffixes)
    if(stem != word): return stem

    # Rule 4
    type3_prefixes = ["aba", "abe" , "ab"]
    type3_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type3_prefixes)
    stem = remove_suffix(stem, type3_suffixes)
    if(stem != word): return stem

    # Rule 5
    type4_prefixes = ["u"]
    type4_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type4_prefixes)
    stem = remove_suffix(stem, type4_suffixes)
    if(stem != word): return stem

    # Rule 6
    type5_prefixes = ["oo"]
    type5_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type5_prefixes)
    stem = remove_suffix(stem, type5_suffixes)
    if(stem != word): return stem

    # Rule 7
    type6_prefixes = ["imi" , "im"]
    type6_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type6_prefixes)
    stem = remove_suffix(stem, type6_suffixes)
    if(stem != word): return stem

    # Rule 8
    type7_prefixes = ["ili"]
    type7_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type7_prefixes)
    stem = remove_suffix(stem, type7_suffixes)
    if(stem != word): return stem

    # Rule 9
    type8_prefixes = ["ama" , "ame"]
    type8_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type8_prefixes)
    stem = remove_suffix(stem, type8_suffixes)
    if(stem != word): return stem

    # Rule 10
    type9_prefixes = ["isi", "is"]
    type9_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type9_prefixes)
    stem = remove_suffix(stem, type9_suffixes)
    if(stem != word): return stem

    # Rule 11
    type10_prefixes = ["izi" , "iz"]
    type10_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type10_prefixes)
    stem = remove_suffix(stem, type10_suffixes)
    if(stem != word): return stem

    # Rule 12
    type11_prefixes = ["in" , "im" , "i"]
    type11_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type11_prefixes)
    stem = remove_suffix(stem, type11_suffixes)
    if(stem != word and stem[0] != 'i'): return stem

    # Rule 13
    type12_prefixes = ["izin" , "izim" , "ii" , "iin" ,"iim"]
    type12_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type12_prefixes)
    stem = remove_suffix(stem, type12_suffixes)
    if(stem != word): return stem

    # Rule 14
    type13_prefixes = ["ulu" , "ulw" , "ul"]
    type13_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type13_prefixes)
    stem = remove_suffix(stem, type13_suffixes)
    if(stem != word): return stem

    # Rule 15
    type14_prefixes = ["ubu" , "ub" , "utyw" , "uty"]
    type14_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type14_prefixes)
    stem = remove_suffix(stem, type14_suffixes)
    if(stem != word): return stem

    # Rule 16
    type15_prefixes = ["uku" , "uk" , "ukw"]
    type15_suffixes = ["ana", "kazi"]

    stem = remove_prefix(word, type15_prefixes)
    stem = remove_suffix(stem, type15_suffixes)
    return stem