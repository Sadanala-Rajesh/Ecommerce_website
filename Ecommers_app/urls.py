
from django.urls import path
from Ecommers_app.views import register,login_page,logout_page,display_Products,Products_add_to_cart,display_user_cart_details,Send_mail_to_Buyer

urlpatterns = [
    path('register/', register),
    path('login/',login_page),
    path('logout/',logout_page),
    path('display_products/',display_Products),
    path('Products_add_to_cart/<str:name>/',Products_add_to_cart,name='Products_add_to_c,arts'),
    path('display_user_cart_details/',display_user_cart_details),
    path('Send_mail_to_Buyer/<str:name>/',Send_mail_to_Buyer),
]
