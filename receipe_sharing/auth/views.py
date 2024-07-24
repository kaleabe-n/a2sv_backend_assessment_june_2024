from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request: Request):
    if request.method == "POST":
        data = request.data
        if "email" not in data:
            return Response("email is required", status=status.HTTP_400_BAD_REQUEST)
        if "first_name" not in data:
            return Response(
                "first name is required", status=status.HTTP_400_BAD_REQUEST
            )
        if "last_name" not in data:
            return Response("last name is required", status=status.HTTP_400_BAD_REQUEST)
        if "password" not in data:
            return Response("password is required", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User(
                username=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                password=(data["password"]),
            )
            print(user.password)
            user.save()
        except Exception as e:
            return Response(
                "unable to create user", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: Request):
    data = request.data
    if "email" not in data:
        return Response("email is required", status=status.HTTP_400_BAD_REQUEST)
    if "password" not in data:
        return Response("password is required", status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=data["email"])
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    print(user.password)
    print(make_password(data["password"]))
    print(data["password"])
    if user.password == (data["password"]):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({"access": access, "refresh": str(refresh)})
    else:
        return Response("invalid credintials", status=status.HTTP_400_BAD_REQUEST)
