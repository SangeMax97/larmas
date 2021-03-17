from django.test import TestCase

# Create your tests here.


# from corpus.models import Language, LanguageMetadata, SpeechMetadata, SignMetadata

# xh = []
# en = []

# x = None
# with open('/Users/sange/Work/IsiXhosa.txt') as f:
#     x = f.read().replace('\n', ' ').replace('  ', ' ').split()
#     x = set(x)  
#     x = list(x).sort()

# y = None
# with open('/Users/sange/Work/English.txt') as f:
#     y = f.read().replace('\n', ' ').replace('  ', ' ').split()
#     y = set(y)  
#     y = list(y).sort()

# for i in range(len(x)):
#     prompt = Language.objects.create(text = x[i], language = 'IsiXhosa', single_word=True)

# for i in range(len(y)):
#     prompt = Language.objects.create(text = y[i], language = 'English', single_word=True)

# x = None
# with open('/Users/sange/Work/IsiXhosa.txt') as f:
#     x = f.readlines()
# y = None
# with open('/Users/sange/Work//English.txt') as f:
#     y = f.readlines()

# for i in range(len(x)):
#     prompt = Language.objects.create(text = x[i], language = 'IsiXhosa')
#     prompt.translations.get_or_create(text=y[i], language='English')

# print('SUCCESS')

def splitLst(x):
        dictionary = dict()
        for word in x:
                f = word[0]
                if f in dictionary.keys():
                        dictionary[f].append(word)
                else:
                        dictionary[f] = [word]
                return dictionary

for ll in ['IsiXhosa', 'English']:
        x = None
        with open('/Users/sange/Work/'+ll+'.txt', 'r') as f:
                x = f.read().replace('\n', ' ').replace('  ', ' ').replace('.', '').replace(',', '').replace('\u0097','')
                x = x.replace('?', '').replace(':', '').replace(';', '')
                x = x.replace('(', '').replace(')', '')
                x = x.lower().split()
                x = set(x)  
                x = list(x)
                x.sort(reverse=True)
        dictionary = dict()
        for i in range(len(x)):
                prompt = Language.objects.create(text = x[i], language = ll, single_word=True)
                prompt_id = prompt.id
                word = x[i]
                f = word[0]
                if f in dictionary.keys():
                        dictionary[f].append(prompt_id)
                else:
                        dictionary[f] = [prompt_id]
        open('/Users/sange/Work/'+ll+'_index.json', 'w+').write(json.dumps(dictionary))
        

x = splitLst(x)
index = 0
for key, value in x.items():

        start = index
        index += len(value)

        print(key)
        print(start)
        print(index)
        print()

        index_ = Index.objects.create(
        language = ll,
        index=key,
        start=start,
        end=index
        )
        
