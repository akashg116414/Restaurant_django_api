
from django.urls import path
from api.views import (Signin, Signup,FoodItemCreate)

urlpatterns = [
    path('user/signin/', Signin.as_view()),
    path("user/signup/", Signup.as_view()),
    path("user/food/", FoodItemCreate.as_view()),
]