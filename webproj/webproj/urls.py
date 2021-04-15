"""webproj URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    ########
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    #########
    path('productsManagement/', views.productsManagement, name='productsManagement'),
    path('createProduct/', views.createProduct, name='createProduct'),
    path('updateProduct/<str:pk>/', views.updateProduct, name='updateProduct'),
    path('deleteProduct/<str:id>', views.deleteProduct, name='deleteProduct'),
    ########
    path('promotionsManagement/', views.promotionsManagement, name='promotionsManagement'),
    path('createPromotion/', views.createPromotion, name='createPromotion'),
    path('updatePromotion/<str:pk>/', views.updatePromotion, name='updatePromotion'),
    path('deletePromotion/<str:id>', views.deletePromotion, name='deletePromotion'),
    ########
    path('searchProducts/', views.searchProducts, name='searchProducts'),
    #W#####
    path('', views.home, name='home'),


    #TODO
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart')




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
