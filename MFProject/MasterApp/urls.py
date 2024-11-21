
from django.urls import path
from .views import *
from captcha import views as captcha_views

urlpatterns = [
    path('branchview/', branchview, name='branchview'),
    path('fileupload/', fileupload, name='fileupload'),
 
]

