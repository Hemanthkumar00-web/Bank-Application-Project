"""
URL configuration for union project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from Bank.views import login,deposit,withdraw,transfer,check,viewtranscations,Register,features_page,logout_here,check_acc_number
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',login ,name="login"),
    path('deposit',deposit,name="deposit"),
    path('withdraw',withdraw,name="withdraw"),
    path('transfer',transfer,name="transfer"),
    path('check',check),
    path('viewtranscations',viewtranscations),
    path('Register',Register),
    path('features',features_page,name="feature"),
    path('logout',logout_here,name='logout_here'),
    path('holder_acc',check_acc_number,name="check_acc_number")
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
