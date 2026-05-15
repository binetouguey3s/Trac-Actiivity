from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Modèle de catégorie (thématique)
class Category(models.Model):
    nom = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Thematique"
        verbose_name_plural = "Thematiques"
        ordering = ['-date_creation']

    def __str__(self):
        return self.nom

# Modèle d'entrée  
class Entry(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE , related_name='entries')
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE , related_name='entries')
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    image_preuve = models.ImageField(upload_to='preuves/', blank=True, null=True)

    class Meta:
        verbose_name = "Entree"
        verbose_name_plural = "Entrees"
        ordering = ['-date_publication']

    def __str__(self):
        return f"{self.titre} par {self.auteur.username}"   
        

        
