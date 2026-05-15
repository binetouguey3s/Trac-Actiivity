from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Entry, Category

# Formulaire d'inscription 
class FormulaireInscription(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Adresse email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}) 

# Formulaire pour la création et la modification des entrées
class FormulaireEntree(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['titre', 'categorie', 'image_preuve', 'contenu']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'entrée'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu de l\'entrée'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'image_preuve': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }     
        # labels pour les champs du formulaire
        labels = {
            'titre': 'Titre',   
            'categorie': 'Catégorie',
            'image_preuve': 'Image de preuve',
            'contenu': 'Contenu',
        }

# Formulaire pour la création et la modification des thématiques
class FormulaireCategorie(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la thematique'}),
        }
        labels = {
            'nom': 'Nom de la thematique',
        }           

