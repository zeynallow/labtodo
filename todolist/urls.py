from django.urls import path, include
from todolist import views


urlpatterns = [
    path('all/',  views.index, name='index'),
    path('create/',  views.create, name='create'),
    path('view/<int:pk>', views.view, name='view'),
    path('share/',  views.share, name='share'),
    path('changeStatus/',  views.changeStatus, name='changeStatus'),
]
