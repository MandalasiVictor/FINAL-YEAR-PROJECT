import pickle
from django.shortcuts import render, redirect
from ..models import UserInputs, ModelOutputs
import pandas as pd
import numpy as np
from joblib import load  
from decimal import Decimal, InvalidOperation
import ast
from django.shortcuts import get_object_or_404

def testing_view(
    total_budget: float,
    campaign_type: str,
    target_audience: str,
    seasonality: str,
    preferred_channels: list = None,
    primary_interest: str = 'Deals'  # Default primary interest
):
    # Attempt to load the machine learning model using joblib
    try:
        model = load('marketing_model.pkl')  # Update the path to your model file
        print("Model loaded successfully.")
    except FileNotFoundError as e:
        print("Error loading model:", e)
        return None  # Exit the function if the model cannot be loaded
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None  # Exit the function for any other errors

    # Prepare the input data for the model
    channels = preferred_channels if preferred_channels else ['Facebook', 'Twitter', 'WhatsApp', 'LinkedIn']
    
    # Create a list of input features based on user input
    input_data = []
    for channel in channels:
        input_data.append([
            channel,                     # Channel
            0.0,                           # Week (placeholder)
            total_budget / len(channels),  # Spend (equal distribution as a placeholder)
            0,                           # Verified Leads (placeholder; will be predicted)
            0,                           # Non-Verified Leads (placeholder)
            0,                           # Lead Revenue (placeholder)
            0,                           # CAC (placeholder)
            0,                           # Conversion Rate (%) (placeholder)
            campaign_type,              # Campaign Type
            0,                           # CTR (%) (placeholder)
            0,                           # Impressions (placeholder)
            seasonality,                # Seasonality Flag
            target_audience,            # Primary Audience Age
            primary_interest,             # Primary Interest
        ])

    # Convert input_data to a Pandas DataFrame
    column_names = [
        'Channel', 'Week', 'Spend', 'Verified Leads', 'Non-Verified Leads',
        'Lead Revenue','CAC', 'Conversion Rate (%)', 'Campaign Type',
        'CTR (%)', 'Impressions', 'Seasonality Flag', 'Primary Audience Age',
        'Primary Interest'
    ]
    X_pred = pd.DataFrame(input_data, columns=column_names)

    # Feature engineering
    X_pred['Cost_Per_Lead'] = X_pred['Spend'] / X_pred['Verified Leads'].replace(0, 1)
    X_pred['Is_Holiday'] = np.where(seasonality == 'Holiday', 1, 0)

    # Ensure correct data types
    X_pred['Spend'] = X_pred['Spend'].astype(float)
    X_pred['Verified Leads'] = X_pred['Verified Leads'].astype(float)
    X_pred['Non-Verified Leads'] = X_pred['Non-Verified Leads'].astype(float)
    X_pred['Lead Revenue'] = X_pred['Lead Revenue'].astype(float)
    X_pred['CAC'] = X_pred['CAC'].astype(float)
    X_pred['Conversion Rate (%)'] = X_pred['Conversion Rate (%)'].astype(float)
    X_pred['CTR (%)'] = X_pred['CTR (%)'].astype(float)
    X_pred['Impressions'] = X_pred['Impressions'].astype(float)
    X_pred['Is_Holiday'] = X_pred['Is_Holiday'].astype(int)

    # Check for NaN values
    if X_pred.isnull().values.any():
        print("Warning: There are NaN values in the input data.")
        print(X_pred[X_pred.isnull().any(axis=1)])  

    # Ensure the input shape is correct
    print("Input shape:", X_pred.shape)  

    # Get model predictions
    roi_predictions = model.predict(X_pred)

    # Calculate proportional allocation based on predicted ROI
    channel_effectiveness = {channels[i]: roi_predictions[i] for i in range(len(channels))}
    total_effectiveness = sum(channel_effectiveness.values())
    
    if total_effectiveness == 0:
        # Fallback to equal distribution
        allocations = {channel: total_budget / len(channels) for channel in channels}
    else:
        allocations = {
            channel: (effectiveness / total_effectiveness) * total_budget
            for channel, effectiveness in channel_effectiveness.items()
        }

    # Calculate predicted total ROI
    predicted_total_roi = sum(
        allocations[channel] * (effectiveness / 100)
        for channel, effectiveness in channel_effectiveness.items()
    )

    return {
        'optimal_budget_allocation': allocations,
        'expected_leads': sum(roi_predictions),  # Placeholder for expected leads; adjust as needed
        'estimated_revenue': predicted_total_roi,
        'channel_effectiveness': channel_effectiveness
    }


