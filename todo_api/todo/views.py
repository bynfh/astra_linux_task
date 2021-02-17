import os
import sys

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer, InventoryFile_Serializer, FileSerializer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .utils import export_to_csv, ImportToDbFromCsv


class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        """
        List all the todo items for given requested user
        """
        todos = Todo.objects.filter(user=request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
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
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            return None

    # 3. Retrieve
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

    # 4. Update
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

    # 5. Delete
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


def get_todo_data():
    queryset = Todo.objects.only('task', 'timestamp', 'completed', 'updated', 'finish_date', 'user')
    fields = ['task', 'timestamp', 'completed', 'updated', 'finish_date', 'user']
    titles = ['Task', 'Timestamp', 'Completed', 'Updated', 'Finish_date', 'User']
    file_name = 'Todos'
    return queryset, fields, titles, file_name


class TodosExportAsCSV(APIView):
    def get(self, request):
        todos = get_todo_data()
        data = export_to_csv(queryset=todos[0],
                             fields=todos[1],
                             titles=todos[2],
                             file_name=todos[3])
        return data


class InvertoryUpload(APIView):
    serializer_class = InventoryFile_Serializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            serializer = InventoryFile_Serializer(data=request.data)
            print(serializer.initial_data)

            if serializer.is_valid():
                print(serializer.data)
                return Response("Done")
            else:
                print(serializer.errors)
                return Response("Not Done")

        except Exception as e:
            return Response(str(e))


class TodosImportCSV(APIView):
    def get(self, request):
        # try:
        ImportToDbFromCsv('/home/oleg/Загрузки/Todos.csv')
        # except:
        #     return Response(
        #         {"res": "Object failed!"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        return Response(
            {"res": "Object added!"},
            status=status.HTTP_200_OK
        )


class SendFileTo(APIView):
    def post(self, request):
        data = {
            'file_name': request.data.get('file_name'),
            'file_name_to_server': request.data.get('file_name_to_server'),
            'url': request.data.get('url'),
        }
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            print(data)
            url = data.get('url')
            file_name = data.get('file_name')
            file_name_to_server = data.get('file_name_to_server')
            if not os.path.exists(file_name):
                return Response({"res": "Not found file", "Wrong path": file_name}, status=status.HTTP_200_OK)
            files = {'file': (file_name_to_server, open(file_name, 'rb'), 'text/csv')}
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
# {
#     "file_name": "/home/oleg/Загрузки/Todos.csv",
#     "file_name_to_server": "This field may not be null.",
#     "url":  "http://qa-test.expsys.org:8080/upload-file"
# }