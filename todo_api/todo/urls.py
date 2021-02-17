from django.urls import path
from .views import TodoListApiView, TodoDetailApiView, TodosExportAsCSV, TodosImportCSV, SendFileTo, History

urlpatterns = [
    path('', TodoListApiView.as_view()),
    path('<int:todo_id>/', TodoDetailApiView.as_view()),
    path('todos-csv-export/', TodosExportAsCSV.as_view()),
    path('upload_file/', TodosImportCSV.as_view()),
    path('send_file/', SendFileTo.as_view()),
    path('history/', History.as_view()),

]