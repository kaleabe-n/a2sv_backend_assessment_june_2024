from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Reciepe(models.Model):
    title = models.CharField(max_length=50)
    instruction = models.TextField()
    preparation_time = models.IntegerField()
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    
class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    Reciepe = models.ForeignKey(Reciepe,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    

class Comment(models.Model):
    content = models.TextField()
    reciepe = models.ForeignKey(Reciepe,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self) -> str:
        return self.author.username + self.content[:20]