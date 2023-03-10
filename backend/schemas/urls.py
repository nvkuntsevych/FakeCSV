from django.urls import path

from schemas.views import ListSchemaView


app_name = 'schemas'

urlpatterns = [
    path('list/', ListSchemaView.as_view(), name='list'),
]
