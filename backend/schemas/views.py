from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from schemas.forms import SchemaForm, ColumnCreateFormSet, ColumnUpdateFormSet
from schemas.models import Schema, Column, DataSet
from schemas.utils import get_dataset_path, get_fieldnames, get_fieldtypes
from schemas.tasks import task


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
        schema_form = SchemaForm(instance=schema)
        column_formset = ColumnUpdateFormSet(queryset=Column.objects.filter(schema_id=pk))
        context = {
            'schema_form': schema_form,
            'column_formset': column_formset,
            'column_number': len(column_formset),
        }
        return render(request, 'schemas/update.html', context)

    def post(self, request, pk):
        schema = get_object_or_404(Schema, pk=pk)
        schema_form = SchemaForm(request.POST, instance=schema)
        column_formset = ColumnUpdateFormSet(request.POST, queryset=Column.objects.filter(schema_id=pk))
        if schema_form.is_valid() and column_formset.is_valid():
            schema_form.save()
            for column_form in column_formset:
                column_form.save()
            return HttpResponseRedirect(reverse('schemas:list'))
        context = {
            'schema_form': schema_form,
            'column_formset': column_formset,
            'column_number': len(column_formset),
        }
        return render(request, 'schemas/update.html', context)


class DeleteSchemaView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('users:login')
    model = Schema
    success_url = reverse_lazy('schemas:list')
    template_name = 'schemas/delete.html'


class RetrieveSchemaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        schema = get_object_or_404(Schema, pk=pk)
        context = {
            'schema': schema,
            'columns': schema.columns.all(),
            'datasets': schema.datasets.order_by('created')
        }
        return render(request, 'schemas/retrieve.html', context)


def generate_file_view(request, pk):
    schema = get_object_or_404(Schema, pk=pk)

    dataset_sequence_number = DataSet.get_next_sequence_number(schema.id)
    dataset = DataSet.objects.create(
        schema=schema,
        status="Processing",
        sequence_number=dataset_sequence_number
    )

    records_number = int(request.POST['records_number'])
    dataset_path = get_dataset_path(schema.user.username, schema.name, dataset_sequence_number)
    column_separator = schema.column_separator
    string_character = schema.string_character
    fieldnames = get_fieldnames(schema)
    fieldtypes = get_fieldtypes(schema)

    dataset.path = dataset_path
    dataset.save()

    task.delay(records_number, dataset_path, column_separator,
               string_character, fieldnames, fieldtypes, dataset.id)

    return HttpResponseRedirect(reverse('schemas:retrieve', args={schema.id}))


def download_file_view(request, pk):
    from django.http import FileResponse, Http404
    import os

    dataset = get_object_or_404(DataSet, pk=pk)
    schema = dataset.schema
    dataset_sequence_number = dataset.sequence_number
    file_path = get_dataset_path(schema.user.username, schema.name, dataset_sequence_number)
    if os.path.exists(file_path):
        with open(file_path, 'r') as fh:
            response = FileResponse(fh.read(), as_attachment=True)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404
