from django.shortcuts import render, redirect
from .forms import PredictionForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from . model_loader import predict_insurance
from appname import model_loader
import pandas as pd
import os
<<<<<<< HEAD
=======
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from io import BytesIO
import base64
>>>>>>> 9893038973993e121a6649ce0ffebe6967b3442a


def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

predict_insurance = model_loader.predict_insurance
@login_required
def predict(request):
    prediction = None
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            print(f"Form Data in predict view: {form_data}") 
            result = predict_insurance(form_data)
            print(f"Result from predict_insurance: {result}") 
            if isinstance(result, tuple) and len(result) == 2:
                prediction, probability = result
                return render(request, 'predict.html', {'form': form, 'prediction': prediction})
            else:
                return render(request, 'predict.html', {'form': form, 'prediction': f"Error in prediction: {result}"})
        else:
            return render(request, 'predict.html', {'form': form, 'prediction': "Invalid form data"})
    else:
        form = PredictionForm()
    return render(request, 'predict.html', {'form': form, 'prediction': prediction})

@login_required
def dashboard(request):
    num_records = 1000
    target_distribution = "Will Avail: 600, Will Not Avail: 400"
    accuracy_score = '84.17%'
    total_predictions = 1987
    target_labels = "Will Avail,Will Not Avail"
    target_values = "710,1277"
    feature_labels = ["Age","AnnualIncome","FamilyMembers"]
    feature_values = ["35","50000","3"]
    feature_stats = list(zip(feature_labels, feature_values))
    feature_labels_str = ",".join(feature_labels)
    feature_values_str = ",".join(feature_values)

    context = {
        'num_records': num_records,
        'target_distribution': target_distribution,
        'accuracy_score': accuracy_score,
        'total_predictions': total_predictions,
        'target_labels': target_labels,
        'target_values': target_values,
        'feature_labels': feature_labels_str,
        'feature_values': feature_values_str,
        'feature_stats': feature_stats,
    }
    return render(request, 'dashboard.html', context)