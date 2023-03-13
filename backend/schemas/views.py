from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView

from schemas.forms import SchemaForm, ColumnFormSet
from schemas.models import Schema, Column


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
        column_formset = ColumnFormSet(queryset=Column.objects.none())
        context = {
            'schema_form': schema_form,
            'column_formset': column_formset,
        }
        return render(request, 'schemas/create.html', context)

    def post(self, request):
        schema_form = SchemaForm(request.POST)
        column_formset = ColumnFormSet(request.POST)
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
