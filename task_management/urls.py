
from django.urls import path

from .views import TaskCreateView, TaskStatusView,  FailedTaskListView, TaskRecoveryView


urlpatterns = [

    path(
        "tasks/",
        TaskCreateView.as_view(),
        name="task-create"
    ),

    path(
        "tasks/<uuid:task_id>/",
        TaskStatusView.as_view(),
        name="task-status"
    ),
    
    path(
    "tasks/failed/",
    FailedTaskListView.as_view(),
    name="failed-tasks"
),

path(
    "tasks/<uuid:task_id>/recover/",
    TaskRecoveryView.as_view(),
    name="task-recovery"
),

]
