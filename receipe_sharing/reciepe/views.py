from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *

# Create your views here.


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def receipe_api(request):
    if request.method == "POST":
        user = request.user if request.user else null
        data = request.data
        try:
            ingredients = list(data['ingredients'])
            instruction = data['instruction']
        except Exception as e:
            print(e)
            return Response('invalid input',status=status.HTTP_400_BAD_REQUEST)
        try:
            receipe = Reciepe(instruction=instruction,creator=user)
            receipe.save()
            for ing in ingredients:
                ingredient = Ingredient(receipe=receipe,name=ing)
                ingredient.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == 'GET':
        reciepies = Reciepe.objects.all()
        ser = ReceipeSerializer(reciepies,many=True)
        return Response(ser.data)


@api_view(["PUT","DELETE"])
@permission_classes([AllowAny])  
def modify_receipies(request,pk):   
    if request.method == "DELETE":
        try:
            receipe = Reciepe.objects.get(id=pk)
        except Exception as e:
            print(e)
            return Response('receipe not found',status=status.HTTP_404_NOT_FOUND)

        if request.user == receipe.user:
            try:
                receipe.delete()
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == "PUT":
        data = request.data
        ingredients = list(data['ingredients'])
        instruction = data['instruction']
        try:
            reciepe = Reciepe.objects.get(id=pk)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ingredients = Reciepe.objects.filter(receipe=reciepe)
        ingredients.delete()
        try:
            receipe.instruction=instruction
            receipe.save()
            for ing in ingredients:
                ingredient = Ingredient(receipe=receipe, name=ing)
                ingredient.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET","POST"])
@permission_classes([AllowAny])
def comment_api(request,pk):
    if request.method == "POST":
        try:
            reciepe = Reciepe.objects.get(id=pk)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        content = data["content"]
        comment = Comment(content=content,author=request.user,reciepe=reciepe)
        comment.save()
        return Response(status=status.HTTP_201_CREATED)
    if request.method == "GET":
        try:
            reciepe = Reciepe.objects.get(id=pk)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        comments = Comment.objects.filter(reciepe=reciepe)
        ser = CommentSerializer(comments,many=True)
        return Response(ser.data)
