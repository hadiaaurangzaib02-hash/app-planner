from django.urls import path

from .views import (CreateTaskView, EditTaskView, 
        GetTaskByIdView, SearchTaskView, DeleteTaskView, DisplayTaskChangeView)

urlpatterns = [
    # Searchs
    path('new', CreateTaskView.as_view()),
    path('edit', EditTaskView.as_view()),
    path('task', GetTaskByIdView.as_view()),
    path('all', SearchTaskView.as_view()),
    path('delete/<int:task_id>', DeleteTaskView.as_view()),
    path('change/display', DisplayTaskChangeView.as_view())
]