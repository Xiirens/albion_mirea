"""
URL configuration for webalb project.

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.views.static import serve

from django.contrib import admin
from django.urls import path
from first.views import first_page, login_page

urlpatterns = [
    path('static/<path:path>', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('login/', login_page),
    path('', first_page)
    
]

handler404 = "webalb.views.page_not_found_view"
