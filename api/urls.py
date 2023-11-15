from django.urls import include, path
from rest_framework import routers

from users import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet, basename="user")

urlpatterns = [
    path("v1/", include(router.urls)),
]

app_name = 'users'
