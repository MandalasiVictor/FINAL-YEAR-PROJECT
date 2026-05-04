from typing import Any

from django.shortcuts import redirect
from ..models import Integration
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from ..forms import IntegrationForm


class IntegrationListView(ListView):
    model = Integration
    template_name = 'integration/index.html'
    context_object_name = "integrations"

    
class IntegrationDetailView(DetailView):
    model = Integration
    template_name = 'integration/details.html'
    context_object_name = 'integration'


class IntegrationCreateView(CreateView):
    model = Integration
    form_class = IntegrationForm
    template_name = 'integration/create.html'
    success_url = reverse_lazy('integration-list')
    
    def get_success_url(self) -> str:
        messages.success(self.request, 'Integration created successfully')
        return super().get_success_url()


class IntegrationUpdateView(UpdateView):
    model = Integration
    template_name = 'integration/update.html'
    fields = ['username', 'password', 'host', 'key', 'endpoint', 'source']
    success_url = reverse_lazy('integration-list')


class IntegrationDeleteView(DeleteView):
    model = Integration
    template_name = 'integration/integration_confirm_delete.html'
    success_url = reverse_lazy('integration-list')
    context_object_name = 'integration'
    
    def get_success_url(self) -> str:
        messages.warning(self.request, 'Integration deleted successfully')
        return super().get_success_url()

    
class IntegrationEnableView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        integration = Integration.objects.get(pk=pk)
        
        if integration.is_active:
            integration.is_active = False
            messages.success(self.request, "The integration was deactivated successfully.")
        else:
            integration.is_active = True
            messages.success(self.request, "The integration was activated successfully.")
        integration.save()
        
        return redirect(reverse("integration-list"))
        
        
        
class IntegrationTestConnection(TemplateView):
    
    def get(self, request, *args, **kwargs):
        integration = Integration.objects.filter(pk=kwargs['pk']).first()
        result = integration.test_connection()
        
        if result is not True :
            messages.warning(request, f"{integration.host} Connection Test Failed: {result}")
        else:
            messages.success(request, f"Connection For {integration.host} Successful")

        return redirect(reverse("integration-list"))