from django.urls import path
from .views import TodoListApiView, TodoDetailApiView, TodosExportAsCSV, InvertoryUpload, TodosImportCSV, SendFileTo, History
from . import views

urlpatterns = [
    path('', TodoListApiView.as_view()),
    path('<int:todo_id>/', TodoDetailApiView.as_view()),
    path('todos-csv-export/', TodosExportAsCSV.as_view()),
    path('download_file/', InvertoryUpload.as_view()),
    path('upload_file/', TodosImportCSV.as_view()),
    path('send_file/', SendFileTo.as_view()),
    path('history/', History.as_view()),

]