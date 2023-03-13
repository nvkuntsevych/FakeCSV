from django.urls import path

from schemas.views import ListSchemaView, CreateSchemaView, UpdateSchemaView


app_name = 'schemas'

urlpatterns = [
    path('list/', ListSchemaView.as_view(), name='list'),
    path('create/', CreateSchemaView.as_view(), name='create'),
    path('update/<int:id>/', UpdateSchemaView.as_view(), name='update'),
]
