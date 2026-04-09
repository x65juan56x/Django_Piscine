from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.account_view, name='account'),
    path('ajax_login/', views.ajax_login, name='ajax_login'),
    path('ajax_logout/', views.ajax_logout, name='ajax_logout'),
    path('login/', auth_views.LoginView.as_view(template_name='account/index.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),
]
