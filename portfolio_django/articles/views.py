from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Article, UserFavouriteArticle

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

class PublicationsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/publications.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

class FavouritesView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = 'articles/favourites.html'
    context_object_name = 'favourites'

    def get_queryset(self):
        return UserFavouriteArticle.objects.filter(user=self.request.user)


class PublishView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'synopsis', 'content']
    template_name = 'articles/publish.html'
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AddFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = ['article']
    success_url = reverse_lazy('favourites')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if UserFavouriteArticle.objects.filter(user=self.request.user, article=form.cleaned_data['article']).exists():
            return redirect('favourites')
        return super().form_valid(form)
