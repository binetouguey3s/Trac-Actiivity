from django.contrib import admin
from .models import Category, Entry, Profile

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    search_fields = ('nom',)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'date_publication')
    search_fields = ('titre', 'contenu')
    list_filter = ('categorie', 'date_publication')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'photo')
    search_fields = ('utilisateur__username',)
