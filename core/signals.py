from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Entry

@receiver(post_save, sender=Entry)
def log_creation_entree(sender, instance, created, **kwargs):
    if created:
        print(f"Nouvelle entrée créée : {instance.titre}")
        print(f"Auteur : {instance.auteur.username}")
        print(f"Thématique : {instance.categorie.nom}")
        print(f"Image de preuve : {instance.image_preuve.url if instance.image_preuve else 'Aucune'}")
        print(f"Date : {instance.date_publication.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Entrée mise à jour : {instance.titre}")
        print(f"Auteur : {instance.auteur.username}")
        print(f"Modifie le : {instance.date_modification.strftime('%Y-%m-%d %H:%M:%S')}")

@receiver(post_delete, sender=Entry)
def log_deletion_entree(sender, instance, **kwargs):
    print(f"Entrée supprimée : {instance.titre}")
    print(f"Auteur : {instance.auteur.username}")