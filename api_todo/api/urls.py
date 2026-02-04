from django.urls import path
from api.views import todo_list


urlpatterns = [
    path('', todo_list),
]