from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.response import Response
import re
from django.contrib.auth.hashers import check_password, make_password
import time
import datetime
import jwt
import traceback
import json
from django.db.models import Q
# Create your views here.

# Models Imports.
from api.models import (
    Person,
    Food,
    FoodAttribute,
    FoodCategory,
)



def check(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # checking email, if in right format or not
    if(re.search(regex, email)):
        return True
    else:
        return False


class Signup(APIView):
    # def get(self, request):
        # userid = request.GET.get('userid')
        # details = Persons.objects.filter(userid=userid).first()
        # user = {'fname': details.fname, 'lname': details.lname}
        # print(user)
        # return Response(user, status.HTTP_200_OK)

    def post(self, request):
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        email = request.data.get('email')
        details = Person.objects.filter(email=email).first()
        if details:
            return Response({"message": "User already exist"}, status=status.HTTP_400_BAD_REQUEST)

        if not fname or not lname or not password or not dob or not email:
            return Response({"message": "Please fill required fields"}, status=status.HTTP_400_BAD_REQUEST)
        elif not check1:
            return Response({"message": "Bad email"}, status=status.HTTP_400_BAD_REQUEST)
        password_hash = make_password(password)
        # print( fname,lname,email,password,dob)
        Person.objects.create(fname=fname, lname=lname,
                              email=email, password=password_hash, dob=dob)

        # print(x.userid,x.fname)
        return Response({"result": "successful signup"}, status.HTTP_200_OK)




class Signin(APIView):
    # This class is to execute the sign-up process which involves acceptig user details including
    # user email (this is checked for validity and whether this address exists in the database)
    # password (bcrypt is used to compare this password with the hashed password stored in the database)
    # Outputs include:
    # <Created 201>
    # {"Message": "Authentication successful!", "Your user id":"id"}
    # (if the user exists in the database, the user-id of the user is shared for him to use)

    # <Bad request 400>
    # {"Message": "Fill the empty fields"}
    # (if any field is not filled)

    # <Bad request 400>
    # {"Message": "Invalid email address"}
    # (if email is not valid)

    # <Bad request 400>
    # {"message": "User doesn't exist"}
    # (if the email is not in the database)

    # <Bad request 400>
    # {"message": "Invalid credentials"}
    # (if the passwords don't match)
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        details = Person.objects.filter(email=email, flag=1).first()
        if details:
            if check_password(password, details.password):
                payload = {'id': details.id}
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                return Response({'message': 'Signin succesful', 'token': token}, status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid email/password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


class FoodItemCreate(APIView):
    @staticmethod
    def post(request):
        try:
            name = request.POST.get("name")
            if not name:
                return Response({"message": "food name missing."}, status.HTTP_400_BAD_REQUEST)
            description = request.POST.get("description")
            if not description:
                return Response({"message": "food description missing."}, status.HTTP_400_BAD_REQUEST)
            price = request.POST.get("price")
            if not price:
                return Response({"message": "food price missing."}, status.HTTP_400_BAD_REQUEST)
            category = request.POST.get("category")
            if not category:
                return Response({"message": "category missing."}, status.HTTP_400_BAD_REQUEST)
            category_obj = FoodCategory.objects.filter(name = category).first()
            if not category_obj:
                category_description = request.POST.get("category_description")
                if not category_description:
                    return Response({"message": "food description missing."}, status.HTTP_400_BAD_REQUEST)
                category_obj = FoodCategory.objects.create(name=category, description=category_description)
            attribute = request.POST.get("attribute")
            if not attribute:
                return Response({"message": "attribute Missing."}, status.HTTP_400_BAD_REQUEST)
            attribute_obj = FoodAttribute.objects.filter(name = attribute).first()
            if not attribute_obj:
                attribute_description = request.POST.get("attribute_description")
                if not description:
                    return Response({"message": "food description missing."}, status.HTTP_400_BAD_REQUEST)
                attribute_obj = FoodAttribute.objects.create(name=attribute, description=attribute_description)

            food_obj = FoodAttribute.objects.create(name=name, description=description, food_category= category_obj.id, food_attribute=attribute_obj.id, price = price)

            return Response({"result": {"food_item": food_obj}}, status.HTTP_200_OK)
        except:
            return Response({"error": traceback.format_exc()}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get(request):
        try:
            food_category_id = request.GET.get("food_category_id")
            food_attribute_id = request.GET.get("food_attribute_id")
            price_range = json.loads(request.GET.get("price_range","[]"))
            search = request.GET.get("search")
            food_details = (
                    Food.objects.filter()
                    .values("id", "name", "description", "food_category_id", "food_category__name", "food_attribute_id", "food_attribute__name")
                )
            if food_category_id:
                food_details = (
                    Food.objects.filter(food_category_id=food_category_id)
                    .values("id", "name", "description", "food_category_id", "food_category__name", "food_attribute_id", "food_attribute__name")
                )
            if food_attribute_id:
                food_details = (
                    Food.objects.filter(food_attribute_id=food_attribute_id)
                    .values("id", "name", "description", "food_category_id", "food_category__name", "food_attribute_id", "food_attribute__name")
                )
            if food_attribute_id and food_category_id:
                food_details = (
                    Food.objects.filter(food_attribute_id=food_attribute_id, food_category_id=food_category_id)
                    .values("id", "name", "description", "food_category_id", "food_category__name", "food_attribute_id", "food_attribute__name")
                )
            if search:
                food_details = (
                    Food.objects.filter(Q(id__icontains=search) | Q(name__icontains=search))
                    .values("id", "name", "description", "food_category_id", "food_category__name", "food_attribute_id", "food_attribute__name")
                )
            return Response({"result": {"food_details": food_details}}, HTTP_200_OK)
        except:
            return Response({"error": traceback.format_exc()}, HTTP_500_INTERNAL_SERVER_ERROR)