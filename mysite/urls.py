"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from app.views import index, detail,ajoutPannier,pannier,recherche,deletePannier
from django.conf.urls.static import static
from mysite import settings
from users.views import seConnecter,logout_user,login_user


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('seConnecter/',seConnecter,name = "seConnecter"),
    path('login/',login_user,name="login"),  
    path('logout/',logout_user,name="logout"), 
    path('pannier/',pannier,name="pannier"),  
    path('pannier/delete',deletePannier,name="deletePannier"),
    path('produit/<str:slug>/', detail, name="produit"),
    path('produit/<str:slug>/ajoutPannier', ajoutPannier, name="ajoutPannier"),
    path('recherche/', recherche,name="recherche"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
