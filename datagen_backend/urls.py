"""
URL configuration for datagen_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import path, include
from django.contrib import admin

from datagen_backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/', include('datasets.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""

# Hablar con escuelas de profesores de autoescuelas fuera

y ofrecer puestos de trabajo con casa subvenciada.

# Montar nuestro FP

alumno FP -> profesor autoescuela -> Profesor FP



"""