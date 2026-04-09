from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='articles', permanent=False), name='home'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('login/', auth_views.LoginView.as_view(template_name='articles/login.html'), name='login'),
    path('publications/', views.PublicationsView.as_view(), name='publications'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('favourites/', views.FavouritesView.as_view(), name='favourites'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('publish/', views.PublishView.as_view(), name='publish'),
    path('add-favourite/', views.AddFavouriteView.as_view(), name='add_favourite'),
]