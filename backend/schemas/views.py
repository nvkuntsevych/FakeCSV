from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView

from schemas.forms import CreateSchemaForm
from schemas.models import Schema


class ListSchemaView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users:login')
    model = Schema
    template_name = 'schemas/list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CreateSchemaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        form = CreateSchemaForm()
        context = {'form': form}
        return render(request, 'schemas/create.html', context)

    def post(self, request):
        form = CreateSchemaForm(request.POST)
        if form.is_valid():
            schema = form.save(commit=False)
            schema.user = request.user
            schema.save()
            return HttpResponseRedirect(reverse('schemas:list'))
        context = {'form': form}
        return render(request, 'schemas/create.html', context)
