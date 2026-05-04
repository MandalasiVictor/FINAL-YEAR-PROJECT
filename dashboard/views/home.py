# from django.shortcuts import render
# from django.views.generic import TemplateView
# import json
# from integration.models import ModelOutputs

# class DashboardListView(TemplateView):   
#     template_name = 'dashboard/dashboard.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # Retrieve all model outputs
#         model_outputs = ModelOutputs.objects.all()

#         # Prepare data for Chart.js
#         channels = []
#         expected_leads = []
#         estimated_revenues = []

#         for output in model_outputs:
#             # Get the corresponding user input
#             user_input = output.user_input
#             channels.append(user_input.campaign_type)  
#             expected_leads.append(output.expected_leads)
#             estimated_revenues.append(output.estimated_revenue)

#         # Prepare the data structure for Chart.js
#         context['expected_leads_data'] = json.dumps({
#             'labels': channels,
#             'datasets': [{
#                 'label': 'Expected Leads',
#                 'data': expected_leads,
#                 'backgroundColor': 'rgba(75, 192, 192, 0.2)',
#                 'borderColor': 'rgba(75, 192, 192, 1)',
#                 'borderWidth': 1
#             }]
#         })

#         context['estimated_revenue_data'] = json.dumps({
#             'labels': channels,
#             'datasets': [{
#                 'label': 'Estimated Revenue',
#                 'data': estimated_revenues,
#                 'backgroundColor': 'rgba(153, 102, 255, 0.2)',
#                 'borderColor': 'rgba(153, 102, 255, 1)',
#                 'borderWidth': 1
#             }]
#         })
#         return context


from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
import json
import ast  
from integration.models import ModelOutputs

class DashboardListView(TemplateView):   
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
   
        model_outputs = ModelOutputs.objects.all()

        # Get filtering parameters from the GET request
        time_filter = self.request.GET.get('time_filter')

        if time_filter:
            now = timezone.now()
            if time_filter == 'day':
                start_date = now - timedelta(days=1)
            elif time_filter == 'week':
                start_date = now - timedelta(weeks=1)
            elif time_filter == 'month':
                start_date = now - timedelta(days=30)  
            elif time_filter == 'year':
                start_date = now - timedelta(days=365)  
            else:
                start_date = None
            
            if start_date:
                model_outputs = model_outputs.filter(created_at__gte=start_date)

        # Prepare data for Chart.js
        channels = []
        expected_leads = []
        estimated_revenues = []
        optimal_budget_allocations = []
        channel_effectiveness = {}

        for output in model_outputs:
            # Get the corresponding user input
            user_input = output.user_input
            campaign_type = user_input.campaign_type
            
            channels.append(campaign_type)  
            expected_leads.append(output.expected_leads)
            estimated_revenues.append(output.estimated_revenue)

            # Prepare optimal budget allocation using ast.literal_eval
            try:
                optimal_budget_allocation = ast.literal_eval(output.optimal_budget_allocation)
                for channel, allocation in optimal_budget_allocation:
                    optimal_budget_allocations.append((channel, float(allocation)))
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing optimal_budget_allocation: {e}")

            # Prepare channel effectiveness using ast.literal_eval
            try:
                channel_effectiveness_data = ast.literal_eval(output.channel_effectiveness)
                for channel, effectiveness in channel_effectiveness_data:  
                    channel_effectiveness[channel] = channel_effectiveness.get(channel, 0) + float(effectiveness)
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing channel_effectiveness: {e}")

        # Prepare the data structure for Chart.js
        context['expected_leads_data'] = json.dumps({
            'labels': channels,
            'datasets': [{
                'label': 'Expected Leads',
                'data': expected_leads,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }]
        })

        context['estimated_revenue_data'] = json.dumps({
            'labels': channels,
            'datasets': [{
                'label': 'Estimated Revenue',
                'data': estimated_revenues,
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 1
            }]
        })

        # Prepare data for Optimal Budget Allocation Bar Chart
        budget_channels, budget_allocations = zip(*optimal_budget_allocations) if optimal_budget_allocations else ([], [])
        context['optimal_budget_allocation_data'] = json.dumps({
            'labels': budget_channels,
            'datasets': [{
                'label': 'Optimal Budget Allocation',
                'data': budget_allocations,
                'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 1
            }]
        })

        # Prepare data for Channel Effectiveness Pie Chart
        effectiveness_labels = list(channel_effectiveness.keys())
        effectiveness_values = list(channel_effectiveness.values())
        
        context['channel_effectiveness_data'] = json.dumps({
            'labels': effectiveness_labels,
            'datasets': [{
                'label': 'Channel Effectiveness',
                'data': effectiveness_values,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                'borderWidth': 1
            }]
        })

        return context