def prediction_view(request):
    if request.method == 'POST':
        # Collect data from the form
        total_budget = request.POST['total_budget']
       

        
        campaign_type = request.POST['campaign_type']
        target_audience = request.POST['target_audience']
        seasonality = request.POST['seasonality']
        preferred_channels = request.POST.getlist('preferred_channels')
        primary_interest = request.POST['primary_interest']

        
        # Load the model
        try:
            model = load('marketing_model.pkl')  # Update the path to your model file
            print("Model loaded successfully.")
        except FileNotFoundError as e:
            print("Error loading model:", e)
            return redirect('error_page')  # Redirect to an error page or handle it appropriately
        except Exception as e:
            print("An unexpected error occurred:", e)
            return redirect('error_page')  # Redirect to an error page or handle it appropriately

        # Prepare input data for prediction
        channels = preferred_channels if preferred_channels else ['Facebook', 'Twitter', 'WhatsApp', 'LinkedIn']
        input_data = []
        for channel in channels:
            input_data.append([
                channel,                     # Channel
                0.0,                        # Week (example placeholder; adjust as needed)
                float(total_budget) / len(channels),  # Spend
                0,                           # Verified Leads (placeholder)
                0,                           # Non-Verified Leads (placeholder)
                0,                           # Lead Revenue (placeholder)
                0,                           # CAC (placeholder)
                0,                           # Conversion Rate (%) (placeholder)
                campaign_type,              # Campaign Type
                0,                           # CTR (%) (placeholder)
                0,                           # Impressions (placeholder)
                seasonality,                # Seasonality Flag
                target_audience,            # Primary Audience Age
                primary_interest             # Primary Interest
            ])

        # Convert input_data to a Pandas DataFrame
        column_names = [
            'Channel', 'Week', 'Spend', 'Verified Leads', 'Non-Verified Leads',
            'Lead Revenue', 'CAC', 'Conversion Rate (%)', 'Campaign Type',
            'CTR (%)', 'Impressions', 'Seasonality Flag', 'Primary Audience Age',
            'Primary Interest'
        ]
        X_pred = pd.DataFrame(input_data, columns=column_names)

        # Feature engineering
        X_pred['Cost_Per_Lead'] = X_pred['Spend'] / X_pred['Verified Leads'].replace(0, 1)
        X_pred['Is_Holiday'] = np.where(seasonality == 'Holiday', 1, 0)

        # Ensure correct data types
        X_pred['Spend'] = X_pred['Spend'].astype(float)
        X_pred['Verified Leads'] = X_pred['Verified Leads'].astype(float)
        X_pred['Non-Verified Leads'] = X_pred['Non-Verified Leads'].astype(float)
        X_pred['Lead Revenue'] = X_pred['Lead Revenue'].astype(float)
        X_pred['CAC'] = X_pred['CAC'].astype(float)
        X_pred['Conversion Rate (%)'] = X_pred['Conversion Rate (%)'].astype(float)
        X_pred['CTR (%)'] = X_pred['CTR (%)'].astype(float)
        X_pred['Impressions'] = X_pred['Impressions'].astype(float)
        X_pred['Is_Holiday'] = X_pred['Is_Holiday'].astype(int)

        # Get model predictions
        roi_predictions = model.predict(X_pred)
        


        # Calculate proportional allocation based on predicted ROI
        channel_effectiveness = {channels[i]: roi_predictions[i] for i in range(len(channels))}
        total_effectiveness = sum(channel_effectiveness.values())

        if total_effectiveness == 0:
            # Fallback to equal distribution
            allocations = {channel: float(total_budget) / len(channels) for channel in channels}
        else:
            allocations = {
                channel: (effectiveness / total_effectiveness) * float(total_budget)
                for channel, effectiveness in channel_effectiveness.items()
            }

        # Calculate predicted total ROI
        predicted_total_roi = sum(
            allocations[channel] * (effectiveness / 100)
            for channel, effectiveness in channel_effectiveness.items()
        )
        predicted_channel_roi = [
            (channel,f'{allocations[channel] * (effectiveness / 100)}')
            for channel, effectiveness in channel_effectiveness.items()
        ]
        print(predicted_channel_roi)

        cpl = 2.21  
        # Calculate expected leads
        expected_leads = {
            channel: allocations[channel] / cpl for channel in channels
        }

        # Total expected leads
        total_expected_leads = sum(expected_leads.values())

        # Save user inputs
        user_input = UserInputs.objects.create(
            total_budget=total_budget,
            campaign_type=campaign_type,
            target_audience=target_audience,
            seasonality=seasonality,
            preferred_channels=', '.join(preferred_channels),
            primary_interest=primary_interest
        )

        keys = allocations.keys()
        allocationvalues = [(key, f"{float(value):.2f}") for key,value in allocations.items()]



        channel_effectiveness_values = [(key, f"{float(value):.2f}") for key,value in channel_effectiveness.items()]

        #looking for the most effective channel

        value = 0.0
        key = ''

        for suitable_platform in channel_effectiveness_values:
            # Convert the effectiveness to float for comparison
            effectiveness_value = float(suitable_platform[1])

            if effectiveness_value > value:
                value = effectiveness_value
                key = suitable_platform[0]

        # Format the value to 2 decimal places
        platform = {key: f"{value:.2f}"}
      
        # print('=====> effective channel', platform)
        # print('=====> allocationvalues', allocationvalues)

        # Save model outputs
        ModelOutputs.objects.create(
            user_input=user_input,
            optimal_budget_allocation=str(allocationvalues),  
            expected_leads=total_expected_leads,  
            estimated_revenue=f"{predicted_total_roi:.2f}",
            channel_effectiveness=str(channel_effectiveness_values), 
            most_effective_channel = platform,
            estimated_channel_revenue = str(predicted_channel_roi)
        )

        return redirect('results', user_input.id)  # Redirect to results page

    return render(request, 'integration/prediction_form.html')  # Render the form for GET requests

