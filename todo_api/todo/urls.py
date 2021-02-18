from django.urls import path
from .views import TodoListApiView, TodoDetailApiView,\
                   TodoExportCSV, TodoImportFromCSV,\
                   SendFileToRemoteServer, GetHistoryTodos

urlpatterns = [
    path('', TodoListApiView.as_view()),
    path('<int:todo_id>/', TodoDetailApiView.as_view()),
    path('export_to_csv/', TodoExportCSV.as_view()),
    path('upload_file/', TodoImportFromCSV.as_view()),
    path('send_file_to_remote/', SendFileToRemoteServer.as_view()),
    path('history/', GetHistoryTodos.as_view()),

]