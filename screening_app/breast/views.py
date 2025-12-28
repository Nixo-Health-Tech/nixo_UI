from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import csv
from datetime import datetime, timedelta

from .models import BreastCancerRiskAssessment
from .forms import BreastCancerRiskAssessmentForm


class BreastCancerAssessmentCreateView(CreateView):
    """
    View for creating a new breast cancer risk assessment
    """
    model = BreastCancerRiskAssessment
    form_class = BreastCancerRiskAssessmentForm
    template_name = 'screening/breast/assessment_form.html'
    success_url = reverse_lazy('breast:assessment_success')

    def form_valid(self, form):
        """Handle successful form submission"""
        self.object = form.save()
        messages.success(
            self.request, 
            'Breast cancer risk assessment completed successfully!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(
            self.request,
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Breast Cancer Risk Assessment'
        context['doctor_name'] = 'Dr. Seyed Mahdi Mirtajaddini'
        context['doctor_specialty'] = 'Specialist in Internal Medicine'
        return context


class BreastCancerAssessmentDetailView(DetailView):
    """
    View for displaying a single assessment result
    """
    model = BreastCancerRiskAssessment
    template_name = 'screening/breast/assessment_detail.html'
    context_object_name = 'assessment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessment = self.object

        # Calculate risk factors
        context['risk_analysis'] = self.calculate_risk_factors(assessment)
        context['recommendations'] = self.get_recommendations(assessment)
        context['page_title'] = f'Assessment Results - {assessment.created_at.strftime("%Y-%m-%d")}'

        return context

    def calculate_risk_factors(self, assessment):
        """
        Calculate and categorize risk factors based on assessment data
        """
        high_risk_factors = []
        moderate_risk_factors = []
        low_risk_factors = []
        protective_factors = []

        # Age risk
        if assessment.age >= 65:
            high_risk_factors.append("Age 65 or older")
        elif assessment.age >= 50:
            moderate_risk_factors.append("Age 50-64")

        # Gender risk
        if assessment.gender == 'y':
            moderate_risk_factors.append("Female gender")

        # Family history
        if assessment.family_history_female == 'y':
            if assessment.family_history_count and assessment.family_history_count > 1:
                high_risk_factors.append(f"Multiple female relatives with breast cancer ({assessment.family_history_count})")
            else:
                moderate_risk_factors.append("Family history of breast cancer (female relatives)")

        if assessment.family_history_male == 'y':
            moderate_risk_factors.append("Family history of breast cancer (male relatives)")

        # Personal history
        if assessment.personal_history == 'y':
            high_risk_factors.append("Personal history of breast cancer")

        # Genetic factors
        if assessment.genetic_test_result == 'y':
            high_risk_factors.append("BRCA1/BRCA2 mutation positive")

        # Reproductive factors
        if assessment.menstrual_start == 'y':
            moderate_risk_factors.append("Early menarche (before age 12)")

        if assessment.menopause_age == 'y':
            moderate_risk_factors.append("Late menopause (after age 55)")

        if assessment.children_before_30 == 'n':
            moderate_risk_factors.append("No children before age 30")

        # Protective factors
        if assessment.breastfeeding == 'y':
            protective_factors.append("Breastfeeding for a year or more")

        if assessment.physical_activity == 'y':
            protective_factors.append("Regular physical activity")

        # Lifestyle factors
        if assessment.alcohol == 'y':
            if assessment.alcohol_amount == '2':
                moderate_risk_factors.append("Heavy alcohol consumption (2+ drinks daily)")
            else:
                low_risk_factors.append("Moderate alcohol consumption (1 drink daily)")

        if assessment.smoking == 'y':
            if assessment.smoking_timing == 'y':
                moderate_risk_factors.append("Heavy smoking started before first pregnancy")
            else:
                low_risk_factors.append("Heavy smoking (20+ cigarettes/day)")

        # BMI calculation
        if assessment.bmi:
            if assessment.bmi >= 30:
                moderate_risk_factors.append(f"Obesity (BMI: {assessment.bmi})")
            elif assessment.bmi >= 25:
                low_risk_factors.append(f"Overweight (BMI: {assessment.bmi})")

        # Medical history
        if assessment.dense_breast == 'y':
            moderate_risk_factors.append("Dense breast tissue")

        if assessment.radiation_therapy == 'y':
            moderate_risk_factors.append("Previous chest radiation therapy")

        if assessment.hormone_therapy == 'y':
            if assessment.hormone_therapy_type == '1':
                moderate_risk_factors.append("Combined hormone therapy (Estrogen + Progesterone)")
            else:
                low_risk_factors.append("Estrogen replacement therapy")

        # Biopsy results
        if assessment.biopsy_report in ['23', '24', '25']:  # Atypical hyperplasia, LCIS
            high_risk_factors.append("Atypical hyperplasia or LCIS on biopsy")
        elif assessment.biopsy_report in ['20', '21', '22']:  # Sclerosing adenosis, papillomatosis, radial scar
            moderate_risk_factors.append("Proliferative breast lesions without atypia")

        return {
            'high_risk': high_risk_factors,
            'moderate_risk': moderate_risk_factors,
            'low_risk': low_risk_factors,
            'protective': protective_factors
        }

    def get_recommendations(self, assessment):
        """
        Generate personalized recommendations based on risk assessment
        """
        recommendations = []

        # Age-based screening
        if assessment.age >= 50:
            recommendations.append({
                'category': 'Screening',
                'recommendation': 'Annual mammography screening is recommended',
                'priority': 'high'
            })
        elif assessment.age >= 40:
            recommendations.append({
                'category': 'Screening',
                'recommendation': 'Discuss mammography screening options with your doctor',
                'priority': 'moderate'
            })

        # High-risk recommendations
        if (assessment.genetic_test_result == 'y' or 
            assessment.personal_history == 'y' or
            (assessment.family_history_female == 'y' and 
             assessment.family_history_count and assessment.family_history_count > 1)):

            recommendations.append({
                'category': 'High-Risk Management',
                'recommendation': 'Consider consultation with a breast specialist or genetic counselor',
                'priority': 'high'
            })

            recommendations.append({
                'category': 'Enhanced Screening',
                'recommendation': 'May benefit from MRI screening in addition to mammography',
                'priority': 'high'
            })

        # Lifestyle recommendations
        if assessment.physical_activity == 'n':
            recommendations.append({
                'category': 'Lifestyle',
                'recommendation': 'Increase physical activity to 150-300 minutes of moderate exercise weekly',
                'priority': 'moderate'
            })

        if assessment.alcohol == 'y':
            recommendations.append({
                'category': 'Lifestyle',
                'recommendation': 'Consider limiting alcohol consumption to reduce breast cancer risk',
                'priority': 'moderate'
            })

        if assessment.smoking == 'y':
            recommendations.append({
                'category': 'Lifestyle',
                'recommendation': 'Smoking cessation is strongly recommended',
                'priority': 'high'
            })

        if assessment.bmi and assessment.bmi >= 25:
            recommendations.append({
                'category': 'Weight Management',
                'recommendation': 'Maintain a healthy weight through diet and exercise',
                'priority': 'moderate'
            })

        # Diet recommendations
        if assessment.diet == '1':  # High fat diet
            recommendations.append({
                'category': 'Diet',
                'recommendation': 'Consider adopting a diet rich in fruits, vegetables, and whole grains',
                'priority': 'moderate'
            })

        return recommendations


class BreastCancerAssessmentListView(ListView):
    """
    View for listing all assessments (for admin/healthcare providers)
    """
    model = BreastCancerRiskAssessment
    template_name = 'screening/breast/assessment_list.html'
    context_object_name = 'assessments'
    paginate_by = 20

    def get_queryset(self):
        queryset = BreastCancerRiskAssessment.objects.all()

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(age__icontains=search_query) |
                Q(ethnicity__icontains=search_query)
            )

        # Filter by date range
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_assessments'] = BreastCancerRiskAssessment.objects.count()
        context['search_query'] = self.request.GET.get('search', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        return context


def assessment_success(request):
    """
    Success page after completing assessment
    """
    return render(request, 'screening/breast/assessment_success.html', {
        'page_title': 'Assessment Completed Successfully'
    })


def assessment_statistics(request):
    """
    View for displaying assessment statistics
    """
    stats = {
        'total_assessments': BreastCancerRiskAssessment.objects.count(),
        'assessments_last_month': BreastCancerRiskAssessment.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'avg_age': BreastCancerRiskAssessment.objects.aggregate(
            avg_age=Avg('age')
        )['avg_age'],
        'gender_distribution': BreastCancerRiskAssessment.objects.values('gender').annotate(
            count=Count('gender')
        ),
        'ethnicity_distribution': BreastCancerRiskAssessment.objects.values('ethnicity').annotate(
            count=Count('ethnicity')
        ),
        'family_history_stats': {
            'female_family_history': BreastCancerRiskAssessment.objects.filter(
                family_history_female='y'
            ).count(),
            'male_family_history': BreastCancerRiskAssessment.objects.filter(
                family_history_male='y'
            ).count(),
            'personal_history': BreastCancerRiskAssessment.objects.filter(
                personal_history='y'
            ).count(),
        }
    }

    return render(request, 'screening/breast/statistics.html', {
        'stats': stats,
        'page_title': 'Assessment Statistics'
    })


@require_http_methods(["GET"])
def export_assessments_csv(request):
    """
    Export assessments data to CSV format
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="breast_cancer_assessments_{datetime.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)

    # Write header
    writer.writerow([
        'ID', 'Date Created', 'Age', 'Gender', 'Ethnicity', 'BMI', 'BMI Category',
        'Family History Female', 'Family History Male', 'Personal History',
        'Genetic Test Result', 'Physical Activity', 'Alcohol Consumption',
        'Smoking', 'Dense Breast', 'Hormone Therapy'
    ])

    # Write data
    for assessment in BreastCancerRiskAssessment.objects.all():
        writer.writerow([
            assessment.id,
            assessment.created_at.strftime('%Y-%m-%d'),
            assessment.age,
            assessment.get_gender_display(),
            assessment.get_ethnicity_display(),
            assessment.bmi or 'N/A',
            assessment.bmi_category or 'N/A',
            assessment.get_family_history_female_display(),
            assessment.get_family_history_male_display(),
            assessment.get_personal_history_display(),
            assessment.get_genetic_test_result_display() if assessment.genetic_test_result else 'Not tested',
            assessment.get_physical_activity_display(),
            assessment.get_alcohol_display(),
            assessment.get_smoking_display(),
            assessment.get_dense_breast_display(),
            assessment.get_hormone_therapy_display()
        ])

    return response


@csrf_exempt
def ajax_validate_field(request):
    """
    AJAX endpoint for real-time field validation
    """
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')

        # Basic validation logic
        errors = []

        if field_name == 'age':
            try:
                age = int(field_value)
                if age < 1 or age > 120:
                    errors.append('Age must be between 1 and 120 years')
            except (ValueError, TypeError):
                errors.append('Please enter a valid age')

        elif field_name == 'weight':
            try:
                weight = float(field_value)
                if weight <= 0:
                    errors.append('Weight must be greater than 0')
            except (ValueError, TypeError):
                errors.append('Please enter a valid weight')

        elif field_name == 'height':
            try:
                height = float(field_value)
                if height <= 0:
                    errors.append('Height must be greater than 0')
            except (ValueError, TypeError):
                errors.append('Please enter a valid height')

        return JsonResponse({
            'valid': len(errors) == 0,
            'errors': errors
        })

    return JsonResponse({'error': 'Invalid request method'})


def risk_calculator(request):
    """
    Interactive risk calculator page
    """
    return render(request, 'screening/breast/risk_calculator.html', {
        'page_title': 'Breast Cancer Risk Calculator',
        'form_choices': {
            'ethnicity_choices': BreastCancerRiskAssessment.ETHNICITY_CHOICES,
            'alcohol_amount_choices': BreastCancerRiskAssessment.ALCOHOL_AMOUNT_CHOICES,
            'hormone_therapy_type_choices': BreastCancerRiskAssessment.HORMONE_THERAPY_TYPE_CHOICES,
            'biopsy_report_choices': BreastCancerRiskAssessment.BIOPSY_REPORT_CHOICES,
            'diet_choices': BreastCancerRiskAssessment.DIET_CHOICES,
        }
    })


class BreastCancerAssessmentUpdateView(UpdateView):
    """
    View for updating an existing assessment
    """
    model = BreastCancerRiskAssessment
    form_class = BreastCancerRiskAssessmentForm
    template_name = 'screening/breast/assessment_update.html'

    def get_success_url(self):
        return reverse_lazy('breast_cancer:assessment_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Assessment updated successfully!')
        return super().form_valid(form)


class BreastCancerAssessmentDeleteView(DeleteView):
    """
    View for deleting an assessment
    """
    model = BreastCancerRiskAssessment
    template_name = 'screening/breast/assessment_confirm_delete.html'
    success_url = reverse_lazy('breast_cancer:assessment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Assessment deleted successfully!')
        return super().delete(request, *args, **kwargs)


def dashboard(request):
    """
    Dashboard view with overview of assessments and quick stats
    """
    # Recent assessments
    recent_assessments = BreastCancerRiskAssessment.objects.order_by('-created_at')[:5]

    # Quick statistics
    total_assessments = BreastCancerRiskAssessment.objects.count()
    high_risk_count = BreastCancerRiskAssessment.objects.filter(
        Q(genetic_test_result='y') | 
        Q(personal_history='y') |
        Q(family_history_count__gt=1)
    ).count()

    # Age distribution
    age_groups = {
        '20-29': BreastCancerRiskAssessment.objects.filter(age__range=(20, 29)).count(),
        '30-39': BreastCancerRiskAssessment.objects.filter(age__range=(30, 39)).count(),
        '40-49': BreastCancerRiskAssessment.objects.filter(age__range=(40, 49)).count(),
        '50-59': BreastCancerRiskAssessment.objects.filter(age__range=(50, 59)).count(),
        '60+': BreastCancerRiskAssessment.objects.filter(age__gte=60).count(),
    }

    context = {
        'page_title': 'Breast Cancer Risk Assessment Dashboard',
        'recent_assessments': recent_assessments,
        'total_assessments': total_assessments,
        'high_risk_count': high_risk_count,
        'age_groups': age_groups,
        'doctor_name': 'Dr. Seyed Mahdi Mirtajaddini',
        'doctor_specialty': 'Specialist in Internal Medicine'
    }

    return render(request, 'screening/breast/dashboard.html', context)