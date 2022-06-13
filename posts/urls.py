from django.urls import path

from posts import views

app_name = "posts"
urlpatterns = [
    path("", views.PostIndexView.as_view(), name="index"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="update"),
]
