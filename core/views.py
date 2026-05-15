from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from .forms import FormulaireCategorie, FormulaireEntree, FormulaireInscription
from .models import Category, Entry


class InscriptionView(CreateView):
    form_class = FormulaireInscription
    template_name = 'inscription.html'
    success_url = reverse_lazy('connexion')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tableau-de-bord')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Inscription reussie. Vous pouvez maintenant vous connecter.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulaire'] = context['form']
        return context


class ConnexionView(LoginView):
    template_name = 'connexion.html'
    next_page = 'tableau-de-bord'


class DeconnexionView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Vous avez été déconnecté.")
        return redirect('connexion')



class TableauDeBordView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'connexion'
    model = Entry
    template_name = 'tableau_de_bord.html'
    context_object_name = 'entrees'
    paginate_by = 3

    def test_func(self):
        return self.request.user.is_authenticated
    # get_queryset pour filtrer les entrées en fonction de la catégorie et de l'auteur sélectionnés dans les filtres du tableau de bord
    def get_queryset(self):
        queryset = Entry.objects.filter(auteur=self.request.user)
        categorie_filtree = self.request.GET.get('categorie')
        auteur_filtree = self.request.GET.get('auteur')
        if categorie_filtree:
            queryset = queryset.filter(categorie_id=categorie_filtree)
        if auteur_filtree:
            queryset = queryset.filter(auteur_id=auteur_filtree)
        return queryset.order_by('-date_publication')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        toutes_entrees = Entry.objects.filter(auteur=self.request.user)
        entrees_ce_mois = toutes_entrees.filter(
            date_publication__year=timezone.now().year,
            date_publication__month=timezone.now().month,
        )
        categories = (
            Category.objects.annotate(nb_entrees=Count('entries'))
            .filter(entries__auteur=self.request.user)
            .distinct()
        )
        context['categories'] = categories
        context['total_entrees'] = toutes_entrees.count()
        context['entrees_mois'] = entrees_ce_mois.count()
        context['nb_categories'] = categories.count()
        context['categorie_active'] = self.request.GET.get('categorie')
        context['auteur_active'] = self.request.GET.get('auteur')
        context['afficher_pagination'] = context['paginator'].count >= self.paginate_by
        return context


class DetailEntreeView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = '/connexion/'
    model = Entry
    template_name = 'detail_entree.html'
    context_object_name = 'entree'

    def test_func(self):
        entree = self.get_object()
        return entree.auteur == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Vous ne pouvez pas voir l'entree d'un autre utilisateur.")
        return redirect('tableau-de-bord')


class CreerEntreeView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = '/connexion/'
    model = Entry
    form_class = FormulaireEntree
    template_name = 'creer_entree.html'
    success_url = reverse_lazy('tableau-de-bord')

    def test_func(self):
        return self.request.user.is_authenticated

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        messages.success(self.request, "Entree creee avec succes !")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulaire'] = context['form']
        return context


class ModifierEntreeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/connexion/'
    model = Entry
    form_class = FormulaireEntree
    template_name = 'modifier_entree.html'

    def test_func(self):
        entree = self.get_object()
        return entree.auteur == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Vous ne pouvez pas modifier l'entree d'un autre utilisateur.")
        return redirect('tableau-de-bord')

    def get_success_url(self):
        return reverse_lazy('entree-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Entree modifiee avec succes !")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulaire'] = context['form']
        context['entree'] = self.object
        return context


class SupprimerEntreeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/connexion/'
    model = Entry
    template_name = 'supprimer_entree.html'
    success_url = reverse_lazy('tableau-de-bord')

    # Seule l'auteur de l'entrée peut la supprimer
    def test_func(self):
        entree = get_object_or_404(Entry, pk=self.kwargs['pk'])
        return entree.auteur == self.request.user
    # Si l'utilisateur n'est pas autorisé, on affiche un message d'erreur et on le redirige vers le tableau de bord
    def handle_no_permission(self):
        messages.error(self.request, "Vous ne pouvez pas supprimer l'entree d'un autre utilisateur.")
        return redirect('tableau-de-bord')

    def post(self, request, pk):
        entree = get_object_or_404(Entry, pk=pk, auteur=request.user)
        entree.delete()
        messages.success(request, "Entree supprimee.")
        return redirect('tableau-de-bord')


class ThematiquesView(LoginRequiredMixin,UserPassesTestMixin, TemplateView):
    login_url = '/connexion/'
    template_name = 'thematiques.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(nb_entrees=Count('entries'))
        context['categories'] = categories
        context['formulaire'] = context.get('formulaire', FormulaireCategorie())
        return context

    def post(self, request):
        formulaire = FormulaireCategorie(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, "Thematique ajoutee !")
            return redirect('thematiques')

        context = self.get_context_data()
        context['formulaire'] = formulaire
        context['erreur'] = formulaire.errors.get('nom', ["Nom de thematique invalide."])[0]
        return render(request, self.template_name, context)

# l'utilisateur simple ne peut pas supprimer aucune thematique , meme celles qui ne sont pas utilisées par des entrées, pour éviter les problèmes de gestion des catégories, seul un administrateur peut supprimer une thematique, et même lui ne peut pas supprimer une thematique utilisée par des entrées

class SupprimerCategorieView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Category
    login_url = '/connexion/'
    success_url = reverse_lazy('thematiques')

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, "Impossible de supprimer une thematique utilisee par des entrees ou qui n'est pas la votre.")
        return redirect('thematiques')
    
    def post(self, request, pk):
        categorie = get_object_or_404(Category, pk=pk)
        if categorie.entries.exists():
            messages.error(request, "Impossible de supprimer une thematique utilisee par des entrees.")
            return redirect('thematiques')

        categorie.delete()
        messages.success(request, "Thematique supprimee.")
        return redirect('thematiques')
