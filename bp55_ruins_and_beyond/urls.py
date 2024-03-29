"""bp55_ruins_and_beyond URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# pylint: disable = import-error
import cas.views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('start/', include('start.urls')),
    path('videos/', include('video_content.urls')),
    path('filter/', include('filter_page.urls')),
    path('details_page/', include('details_page.urls')),
    path('timeline/', include('timeline.urls')),
    path('search/', include('search.urls')),
    path('materials_page/', include('materials_page.urls')),
    path('impressum/', include('impressum.urls')),
    path('analytics/', include('analytics.urls')),
    # CAS SSO TU-Darmstadt:
    path('login/', cas.views.login, name='login'),
    path('logout/', cas.views.logout, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
