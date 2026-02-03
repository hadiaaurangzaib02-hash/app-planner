from django.urls import path

from .views import (CreatePlanView, ListAllPlansView, DeletePlanView, ShowPlanView, EditPlaniew,
                AddClientToPlan)

urlpatterns = [
    # Searchs
    path('new', CreatePlanView.as_view()),
    path('all', ListAllPlansView.as_view()),
    path('delete/<int:plan_id>', DeletePlanView.as_view()),
    path('<int:plan_id>', ShowPlanView.as_view()),
    path('edit', EditPlaniew.as_view()),
    path('add-to-client', AddClientToPlan.as_view())
]