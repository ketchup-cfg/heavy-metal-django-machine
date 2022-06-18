from django.urls import path

from posts import views

app_name = "posts"
urlpatterns = [
    path("", views.PostIndexView.as_view(), name="index"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="update"),
]
