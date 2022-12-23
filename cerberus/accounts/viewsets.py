from datetime import timezone

from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from accounts.models import Email,User
from accounts.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
)

from base import response



class UserViewSet(
    GenericViewSet,
    RetrieveModelMixin,
):
    queryset = User.objects.all()

    @action(
        detail=False,
        methods=[
            "POST",
        ],
    )
    def sign_up(
        self,
        request,
    ):
        context = {
            "request": request,
        }
        serializer = UserRegistrationSerializer(data=request.data, context=context)

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return response.Created(
            data=serializer.validated_data,
        )

    @action(
        detail=False,
        methods=[
            "POST",
        ],
    )
    def login(
        self,
        request,
    ):
        data = request.data

        serializer = UserSerializer(
            data=data,
        )

        try:

            serializer.is_valid(
                raise_exception=True,
            )

        except Exception as e:

            raise ValueError(e.args[0]) from e

        return response.Ok(
            data=serializer.validated_data,
        )

    @action(
        detail=False,
        methods=[
            "GET",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def fetch_profile(
        self,
        request,
    ):
        user = request.user
        serializer = UserSerializer(
            instance=user,
        )

        try:
            last_login = timezone.localtime(
                value=request.user.last_login,
            ).strftime("%d-%b-%Y %I:%M:%S %p")
        except Exception:
            last_login = None

        profile = {
            "ip_address": request.META.get("REMOTE_ADDR", None),
            "last_login": last_login,
        }

        profile.update(serializer.data)

        return response.Ok(
            data=profile,
        )

