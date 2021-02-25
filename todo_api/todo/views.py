import json
import os
import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer, FileSerializer, FileTodbSerializer
from rest_framework import permissions
from django.core import serializers

from .utils import export_to_csv, import_to_db_from_csv


class TodoListApiView(APIView):
    """
    Display and create todos
    Method get display everything todos
    Method post create todos
    :return Response with json and response status
    """
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # List all
    def get(self, request, *args, **kwargs):
        """
        List all the todo items for given requested user
        """
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create
    def post(self, request, *args, **kwargs):
        """
        Create the Todo with given todo data
        """
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'finish_date': request.data.get('finish_date'),
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailApiView(APIView):
    """
    Display, edit, delete single todo.
    Method get display single todo
    Method put edit single todo
    :return Response with json and response status
    """
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """
        Helper method to get the object with given todo_id
        """
        try:
            return Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return None

    # Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        """
        Retrieves the Todo with given todo_id
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update
    def put(self, request, todo_id, *args, **kwargs):
        """
        Updates the todo item with given todo_id if exists
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'finish_date': request.data.get('finish_date'),
            'user': request.user.id,
        }
        serializer = TodoSerializer(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def delete(self, request, todo_id, *args, **kwargs):
        """
        Deletes the todo item with given todo_id if exists
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class TodoExportCSV(APIView):
    """
    Export data about todos from server to local machine
    Request method == get
    Run utils export_to_csv and get HttpResponse
    :return HttpResponse from export_to_csv
    """
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, file_name):
        """
        Run util export_to_csv
        :return HttpResponse

        """
        response = HttpResponse(content_type='text/csv')
        response = export_to_csv(file_name, response)
        return response


class TodoImportFromCSV(APIView):
    """
    Import from csv in local machine to server
    Run util import_to_db_from_csv
    :return Response with status and info about processing
    """
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = {
            'file_name': request.data.get('file_name'),
        }
        serializer = FileTodbSerializer(data=data)
        if serializer.is_valid():
            if not os.path.exists(data.get('file_name')):
                return Response({"res": "Not found file", "Wrong path": data.get('file_name')},
                                status=status.HTTP_200_OK)
            import_to_db_from_csv(data.get('file_name'), Todo())
            return Response(
                {"res": f"File {data.get('file_name')} added"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendFileToRemoteServer(APIView):
    """
    Send file to remote server
    Url, file_name, file_name_to_server
    for remote server get from request data
    :return Response with status and info about processing
    """
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = {
            'file_name': request.data.get('file_name'),
            'file_name_to_server': request.data.get('file_name_to_server'),
            'url': request.data.get('url'),
        }
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            # Get data from request
            url = data.get('url')
            file_name = data.get('file_name')
            file_name_to_server = data.get('file_name_to_server')
            # Check that file exists
            if not os.path.exists(file_name):
                return Response({"res": "Not found file", "Wrong path": file_name}, status=status.HTTP_200_OK)
            files = {'file': (file_name_to_server, open(file_name, 'rb'), 'text/csv')}
            # Send request to remote server
            response = requests.post(url=url, files=files)
            if response.status_code == 200:
                return Response(
                    {"res": f"File {file_name}->{file_name_to_server} added to server {url}"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"res": (response.status_code, response.json())},
                    status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetHistoryTodos(APIView):
    """
    Get History about modify Todos
    :return Response with data about history
    """
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        todos = Todo.history.all()
        resp = json.loads(serializers.serialize('json', todos))
        return Response(resp, status=status.HTTP_200_OK)
