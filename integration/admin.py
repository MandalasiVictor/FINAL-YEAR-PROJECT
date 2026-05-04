from django.contrib import admin
from .models import Integration
from .models import UserInputs, ModelOutputs

class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'host', 'source', 'created', 'updated')
    search_fields = ('username', 'host')
    list_filter = ('source', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    fieldsets = (
        ('Integration Details', {
            'fields': ('username', 'password', 'host', 'key', 'endpoint', 'source')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
    )
    actions = ['test_connection']

    def test_connection(self, request, queryset):
        # Implement your logic to test the connection for selected Integration objects
        pass
    test_connection.short_description = "Test Connection"

class UserInputsAdmin(admin.ModelAdmin):
    list_display = ('campaign_type', 'total_budget', 'target_audience', 'seasonality', 'preferred_channels', 'primary_interest')
    search_fields = ('campaign_type', 'target_audience', 'seasonality', 'preferred_channels', 'primary_interest')

class ModelOutputsAdmin(admin.ModelAdmin):
    list_display = ('user_input', 'optimal_budget_allocation', 'expected_leads', 'estimated_revenue', 'channel_effectiveness')
    search_fields = ('user_input__campaign_type',)  # Allows searching by campaign type in related UserInputs

# Register the models with the admin site
admin.site.register(UserInputs, UserInputsAdmin)
admin.site.register(ModelOutputs, ModelOutputsAdmin)

admin.site.register(Integration, IntegrationAdmin)