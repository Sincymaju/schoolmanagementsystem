from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.urls import path
from django.http import HttpResponse

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set.")
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'School Admin'),
        ('staff', 'Office Staff'),
        ('librarian', 'Librarian'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='staff')
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    objects = CustomUserManager()  # Assign the custom manager

    REQUIRED_FIELDS = ['email']  # Additional required fields

    def __str__(self):
        return f"{self.username} ({self.role})"

# Models for Students, Library History, and Fees History
class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    grade = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class LibraryHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book_title} - {self.student.name}"


class FeesHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.amount}"
