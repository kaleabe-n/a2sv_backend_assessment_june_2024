from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import *

class IngredientSerilizer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']

class ReceipeSerializer(ModelSerializer):
    ingredients = SerializerMethodField()
    def get_ingredients(self,obj):
        ingredients = Ingredient.objects.filter(receipe=obj)
        return [ingredient.name for ingredient in ingredients]
        
    class Meta:
        model = Reciepe
        fields = ["title",'instruction','preparation_time','ingredients','id']
        
        
class CommentSerializer(ModelSerializer):
    
    receipe = SerializerMethodField()
    
    def get_receipe(self,obj:Comment):
        receipe = obj.reciepe
        ser = ReceipeSerializer(receipe)
        return ser.data
    class Meta:
        model = Comment
        fields = ["content","receipe"]