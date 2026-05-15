from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Entry


class CoreViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='secret12345')
        self.category = Category.objects.create(nom='Bug')
        self.other_category = Category.objects.create(nom='Documentation')
        self.entry = Entry.objects.create(
            auteur=self.user,
            categorie=self.category,
            titre='Correction formulaire',
            contenu='Le formulaire ne renvoyait aucune reponse en cas d erreur.',
        )
        self.client.login(username='alice', password='secret12345')

    def test_dashboard_filters_entries_and_sets_expected_context(self):
        response = self.client.get(reverse('tableau-de-bord'), {'categorie': self.category.pk})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.titre)
        self.assertEqual(response.context['total_entrees'], 1)
        self.assertEqual(response.context['entrees_mois'], 1)
        self.assertEqual(response.context['nb_categories'], 1)

    def test_thematiques_page_renders_without_category_pk(self):
        response = self.client.get(reverse('thematiques'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.nom)

    def test_logout_redirects_to_login_page(self):
        response = self.client.get(reverse('deconnexion'))

        self.assertRedirects(response, reverse('connexion'))

    def test_signup_invalid_form_exposes_formulaire_context(self):
        self.client.logout()

        response = self.client.post(reverse('inscription'), data={})

        self.assertEqual(response.status_code, 200)
        self.assertIn('formulaire', response.context)
        self.assertContains(response, 'Ce champ est obligatoire.')

    def test_create_entry_invalid_form_renders_errors(self):
        response = self.client.post(reverse('entree-creer'), data={})

        self.assertEqual(response.status_code, 200)
        self.assertIn('formulaire', response.context)
        self.assertContains(response, 'Erreur lors de la creation')

    def test_used_category_cannot_be_deleted(self):
        response = self.client.post(reverse('thematique-supprimer', args=[self.category.pk]))

        self.assertRedirects(response, reverse('thematiques'))
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())

    def test_unused_category_can_be_deleted(self):
        response = self.client.post(reverse('thematique-supprimer', args=[self.other_category.pk]))

        self.assertRedirects(response, reverse('thematiques'))
        self.assertFalse(Category.objects.filter(pk=self.other_category.pk).exists())
