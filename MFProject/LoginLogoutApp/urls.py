
from django.urls import path
from .views import User_Login,dashboard_view,user_Logout,mainpage
from captcha import views as captcha_views

urlpatterns = [
    path('login/', User_Login, name='login'),
    path('logout/', user_Logout, name='logout'),
    path('dashboard/',dashboard_view, name='dashboard'),
    path('mainpage/',mainpage, name='mainpage'),
    path('captcha/image/<str:key>/', captcha_views.captcha_image, name='captcha-image'),
    path('captcha/refresh/', captcha_views.captcha_refresh, name='captcha-refresh'),
]
