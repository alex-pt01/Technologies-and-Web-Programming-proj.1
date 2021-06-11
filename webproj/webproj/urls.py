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

    # Products
    path('ws/product', views.get_product),
    path('ws/products', views.get_products),
    path('ws/productcre', views.create_product),
    path('ws/productup', views.update_product),
    path('ws/productdel/<int:id>', views.del_product),
    # Promotions
    path('ws/promotions', views.get_promotions),
    path('ws/promotioncre', views.create_promotion),
    path('ws/promotionup', views.update_promotion),
    path('ws/promotiondel/<int:id>', views.del_promotion),
    #Search
    path('ws/search', views.search_products),
    #Comments
    path('ws/commentcre', views.create_comment),
    path('ws/commentdel/<int:id>', views.del_comment),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
