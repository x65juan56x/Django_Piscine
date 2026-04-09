from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('get-name/', views.get_current_name, name='get_name'),
    path('tip/<int:tip_id>/upvote/', views.upvote_tip, name='upvote_tip'),
    path('tip/<int:tip_id>/downvote/', views.downvote_tip, name='downvote_tip'),
    path('tip/<int:tip_id>/delete/', views.delete_tip, name='delete_tip'),
]
