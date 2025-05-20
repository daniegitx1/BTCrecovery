"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scanner.urls')),  # 👈 Removes the /scanner/ prefix

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Expose dd-lists and derivationpath-lists CORRECTLY
urlpatterns += static('/dd-lists/', document_root=os.path.join(settings.BASE_DIR, 'btcrecover', 'dd-lists'))
urlpatterns += static('/derivationpath-lists/', document_root=os.path.join(settings.BASE_DIR, 'derivationpath-lists'))