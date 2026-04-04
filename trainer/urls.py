from django.urls import path

from . import views


app_name = "trainer"

urlpatterns = [
    path("", views.index, name="index"),
    path("topic/<slug:slug>/", views.topic, name="topic"),
    path("topic/<slug:slug>/tests/", views.tests, name="tests"),
    path("topic/<slug:slug>/tasks/", views.tasks, name="tasks"),
    path("topic/<slug:slug>/cards/", views.cards, name="cards"),
]
