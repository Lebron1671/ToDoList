from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("view/", views.view, name="view"),
    path("delete_list/<int:id>", views.delete_list, name="delete_list"),
    path("delete_task/<int:id>", views.delete_task, name="delete_task"),
]