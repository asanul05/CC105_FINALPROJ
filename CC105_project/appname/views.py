from django.shortcuts import render, redirect
from .forms import PredictionForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . model_loader import predict_insurance
from appname import model_loader
import pandas as pd
import os


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
    feature_summary = "Age: mean=35, AnnualIncome: mean=50000, FamilyMembers: mean=3"
    target_distribution = "Will Avail: 600,           Will Not Avail: 400"
    accuracy_score = '82%'
    confusion_matrix = "[[300, 50], [30, 620]]"
    loss_value = 0.16
    target_labels = "Will Avail,Will Not Avail"
    target_values = "600,400"
    feature_labels = "Age,AnnualIncome,FamilyMembers"
    feature_values = "35,50000,3"

    context = {
        'num_records': num_records,
        'feature_summary': feature_summary,
        'target_distribution': target_distribution,
        'accuracy_score': accuracy_score,
        'confusion_matrix': confusion_matrix,
        'loss_value': loss_value,
        'target_labels': target_labels,
        'target_values': target_values,
        'feature_labels': feature_labels,
        'feature_values': feature_values,
    }
    return render(request, 'dashboard.html', context)