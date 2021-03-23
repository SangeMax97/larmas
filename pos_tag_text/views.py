from django.shortcuts import render
from corpus.models import Language, LanguageMetadata
from django.http import JsonResponse
from collections import defaultdict

# Create your views here.
def index(request):
    if(request.method == 'POST'):
      
        language = request.POST.get('language', '')
        text = request.POST.get('text', '').lower().split()

        tagged = {}

        x = Language.objects.filter(text__in = text)
        
        for i in x:
            try:    
                y = '<div class="tag-label tagged '+ i.text_metadata.first().part_of_speech + '">' + i.text + ' <div class="badge badge-light">' + i.text_metadata.first().part_of_speech + '</div></div>'
            except:
                y = '<div class="tag-label">' + i.text + '</div>'

            tagged[i.text] = y

        for i in range(len(text)):
            try:
                text[i] = tagged[text[i]]
            except:
                text[i] = '<div class="tag-label">' + text[i] + '</div>'
                
        context = {'response': text}
        
        return JsonResponse(context)
        
    return render(request, 'pos_tag_text/pos_tag.html')