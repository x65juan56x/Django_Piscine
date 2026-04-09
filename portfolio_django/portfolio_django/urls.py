from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from .views import index

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('articles/', include('articles.urls')),
    path('tips/', include('tips.urls')),
    path('chat/', include('chat.urls')),
    path('account/', include('account.urls')),
)
