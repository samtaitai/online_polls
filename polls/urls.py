# path() takes {route}, {view}, [{kwang}, {name}]
from django.urls import path
from . import views

# set the application namespace
app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("new/", views.create_poll, name="create_poll"),
]