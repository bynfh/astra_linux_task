from django.urls import path
from .views import TodoListApiView, TodoDetailApiView, TodosExportAsCSV

urlpatterns = [
    path('', TodoListApiView.as_view()),
    path('<int:todo_id>/', TodoDetailApiView.as_view()),
    path('todos-csv-export/', TodosExportAsCSV.as_view())
]