from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random", views.randomEntry, name="random"),
    path("delete/<str:entry>", views.delete, name="delete")
]
