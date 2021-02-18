from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    url(r'admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('todos/', include('todo.urls')),
    path('', include('todo.urls')),
]
