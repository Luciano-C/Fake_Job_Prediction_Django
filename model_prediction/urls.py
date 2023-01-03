from django.urls import path
from .views import *


# Viene de django y sirve para links 
#app_name = "passwords" 

urlpatterns = [
    path("", home, name="home"),
    path("prediction/", prediction, name="prediction")
]