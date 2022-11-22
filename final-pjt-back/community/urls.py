from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('<int:movie_pk>/reviews/', views.review_list),
    path('<int:movie_pk>/reviews/create/', views.create_review),
    path('reviews/<int:review_pk>/', views.review_detail),
    path('reviews/<int:review_pk>/comments/', views.create_comment),
    path('reviews/<int:review_pk>/like/', views.like_review),
]