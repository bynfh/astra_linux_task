import json
import os
import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
        """List all the todo items for given requested user"""
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create
    def post(self, request, *args, **kwargs):
        """Create the Todo with given todo data"""
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"added": serializer.data}, status=status.HTTP_201_CREATED)

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

    # Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        """Retrieves the Todo with given todo_id"""
        queryset = Todo.objects.filter(id=todo_id)
        todo_instance = get_object_or_404(queryset)
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update
    def put(self, request, todo_id, *args, **kwargs):
        """Updates the todo item with given todo_id if exists"""
        queryset = Todo.objects.filter(id=todo_id)
        todo_instance = get_object_or_404(queryset)
        serializer = TodoSerializer(instance=todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def delete(self, request, todo_id, *args, **kwargs):
        """Deletes the todo item with given todo_id if exists"""
        queryset = Todo.objects.filter(id=todo_id)
        todo_instance = get_object_or_404(queryset)
        todo_instance.delete()
        return Response({"res": "Object deleted!"},
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
        """Send data from csv in local machine to model Todo"""
        serializer = FileTodbSerializer(data=request.data)
        if serializer.is_valid():
            if not os.path.exists(request.data.get('file_name')):
                return Response({"res": "Not found file", "Wrong path": request.data.get('file_name')},
                                status=status.HTTP_200_OK)
            import_to_db_from_csv(request.data.get('file_name'))
            return Response(
                {"res": f"File {request.data.get('file_name')} added"},
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
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            # Check that file exists
            if not os.path.exists(request.data.get('file_name')):
                return Response({"res": "Not found file",
                                 "Wrong path": request.data.get('file_name')},
                                status=status.HTTP_200_OK)
            files = {'file': (request.data.get('file_name_to_server'),
                              open(request.data.get('file_name'), 'rb'), 'text/csv')}
            # Send request to remote server
            response = requests.post(url=request.data.get('url'), files=files)
            if response.status_code == 200:
                return Response(
                    {"res": f"File {request.data.get('file_name')}->"
                            f"{request.data.get('file_name_to_server')}"
                            f" added to server {request.data.get('url')}"},
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
