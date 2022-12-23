from rest_framework.routers import DefaultRouter
from accounts.viewsets import UserViewSet


router = DefaultRouter()


router.register(r"user", UserViewSet)