# def results_view(request, input_id):
#     user_input = UserInputs.objects.get(id=input_id)
#     model_output = ModelOutputs.objects.get(user_input=user_input)
#     return render(request, 'integration/results.html', {'user_input': user_input, 'model_output': model_output})


def results_view(request, input_id):
    
    user_input = get_object_or_404(UserInputs, id=input_id)
    model_output = get_object_or_404(ModelOutputs, user_input=user_input)


    try:
        optimal_budget_allocation = ast.literal_eval(model_output.optimal_budget_allocation)
        channel_effectiveness = ast.literal_eval(model_output.channel_effectiveness)
        estimated_channel_revenue = ast.literal_eval(model_output.estimated_channel_revenue)
        most_effective_channel = model_output.most_effective_channel
    except (ValueError, SyntaxError) as e:
        print(f"Error converting: {e}")
        if not optimal_budget_allocation:
            optimal_budget_allocation = [] 
        if not channel_effectiveness:
            channel_effectiveness = []
        if not estimated_channel_revenue:
            estimated_channel_revenue = []

    
    # print("Optimal Budget Allocation:", optimal_budget_allocation)
    # print("Optimal Budget Allocation:", channel_effectiveness)
    # print("Optimal Budget Allocation:", most_effective_channel)

    
    if not isinstance(optimal_budget_allocation, list) or not all(isinstance(i, tuple) and len(i) == 2 for i in optimal_budget_allocation):
        optimal_budget_allocation = [] 
    

    
    # Pass the converted data to the template
    context = {
        'user_input': user_input,
        'model_output': model_output,
        'optimal_budget_allocation': optimal_budget_allocation,
        'channel_effectiveness': channel_effectiveness,
        'most_effective_channel': most_effective_channel,
    }
    
    return render(request, 'integration/results.html', context)