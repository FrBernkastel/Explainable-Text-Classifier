from django.urls import path
from . import views

app_name = "classifier"

urlpatterns = [
    path('', views.review, name='review'),
    path('news/', views.news, name="news"),
    path('predict/', views.predict, name = 'predict'),
    path('predict2/', views.predict_news, name = 'predict_news'),
    path('pick/', views.pick_review, name = 'pick_review'),
    path('pick2/', views.pick_news, name = 'pick_news')
]