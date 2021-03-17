from django.shortcuts import render
from corpus.models import chunk, tokenize

def chunk_view(request):
    if(request.method=='POST'):
        n = int(request.POST.get('n-gram', 0))  
        text = request.POST.get('text_to_chunk', '').strip()
        print(text)
        language = request.POST.get('language', '')
        
        return chunk(text, n, language)

    return render(request, 'chunk_text/chunk.html')

def tokenize_view(request):
    if(request.method=='POST'):
        text = request.POST.get('text_to_tokenize', '')
        splitter = request.POST.get('splitter', '') +' '
        return tokenize(text, splitter)
        
    return render(request, 'chunk_text/tokenize.html')


def index(request):
    if(request.method=='POST'):
        n = int(request.POST.get('n-gram', 0))  
        text = request.POST.get('text_to_chunk', '')
        language = request.POST.get('language', '')
        return chunk(text, n, language)

    return render(request, 'chunk_text/index.html')