from django.urls import path

from pcwkb_core.views import views

urlpatterns = [
    path("", views.index, name="index"),
]