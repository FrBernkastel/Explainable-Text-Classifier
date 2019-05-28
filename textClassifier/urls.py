from django.urls import path
from . import views

app_name = "classifier"

urlpatterns = [
    path('', views.review, name='review'),
    path('news/', views.news, name="news"),
    path('predict/', views.predict, name = 'predict'),    
]