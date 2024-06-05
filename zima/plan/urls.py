from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views
from .views import MyLoginView


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('zima/', views.run_exe_zima),
    path('zima_download/', views.download_and_cache_zima_app),
    ]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    # urlpatterns += static(settings.MEDIA_URL,
    #                       document_root=settings.MEDIA_ROOT)


