from django.contrib import admin
from .models import ( 
    Language, LanguageMetadata, SignMetadata, SpeechMetadata, Conjugation, Index
)

# Register your models here.
class LanguageMetadataInline(admin.StackedInline):
    model = LanguageMetadata
    extra = 0

class SignMetadataInline(admin.StackedInline):
    model = SignMetadata
    extra = 0

class SpeechMetadataInline(admin.StackedInline):
    model = SpeechMetadata
    extra = 0

class ConjugationAdmin(admin.ModelAdmin):
    list_display = ('base_form', 'past_simple', 'past_participle', 'third_person_singular', 'present_participle')

class LanguageAdmin(admin.ModelAdmin):
    inlines = [LanguageMetadataInline,  SpeechMetadataInline, SignMetadataInline]
    list_display = ('text', 'language', 'single_word')
        
    fieldsets = (
        (None, {'fields': ('text', 'language', 'num_searches', 'single_word')}),
        ('Thesaurus and Translation', {'fields': ('synonyms', 'antonyms', 'translations')}),
        # ('Conjugations', {'fields': ('base_form', 'past_simple',)}),
        ('Pronounciation votes', {'fields': (
            'pronounciation_is_easy_num_votes',
            'pronounciation_is_average_num_votes', 
            'pronounciation_is_difficult_num_votes', 
            'pronounciation_not_sure_num_votes',
        )}),
        ('Heteronym votes (word pronounced multiple ways)', {'fields': (
            'is_heteronym_num_votes', 
            'is_not_heteronym_num_votes',
            'heteronym_not_sure_num_votes',
        )}),
        ('Sign votes', {'fields': (
            'sign_is_easy_num_votes',
            'sign_is_average_num_votes', 
            'sign_is_difficult_num_votes', 
            'sign_not_sure_num_votes',
        )}),
        ('Signed multiple ways (heteronym) votes', {'fields': (
            'is_heteronym_sign_num_votes', 
            'is_not_heteronym_sign_num_votes',
            'heteronym_sign_not_sure_num_votes',
        )}),
    )

class TextAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'text', 'definition', 'usage', 'part_of_speech')

class SpeechAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'text', 'pronounciation_is_accurate_num_votes', 'pronounciation_is_not_accurate_num_votes', 'pronounciation_accuracy_not_sure_num_votes')
    
class SignAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'text', 'sign_is_accurate_num_votes', 'sign_is_not_accurate_num_votes', 'sign_accuracy_not_sure_num_votes')

admin.site.register(Language, LanguageAdmin)
admin.site.register(Conjugation, ConjugationAdmin)

admin.site.register(LanguageMetadata, TextAdmin)
admin.site.register(SpeechMetadata, SpeechAdmin)
admin.site.register(SignMetadata, SignAdmin)

admin.site.register(Index)
