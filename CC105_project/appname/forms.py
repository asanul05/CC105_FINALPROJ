from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PredictionForm(forms.Form):
    Age = forms.IntegerField(label='Age')
    GraduateOrNot = forms.ChoiceField(
        label='Graduate?',
        choices=[(0, 'No'), (1, 'Yes')]
    )
    AnnualIncome = forms.FloatField(label='Annual Income')
    FamilyMembers = forms.IntegerField(label='Number of Family Members')
    ChronicDiseases = forms.ChoiceField(
        label='Has Chronic Disease?',
        choices=[(0, 'No'), (1, 'Yes')]
    )
    FrequentFlyer = forms.ChoiceField(
        label='Frequent Flyer?',
        choices=[(0, 'No'), (1, 'Yes')]
    )
    EverTravelledAbroad = forms.ChoiceField(
        label='Ever Travelled Abroad?',
        choices=[(0, 'No'), (1, 'Yes')]
    )
    Employment_Type_Government_Sector = forms.ChoiceField(
        label='Government Employee?',
        choices=[(0, 'No'), (1, 'Yes')]
    )
    Employment_Type_Private_Sector_or_Self_Employed = forms.ChoiceField(
        label='Private/Self-Employed?',
        choices=[(0, 'No'), (1, 'Yes')]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for password fields
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ("username", "password1", "password2")