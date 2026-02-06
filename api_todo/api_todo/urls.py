from django.contrib import admin
from django.urls import include, path

from api.views import dashboard_view, calendar_view, records_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls') ),
    path('', dashboard_view, name='dashboard'),
    path('calendar/', calendar_view, name='calendar'),
    path('records/', records_list_view, name='records_list'),
    
]
