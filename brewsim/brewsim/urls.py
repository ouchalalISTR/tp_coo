from django.contrib import admin
from django.urls import path
from high_level import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "departement/<int:pk>",
        views.DepartementDetailView.as_view(),
        name="departement",
    ),
    path("machine/<int:pk>", views.MachineDetailView.as_view(), name="machine"),
    path(
        "ingredient/<int:pk>", views.IngredientDetailView.as_view(), name="ingredient"
    ),
    path("prix/<int:pk>", views.PrixDetailView.as_view(), name="prix"),
    path(
        "quantiteingredient/<int:pk>",
        views.QuantiteIngredientDetailView.as_view(),
        name="quantiteingredient",
    ),
    path("action/<int:pk>", views.ActionDetailView.as_view(), name="action"),
    path("recette/<int:pk>", views.RecetteDetailView.as_view(), name="recette"),
    path("usine/<int:pk>", views.UsineDetailView.as_view(), name="usine"),
    path("api/<int:pk>", views.APIDetailView.as_view(), name="api"),
]
