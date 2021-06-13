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
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login', views.CustomAuthToken.as_view()),
    path('signup', views.sign_up),

    # Products
    path('product', views.get_product),
    path('products', views.get_products),
    path('productcre', views.create_product),
    path('productup', views.update_product),
    path('productdel/<int:id>', views.del_product),
    # Promotions
    path('promotions', views.get_promotions),
    path('promotioncre', views.create_promotion),
    path('promotionup', views.update_promotion),
    path('promotiondel/<int:id>', views.del_promotion),
    #Search
    path('search', views.search_products),
    #Comments
    path('commentcre', views.create_comment),
    path('commentdel/<int:id>', views.del_comment),








    path('admin/', admin.site.urls),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
