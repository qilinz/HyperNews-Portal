from django.urls import path, re_path
from . import views


urlpatterns = [
    path('news/', views.MainView.as_view()),
    path('news/<int:news_id>/', views.DetailsView.as_view()),
    path('news/create/', views.NewPostView.as_view()),
    path('', views.index_view)
]