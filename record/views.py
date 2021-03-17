from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.

from corpus.models import Language, SpeechMetadata, SignMetadata

import json
 
def record(request):
    return render(request, 'record/index.html')
    
def audio_video(request):
    print("DEBUG audio_video container")
    if request.method == 'POST':
        audio_video = request.FILES.get('player', '')
        handle_uploaded_file(audio_video)     
    else:
        print("FAIL audio_video container")
    return render(request, 'record/audio-video-container.html')

def audio_container(request):
    print("DEBUG audio container")
    if request.method == 'POST':
        print(request.POST)
        text          = request.POST.get('text', '')
        language      = request.POST.get('language', '')
        name          = request.POST.get('name', '')
        timestamps    = request.POST.get('timestamps', '')
        audio         = request.FILES.get('audio_player', '')
        file_type     = request.POST.get('type', '/').split('/')[0]
        size          = request.POST.get('size', '')
        created       = request.POST.get('created', '')
        
        print(language)
        if(text==""): path = os.path.join('static/media', file_type, 'not_labled')
        else: path = os.path.join('static/media', file_type, text)
        
        file_saved = handle_uploaded_file(audio, path, name)

        open(os.path.join(path, name[:-4]+'json'), 'w+').write(timestamps)

        if(file_saved and text !=""):
            if(language == ""):
                prompt, created = Language.objects.get_or_create(text=text)
            else:
                prompt, created = Language.objects.get_or_create(
                    text= text,
                    language = language
                )
            
            speech = SpeechMetadata(
                text = prompt,
                audio = os.path.join(path, name),
                timestamps = os.path.join(path, name[:-4]+'json'),
                user = request.user
            ).save()
    else:
        print("FAIL audio container")
    return render(request, 'record/audio-container.html')

def video_container(request):
    print("DEBUG video_container container")
    if request.method == 'POST':
        print()
        print(request.POST)
        print()
        text          = request.POST.get('text', '')
        language      = request.POST.get('language', '')
        name          = request.POST.get('name', '')
        video         = request.FILES.get('video_player', '')
        file_type     = request.POST.get('type', '/').split('/')[0]
        size          = request.POST.get('size', '')
        created       = request.POST.get('created', '')
        
        if(text==""): path = os.path.join('static','media', file_type, 'not_labled')
        else: path = os.path.join('static','media', file_type, text)
        
        file_saved = handle_uploaded_file(video, path, name)

        if(file_saved and text !=""):
            if(language == ""):
                prompt, created = Language.objects.get_or_create(text=text)
            else:
                prompt, created = Language.objects.get_or_create(
                    text= text,
                    language = language
                )
            
            SignMetadata(
                text = prompt,
                video = os.path.join(path, name),
                user = request.user
            ).save()        
    else:
        print("FAIL video_container container")
    return render(request, 'record/video-container.html')

# Function to handle an uploaded file.

import os

def handle_uploaded_file(f, path, name):


    if(f !=''):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    return False




# metadata = LanguageMetadata(
#     text = prompt,
#     definition = meta['definition'],
#     usage = meta['example'],
#     part_of_speech = pos
# )
# metadata.save()


# print('text:', text)
# print('language:',language)
# print()
# print('file_saved:', file_saved)
# print('f:', f)