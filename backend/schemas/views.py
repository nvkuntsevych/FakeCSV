import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden,
    HttpResponseNotFound, HttpResponseServerError,
    HttpResponseBadRequest, FileResponse, Http404
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from schemas.forms import SchemaForm, ColumnCreateFormSet, ColumnUpdateFormSet
from schemas.models import Schema, Column, DataSet
from schemas.tasks import task
from schemas.utils import (
    get_dataset_path, get_fieldnames,
    get_fieldtypes, is_owner
)


class ListSchemaView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users:login')
    model = Schema
    template_name = 'schemas/list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CreateSchemaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        schema_form = SchemaForm()
        column_formset = ColumnCreateFormSet(queryset=Column.objects.none())
        context = {
            'schema_form': schema_form,
            'column_formset': column_formset,
        }
        return render(request, 'schemas/create.html', context)

    def post(self, request):
        schema_form = SchemaForm(request.POST)
        column_formset = ColumnCreateFormSet(request.POST)
        if schema_form.is_valid() and column_formset.is_valid():
            schema = schema_form.save(commit=False)
            schema.user = request.user
            schema.save()
            for column_form in column_formset:
                column = column_form.save(commit=False)
                column.schema = schema
                column.save()
            return HttpResponseRedirect(reverse('schemas:list'))
        context = {
            'schema_form': schema_form,
            'column_formset': column_formset,
        }
        return render(request, 'schemas/create.html', context)


class UpdateSchemaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        schema = get_object_or_404(Schema, pk=pk)
        is_owner(request.user, schema)
        schema_form = SchemaForm(instance=schema)
        column_formset = ColumnUpdateFormSet(
            queryset=Column.objects.filter(schema_id=pk)
        )
        context = {
            'schema_form': schema_form,
            'column_formset': column_formset
        }
        return render(request, 'schemas/update.html', context)

    def post(self, request, pk):
        schema = get_object_or_404(Schema, pk=pk)
        is_owner(request.user, schema)
        schema_form = SchemaForm(request.POST, instance=schema)
        column_formset = ColumnUpdateFormSet(
            request.POST,
            queryset=Column.objects.filter(schema_id=pk)
        )
        if schema_form.is_valid() and column_formset.is_valid():
            schema_form.save()
            for column_form in column_formset:
                column_form.save()
            return HttpResponseRedirect(reverse('schemas:list'))
        context = {
            'schema_form': schema_form,
            'column_formset': column_formset
        }
        return render(request, 'schemas/update.html', context)


class DeleteSchemaView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('users:login')
    model = Schema
    success_url = reverse_lazy('schemas:list')
    template_name = 'schemas/delete.html'

    def get(self, request, pk):
        schema = get_object_or_404(Schema, pk=pk)
        is_owner(request.user, schema)
        return super().get(request, pk)


class RetrieveSchemaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        schema = get_object_or_404(Schema, pk=pk)
        is_owner(request.user, schema)
        context = {
            'schema': schema,
            'column_list': schema.columns.all(),
            'dataset_list': schema.datasets.order_by('created')
        }
        return render(request, 'schemas/retrieve.html', context)


def generate_file_view(request, pk):
    schema = get_object_or_404(Schema, pk=pk)
    is_owner(request.user, schema)
    dataset_sequence_number = DataSet.get_next_sequence_number(schema.id)
    records_number = int(request.POST['records_number'])
    dataset_path = get_dataset_path(
        schema.user.username,
        schema.name,
        dataset_sequence_number
    )
    column_separator = schema.column_separator
    string_character = schema.string_character
    fieldnames = get_fieldnames(schema)
    fieldtypes = get_fieldtypes(schema)

    dataset = DataSet.objects.create(
        schema=schema,
        status="Processing",
        path=dataset_path
    )
    task.delay(records_number, dataset_path, column_separator,
               string_character, fieldnames, fieldtypes, dataset.id)
    return HttpResponseRedirect(reverse('schemas:retrieve', args={schema.id}))


def download_file_view(request, pk):
    dataset = get_object_or_404(DataSet, pk=pk)
    is_owner(request.user, dataset)
    dataset_path = dataset.path
    if os.path.exists(dataset_path):
        with open(dataset_path, 'r') as dataset_file:
            response = FileResponse(dataset_file.read(), as_attachment=True)
            response['Content-Disposition'] = (
                'attachment; filename=' + os.path.basename(dataset_path)
            )
            return response
    raise Http404


def handler400(request, exception=None):
    return HttpResponseBadRequest(render(request, 'schemas/errors/400.html'))


def handler403(request, exception):
    return HttpResponseForbidden(render(request, 'schemas/errors/403.html'))


def handler404(request, exception):
    return HttpResponseNotFound(render(request, 'schemas/errors/404.html'))


def handler500(request, exception=None):
    return HttpResponseServerError(render(request, 'schemas/errors/500.html'))
