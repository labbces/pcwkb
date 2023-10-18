from django.urls import path

from pcwkb_core.views import views

urlpatterns = [
    path("", views.index, name="index"),
    path("browse_species", views.browse_species, name='browse_species'),
    path("species_page/<str:species_code>", views.species_page, name='species_page'),
    path('team', views.team, name='team'),
    path('funding', views.funding, name='funding'),
    path('faq', views.faq, name='faq'),
]