from django.urls import path

from schemas.views import (
    ListSchemaView, CreateSchemaView,
    UpdateSchemaView, DeleteSchemaView,
    RetrieveSchemaView, generate_file_view,
    download_file_view
)


app_name = 'schemas'

urlpatterns = [
    path('list/', ListSchemaView.as_view(), name='list'),
    path('create/', CreateSchemaView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateSchemaView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteSchemaView.as_view(), name='delete'),
    path('retrieve/<int:pk>/', RetrieveSchemaView.as_view(), name='retrieve'),
    path('generate/<int:pk>/', generate_file_view, name='generate'),
    path('download/<int:pk>/', download_file_view, name='download'),
]
