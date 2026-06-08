# Trac-Activity 

Système de traçabilité d'activité en ligne permettant aux utilisateurs de créer, modifier et supprimer des entrées d'activité avec catégorisation par thématiques.

##  Fonctionnalités

- **Authentification** : Inscription et connexion sécurisées
- **Dashboard** : Vue d'ensemble de toutes vos activités
- **Gestion des entrées** : Créer, modifier et supprimer des activités
- **Catégorisation** : Organisation par thématiques
- **Preuves jointes** : Possibilité d'ajouter des images/photos en tant que preuves
- **Pagination** : Navigation facile entre les entrées

##  Stack Technique

- **Backend** : Django (Python)
- **Frontend** : HTML5, CSS, Bootstrap
- **Base de données** : MySQL
- **Gestion des fichiers** : Support des uploads d'images

##  Installation

```bash
# 1. Cloner le projet
git clone https://github.com/binetouguey3s/Trac-Actiivity.git
cd Trac-Actiivity

# 2. Créer un environnement virtuel
# venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Lancer le serveur
python manage.py runserver
```

Accédez à l'application sur `http://localhost:8000`

##  Structure du Projet

```
Trac-Actiivity/
├── config/              # Configuration Django
├── core/                # Application principale
│   ├── migrations/      # Migrations de base de données
│   ├── templates/       # Templates HTML
    ├   - `connexion.html` → Page de login
        - `inscription.html` → Création de compte
        - `tableau_de_bord.html` → Dashboard paginé des logs
        - `creer_entree.html` → Formulaire de création
        - `modifier_entree.html` → Modification (auteur uniquement)
        - `supprimer_entree.html` → Confirmation de suppression
        - `detail_entree.html` → Détail du log + image de preuve
        - `thematiques.html` → Gestion des thématiques
│   └── models.py        # Modèles de données
├── media/               # Fichiers uploadés
├── templates/           # Templates globaux
├   - `base.html         # base.htmlTemplate parent (navbar, footer, structure commune)
├── manage.py            # Gestionnaire Django
└── requirements.txt     # Dépendances
```

##  Auteur

- **binetouguey3s**


