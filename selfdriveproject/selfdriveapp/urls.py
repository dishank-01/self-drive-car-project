from django.contrib import admin
from django.urls import path
from selfdriveapp import views
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path('register',views.register),
    path('login',views.user_login),
    path('homepage',views.home),
     path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    #path('age',views.age),
    #path('city',views.city),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('placeorder',views.placeorder),
    path('product/<pid>',views.product_details),
    path('makepayment',views.makepayment),
    path('remove/<cid>',views.remove),
    path('about',views.about),
    path('contact',views.contact),
    path('forget',views.forget_password),
    path('userlogout',views.user_logout),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)