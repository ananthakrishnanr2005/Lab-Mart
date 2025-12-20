"""
URL configuration for pro project.

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
from django.conf.urls.static import static
from app1 import views
from pro import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loading, name='loading'),
    path('index', views.index, name='index'),
    path('userhome', views.userhome, name="userhome"),
    path('adminhome', views.adminhome, name="adminhome"),
    path('about', views.about, name="about"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('viewuser', views.viewuser, name='viewuser'),
    path('deleteuser/<int:id>',views.deleteuser, name='deleteuser'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('viewproduct', views.viewproduct,name="viewproduct"),
    path("updateproduct/<int:id>/", views.updateproduct, name="updateproduct"),
    path("deleteproduct/<int:id>/", views.deleteproduct, name="deleteproduct"),
    path('viewfeedback', views.viewfeedback, name='viewfeedback'),
    path('orderdetails', views.orderdetails, name='orderdetails'),
    path('userabout', views.userabout, name='userabout'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('updateprofile/<int:id>',views.updateprofile, name='updateprofile'),
    path('viewuserdetails/<int:id>', views.viewuserdetails, name='viewuserdetails'),
    path('shop', views.shop, name='shop'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('addtowishlist/<int:pid>', views.addtowishlist, name='addtowishlist'),
    path('cart', views.cart, name='cart'),
    path('addtocart/<int:pid>', views.addtocart, name='addtocart'),
    path('checkout', views.checkout, name='checkout'),
    path('addfeedback', views.addfeedback, name='addfeedback'),
    path('removefromwishlist/<int:wid>', views.removefromwishlist, name='removefromwishlist'),
    path('movetocart/<int:wid>', views.movetocart, name='movetocart'),
    path('removefromcart/<int:cid>', views.removefromcart, name='removefromcart'),
    path('updatecartquantity/<int:cid>', views.updatecartquantity, name='updatecartquantity'),
    path('placeorder', views.placeorder, name='placeorder'),
    path('ordersuccess', views.ordersuccess, name='ordersuccess'),
    path('userorderdetails/<int:order_id>/', views.userorderdetails, name='userorderdetails'),
    path('updateorderstatus/<int:order_id>/', views.updateorderstatus, name='updateorderstatus'),
    path('myorders', views.myorders, name='myorders'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('resetpassword/<str:token>/', views.resetpassword, name='resetpassword'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

