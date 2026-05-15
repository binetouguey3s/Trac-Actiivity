from django.urls import path
from .views import (
    InscriptionView, ConnexionView, DeconnexionView, TableauDeBordView,
    DetailEntreeView, CreerEntreeView, ModifierEntreeView, SupprimerEntreeView, ThematiquesView, SupprimerCategorieView
)

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', DeconnexionView.as_view(), name='deconnexion'),
    path('tableau-de-bord/', TableauDeBordView.as_view(), name='tableau-de-bord'),

    # entrees CRUD
    path('entree/creer/', CreerEntreeView.as_view(), name='entree-creer'),
    path('entree/<int:pk>/modifier/', ModifierEntreeView.as_view(), name='entree-modifier'),
    path('entree/<int:pk>/supprimer/', SupprimerEntreeView.as_view(), name='entree-supprimer'),
    path('entree/<int:pk>/', DetailEntreeView.as_view(), name='entree-detail'),

    # thematiques CRUD
    path('thematiques/', ThematiquesView.as_view(), name='thematiques'),
    path('categorie/<int:pk>/supprimer/', SupprimerCategorieView.as_view(), name='thematique-supprimer'),
]
