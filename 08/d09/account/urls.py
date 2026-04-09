from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_view, name='account'),
    path('login/', views.ajax_login, name='ajax_login'),
    path('logout/', views.ajax_logout, name='ajax_logout'),
]
