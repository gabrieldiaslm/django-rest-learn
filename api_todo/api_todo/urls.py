from django.contrib import admin
from django.urls import include, path

from api.views import dashboard_view, calendar_view, records_list_view, patient_card_view, patient_list_view, usertest_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls') ),
    path('', dashboard_view, name='dashboard'),
    path('calendar/', calendar_view, name='calendar'),
    path('records/', records_list_view, name='records_list'),
    path('patient/<int:patient_id>/card/', patient_card_view, name='patient_card'),
    path('patients/', patient_list_view, name='patient_list'),
    path('usertest/', usertest_list_view, name='usertest')
]
