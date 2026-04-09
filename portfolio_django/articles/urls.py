from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='articles', permanent=False), name='articles_home'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('publications/', views.PublicationsView.as_view(), name='publications'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('favourites/', views.FavouritesView.as_view(), name='favourites'),
    path('publish/', views.PublishView.as_view(), name='publish'),
    path('add-favourite/', views.AddFavouriteView.as_view(), name='add_favourite'),
]