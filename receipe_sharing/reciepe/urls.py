from django.urls import path
from . import views

urlpatterns = [
    path('receipies/',views.receipe_api),
    path('receipies/<str:pk>/',views.modify_receipies),
    path('receipies/comment/<str:pk>/',views.comment_api),#accessing and creating comments with reciepie id
    
]
