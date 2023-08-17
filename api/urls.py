from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from users import views

router = routers.DefaultRouter()
router.register("users", views.CurrentClientViewSet, basename="user")

urlpatterns = [
    include("v1/", namespace="api"),
]
