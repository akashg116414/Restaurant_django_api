from django.db import models

# Create your models here.
class Person(models.Model):
    id = models.BigAutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=100)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = "person"

class FoodCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    flag = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = "food_category"

class FoodAttribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    flag = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = "food_attribute"


class Food(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    food_attribute = models.ForeignKey(FoodAttribute, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.IntegerField()

    class Meta:
        managed = False
        db_table = "food"

