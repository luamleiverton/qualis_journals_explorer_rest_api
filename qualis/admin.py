from django.contrib import admin
from qualis.models import Journals

class List_Journals(admin.ModelAdmin):
    list_display = ('id','issn','journal','qualis')
    list_display_links = ('id','issn')
    search_fields = ('issn', 'journal')
    list_editable = ('qualis',)
    ordering = ('journal',)

admin.site.register(Journals, List_Journals)