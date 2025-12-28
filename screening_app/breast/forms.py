from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .models import BreastCancerRiskAssessment


class BreastCancerRiskAssessmentForm(forms.ModelForm):
    """
    Form for breast cancer risk assessment
    Created based on Dr. Seyed Mahdi Mirtajaddini's assessment criteria
    """

    class Meta:
        model = BreastCancerRiskAssessment
        fields = [
            # Basic Information
            'age', 'gender', 'ethnicity',

            # Lifestyle Factors
            'alcohol', 'alcohol_amount', 'weight', 'height', 'physical_activity',

            # Reproductive History
            'children_before_30', 'breastfeeding', 'birth_control', 
            'hormone_therapy', 'hormone_therapy_type', 'menstrual_start', 'menopause_age',

            # Medical History
            'breast_implants', 'radiation_therapy', 'dense_breast', 'des_exposure',
            'breast_biopsy', 'biopsy_report',

            # Family History
            'family_history_female', 'family_history_count', 'family_history_male', 'personal_history',

            # Physical Characteristics
            'tall',

            # Genetic Testing
            'genetic_test', 'genetic_test_result',

            # Diet and Lifestyle
            'diet', 'smoking', 'smoking_timing', 'night_shift',

            # Environmental Factors
            'chemicals_environment', 'controversial_factors'
        ]

        widgets = {
            # Basic Information
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age',
                'min': '1',
                'max': '120'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'data-toggle': 'tooltip',
                'title': 'Are you a woman?'
            }),
            'ethnicity': forms.Select(attrs={
                'class': 'form-control'
            }),

            # Lifestyle Factors
            'alcohol': forms.Select(attrs={
                'class': 'form-control',
                'data-conditional': 'true',
                'data-target': 'alcohol_amount'
            }),
            'alcohol_amount': forms.Select(attrs={
                'class': 'form-control conditional-field',
                'data-parent': 'alcohol'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kilograms',
                'step': '0.1',
                'min': '0.1'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in centimeters',
                'step': '0.1',
                'min': '0.1'
            }),
            'physical_activity': forms.Select(attrs={
                'class': 'form-control'
            }),

            # Reproductive History
            'children_before_30': forms.Select(attrs={
                'class': 'form-control'
            }),
            'breastfeeding': forms.Select(attrs={
                'class': 'form-control'
            }),
            'birth_control': forms.Select(attrs={
                'class': 'form-control'
            }),
            'hormone_therapy': forms.Select(attrs={
                'class': 'form-control',
                'data-conditional': 'true',
                'data-target': 'hormone_therapy_type'
            }),
            'hormone_therapy_type': forms.Select(attrs={
                'class': 'form-control conditional-field',
                'data-parent': 'hormone_therapy'
            }),
            'menstrual_start': forms.Select(attrs={
                'class': 'form-control'
            }),
            'menopause_age': forms.Select(attrs={
                'class': 'form-control'
            }),

            # Medical History
            'breast_implants': forms.Select(attrs={
                'class': 'form-control'
            }),
            'radiation_therapy': forms.Select(attrs={
                'class': 'form-control'
            }),
            'dense_breast': forms.Select(attrs={
                'class': 'form-control'
            }),
            'des_exposure': forms.Select(attrs={
                'class': 'form-control'
            }),
            'breast_biopsy': forms.Select(attrs={
                'class': 'form-control',
                'data-conditional': 'true',
                'data-target': 'biopsy_report'
            }),
            'biopsy_report': forms.Select(attrs={
                'class': 'form-control conditional-field',
                'data-parent': 'breast_biopsy'
            }),

            # Family History
            'family_history_female': forms.Select(attrs={
                'class': 'form-control',
                'data-conditional': 'true',
                'data-target': 'family_history_count'
            }),
            'family_history_count': forms.NumberInput(attrs={
                'class': 'form-control conditional-field',
                'data-parent': 'family_history_female',
                'placeholder': 'Number of relatives',
                'min': '1'
            }),
            'family_history_male': forms.Select(attrs={
                'class': 'form-control'
            }),
            'personal_history': forms.Select(attrs={
                'class': 'form-control'
            }),

            # Physical Characteristics
            'tall': forms.Select(attrs={
                'class': 'form-control'
            }),

            # Genetic Testing
            'genetic_test': forms.Select(attrs={
                'class': 'form-control',
                'data-conditional': 'true',
                'data-target': 'genetic_test_result'
            }),
            'genetic_test_result': forms.Select(attrs={
                'class': 'form-control conditional-field',
                'data-parent': 'genetic_test'
            }),

            # Diet and Lifestyle
            'diet': forms.Select(attrs={
                'class': 'form-control'
            }),
            'smoking': forms.Select(attrs={
                'class': 'form-control',
                'data-conditional': 'true',
                'data-target': 'smoking_timing'
            }),
            'smoking_timing': forms.Select(attrs={
                'class': 'form-control conditional-field',
                'data-parent': 'smoking'
            }),
            'night_shift': forms.Select(attrs={
                'class': 'form-control'
            }),

            # Environmental Factors
            'chemicals_environment': forms.Select(attrs={
                'class': 'form-control'
            }),
            'controversial_factors': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

        labels = {
            'age': 'How old are you?',
            'gender': 'Are you a woman?',
            'ethnicity': 'What is your race and ethnicity?',
            'alcohol': 'Do you drink alcohol everyday?',
            'alcohol_amount': 'How much alcoholic drink do you consume in a day?',
            'weight': 'How much is your weight (Kg)?',
            'height': 'How tall are you (Cm)?',
            'physical_activity': 'Are you physically active?',
            'children_before_30': 'Have you had children before the age of 30?',
            'breastfeeding': 'Have you had breastfeeding that lasted for a year or more?',
            'birth_control': 'Have you had Birth Control Plan?',
            'hormone_therapy': 'Have you had post-menopausal hormone therapy?',
            'hormone_therapy_type': 'Type of hormone therapy:',
            'menstrual_start': 'Did your menstrual periods start before age 12?',
            'menopause_age': 'Did you go through menopause after age 55?',
            'breast_implants': 'Do you have breast implants?',
            'radiation_therapy': 'Have you been treated with radiation therapy to the chest for another cancer?',
            'dense_breast': 'Has dense breast tissue been reported in your mammogram?',
            'des_exposure': 'Have you had exposure to diethylstilbestrol (DES)?',
            'breast_biopsy': 'Have you ever had a breast biopsy for a reason other than cancer?',
            'biopsy_report': 'Which of the following is mentioned in your biopsy report?',
            'family_history_female': 'Have you had family history of breast cancer in your mother, sister or daughter?',
            'family_history_count': 'How many of your family (mother, sister, daughter) have had breast cancer?',
            'family_history_male': 'Have you had family history of breast cancer in your father or brother?',
            'personal_history': 'Have you had personal history of breast cancer in one breast?',
            'tall': 'Are you taller than 170 centimeters?',
            'genetic_test': 'Have you had genetic test for breast cancer related gene mutations (BRCA1, BRCA2)?',
            'genetic_test_result': 'Is your test result positive for BRCA1 or BRCA2?',
            'diet': 'Which of the following do you use in your daily regimen?',
            'smoking': 'Do you smoke 20 or more cigarettes per day?',
            'smoking_timing': 'Did you begin smoking before the first pregnancy?',
            'night_shift': 'Do you have night shift work?',
            'chemicals_environment': 'Do you think chemicals in the environment are risk factors for breast cancer?',
            'controversial_factors': 'Do you think antiperspirants, bras, or abortion are risk factors for breast cancer?',
        }

        help_texts = {
            'age': 'Enter your current age in years',
            'weight': 'Enter your weight in kilograms (e.g., 65.5)',
            'height': 'Enter your height in centimeters (e.g., 165.0)',
            'physical_activity': 'Physically active means: 150-300 minutes of moderate intensity OR 75-150 minutes of vigorous intensity activity each week',
            'alcohol_amount': 'One alcoholic drink = 12 oz beer (5% alcohol) OR 5 oz wine (12% alcohol) OR 1.5 oz distilled spirits (40% alcohol)',
            'birth_control': 'Includes: oral contraceptives, progesterone shots, implants, hormone-releasing IUDs, patches, vaginal rings',
            'hormone_therapy': 'Combined HT: Estrogen + progesterone for women with uterus. ERT: Estrogen alone for women who had hysterectomy',
            'des_exposure': 'From 1940s-early 1970s, some pregnant women were given DES to lower miscarriage chances',
            'family_history_count': 'Count only mother, sister, or daughter with breast cancer history',
            'tall': 'Average height for adult women is around 160-165 cm. Taller women are those above 170 cm',
            'genetic_test': 'BRCA1 and BRCA2 are genes that help repair damaged DNA. Mutations increase breast cancer risk',
            'chemicals_environment': 'Includes estrogen-like substances in plastics, phthalates, parabens, pesticides, and PCBs',
            'controversial_factors': 'Research shows little to no evidence that antiperspirants, bras, or abortion increase breast cancer risk',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make conditional fields not required initially
        conditional_fields = [
            'alcohol_amount', 'hormone_therapy_type', 'biopsy_report',
            'family_history_count', 'genetic_test_result', 'smoking_timing'
        ]

        for field_name in conditional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False

    def clean_age(self):
        """Validate age field"""
        age = self.cleaned_data.get('age')
        if age:
            if age < 1 or age > 120:
                raise ValidationError('Age must be between 1 and 120 years.')
        return age

    def clean_weight(self):
        """Validate weight field"""
        weight = self.cleaned_data.get('weight')
        if weight:
            if weight <= 0:
                raise ValidationError('Weight must be greater than 0.')
            if weight > 999:
                raise ValidationError('Please enter a valid weight.')
        return weight

    def clean_height(self):
        """Validate height field"""
        height = self.cleaned_data.get('height')
        if height:
            if height <= 0:
                raise ValidationError('Height must be greater than 0.')
            if height > 999:
                raise ValidationError('Please enter a valid height.')
        return height

    def clean_family_history_count(self):
        """Validate family history count"""
        family_history_female = self.cleaned_data.get('family_history_female')
        family_history_count = self.cleaned_data.get('family_history_count')

        if family_history_female == 'y':
            if not family_history_count:
                raise ValidationError('Please specify how many family members have had breast cancer.')
            if family_history_count < 1:
                raise ValidationError('Count must be at least 1.')

        return family_history_count

    def clean_alcohol_amount(self):
        """Validate alcohol amount field"""
        alcohol = self.cleaned_data.get('alcohol')
        alcohol_amount = self.cleaned_data.get('alcohol_amount')

        if alcohol == 'y' and not alcohol_amount:
            raise ValidationError('Please specify your daily alcohol consumption amount.')

        return alcohol_amount

    def clean_hormone_therapy_type(self):
        """Validate hormone therapy type"""
        hormone_therapy = self.cleaned_data.get('hormone_therapy')
        hormone_therapy_type = self.cleaned_data.get('hormone_therapy_type')

        if hormone_therapy == 'y' and not hormone_therapy_type:
            raise ValidationError('Please specify the type of hormone therapy.')

        return hormone_therapy_type

    def clean_biopsy_report(self):
        """Validate biopsy report field"""
        breast_biopsy = self.cleaned_data.get('breast_biopsy')
        biopsy_report = self.cleaned_data.get('biopsy_report')

        if breast_biopsy == 'y' and not biopsy_report:
            raise ValidationError('Please select what was mentioned in your biopsy report.')

        return biopsy_report

    def clean_genetic_test_result(self):
        """Validate genetic test result"""
        genetic_test = self.cleaned_data.get('genetic_test')
        genetic_test_result = self.cleaned_data.get('genetic_test_result')

        if genetic_test == 'y' and not genetic_test_result:
            raise ValidationError('Please specify your genetic test result.')

        return genetic_test_result

    def clean_smoking_timing(self):
        """Validate smoking timing"""
        smoking = self.cleaned_data.get('smoking')
        smoking_timing = self.cleaned_data.get('smoking_timing')

        if smoking == 'y' and not smoking_timing:
            raise ValidationError('Please specify when you began smoking.')

        return smoking_timing

    def clean(self):
        """Additional form-wide validation"""
        cleaned_data = super().clean()

        # BMI calculation and validation
        weight = cleaned_data.get('weight')
        height = cleaned_data.get('height')

        if weight and height:
            height_m = float(height) / 100  # Convert cm to meters
            bmi = float(weight) / (height_m ** 2)

            if bmi < 10 or bmi > 60:
                raise ValidationError(
                    'The calculated BMI seems unusual. Please check your weight and height values.'
                )

        return cleaned_data


class AssessmentSearchForm(forms.Form):
    """
    Form for searching and filtering assessments
    """
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by age or ethnicity...'
        })
    )

    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )

    age_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min age'
        }),
        label='Minimum Age'
    )

    age_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max age'
        }),
        label='Maximum Age'
    )

    ethnicity = forms.ChoiceField(
        choices=[('', 'All ethnicities')] + BreastCancerRiskAssessment.ETHNICITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    gender = forms.ChoiceField(
        choices=[('', 'All genders')] + BreastCancerRiskAssessment.YES_NO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class RiskCalculatorForm(forms.Form):
    """
    Simplified form for quick risk calculation
    """
    age = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter age'
        })
    )

    family_history = forms.ChoiceField(
        choices=BreastCancerRiskAssessment.YES_NO_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Family history of breast cancer?'
    )

    genetic_mutation = forms.ChoiceField(
        choices=BreastCancerRiskAssessment.YES_NO_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Known BRCA1/BRCA2 mutation?'
    )

    personal_history = forms.ChoiceField(
        choices=BreastCancerRiskAssessment.YES_NO_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Personal history of breast cancer?'
    )