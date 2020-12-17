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
from django.contrib import admin
from django.urls import include, path

from video_content.views import upload_video, display

from django.conf.urls.static import static
from django.conf import settings
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include([
        path('', views.index, name='index'),
        path('start', views.start, name='start'),
        path('zeitstrahl', views.zeitstrahl, name='zeitstrahl'),
        path('themengrid', views.themengrid, name='themengrid'),
        path('t', views.t, name='t'),
    ])),
    # For later use´in the admin interface
    # path('upload/', upload_video, name='upload'),
    # path('videos/', display, name='videos'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
