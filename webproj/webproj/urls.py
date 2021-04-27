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
    path('updatePromotion/<str:promotion_id>/', views.updatePromotion, name='updatePromotion'),
    path('deletePromotion/<str:id>', views.deletePromotion, name='deletePromotion'),
    ########
    path('searchProducts/', views.searchProducts, name='searchProducts'),
    path('details/<str:id>', views.productInfo, name='productInfo'),
    ########
    path('account/', views.account, name='account'),
    path('sold/', views.soldManagement, name='soldManagement'),
    ########
    path('commentsManagement/', views.commentsManagement, name='commentsManagement'),
    path('deleteComment/<str:id>', views.deleteComment, name='deleteComment'),
    ######
    path('shop/', views.shop, name='shop'),
    #######
    path('usersManagement/', views.usersManagement, name='usersManagement'),
    path('deleteUser/<str:id>', views.deleteUser, name='deleteUser'),
    path('updateUser/', views.updateUser, name='updateUser'),

    path('', views.home, name='home'),
    #########
    path('addToCart/<str:id>', views.addToCart, name='addToCart'),
    path('removeFromCart/<str:id>', views.removeFromCart, name='removeFromCart'),
    path('increaseQuantity/<str:id>', views.increaseQuantity, name='increaseQuantity'),
    path('decreaseQuantity/<str:id>', views.decreaseQuantity, name='decreaseQuantity'),



    #TODO
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart')




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)