from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class BreastCancerRiskAssessment(models.Model):
    """
    Model for storing breast cancer risk assessment data
    Created based on Dr. Seyed Mahdi Mirtajaddini's assessment form
    """

    # Choice constants
    YES_NO_CHOICES = [
        ('y', 'Yes'),
        ('n', 'No'),
    ]

    ETHNICITY_CHOICES = [
        ('1', 'White'),
        ('2', 'African American'),
        ('3', 'Other race or ethnicity'),
    ]

    ALCOHOL_AMOUNT_CHOICES = [
        ('1', '1 drink'),
        ('2', '2 or more drinks'),
    ]

    HORMONE_THERAPY_TYPE_CHOICES = [
        ('1', 'Combined HT (Estrogen + Progesterone)'),
        ('2', 'ERT (Estrogen Replacement Therapy)'),
    ]

    BIOPSY_REPORT_CHOICES = [
        ('1', 'Fibrosis'),
        ('2', 'Simple cysts (fibrocystic changes)'),
        ('3', 'Mild hyperplasia'),
        ('4', 'Adenosis'),
        ('5', 'Phyllodes tumor'),
        ('6', 'A single papilloma'),
        ('7', 'Fat necrosis'),
        ('8', 'Duct ectasia'),
        ('9', 'Periductal fibrosis'),
        ('10', 'Squamous and apocrine metaplasia'),
        ('11', 'Epithelial-related calcifications'),
        ('12', 'Lipoma'),
        ('13', 'Hamartoma'),
        ('14', 'Hemangioma'),
        ('15', 'Neurofibroma'),
        ('16', 'Adenomyoepithelioma'),
        ('17', 'Mastitis (infection of the breast)'),
        ('18', 'Usual ductal hyperplasia (without atypia)'),
        ('19', 'Fibroadenoma'),
        ('20', 'Sclerosing adenosis'),
        ('21', 'Several papillomas (papillomatosis)'),
        ('22', 'Radial scar'),
        ('23', 'Atypical ductal hyperplasia (ADH)'),
        ('24', 'Atypical lobular hyperplasia (ALH)'),
        ('25', 'Lobular carcinoma in situ (LCIS)'),
    ]

    DIET_CHOICES = [
        ('1', 'High fat diets'),
        ('2', 'High in fruits and vegetables and calcium-rich dairy diets'),
        ('3', 'Low in red and processed meats'),
        ('4', 'Diets high in soy products'),
        ('5', 'None of mentioned above'),
    ]

    # Basic Information
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        help_text="Age in years"
    )
    gender = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Are you a woman?"
    )
    ethnicity = models.CharField(
        max_length=1,
        choices=ETHNICITY_CHOICES,
        help_text="Race and ethnicity"
    )

    # Lifestyle Factors
    alcohol = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Do you drink alcohol everyday?"
    )
    alcohol_amount = models.CharField(
        max_length=1,
        choices=ALCOHOL_AMOUNT_CHOICES,
        blank=True,
        null=True,
        help_text="How much alcoholic drink do you consume in a day?"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.1)],
        help_text="Weight in kilograms"
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.1)],
        help_text="Height in centimeters"
    )
    physical_activity = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Are you physically active?"
    )

    # Reproductive History
    children_before_30 = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had children before the age of 30?"
    )
    breastfeeding = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had breastfeeding that lasted for a year or more?"
    )
    birth_control = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had Birth Control Plan?"
    )
    hormone_therapy = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had post-menopausal hormone therapy?"
    )
    hormone_therapy_type = models.CharField(
        max_length=1,
        choices=HORMONE_THERAPY_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Type of hormone therapy"
    )
    menstrual_start = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Did your menstrual periods start before age 12?"
    )
    menopause_age = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Did you go through menopause after age 55?"
    )

    # Medical History
    breast_implants = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Do you have breast implants?"
    )
    radiation_therapy = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you been treated with radiation therapy to the chest for another cancer?"
    )
    dense_breast = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Has dense breast tissue been reported in your mammogram?"
    )
    des_exposure = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had exposure to diethylstilbestrol (DES)?"
    )
    breast_biopsy = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you ever had a breast biopsy for a reason other than cancer?"
    )
    biopsy_report = models.CharField(
        max_length=2,
        choices=BIOPSY_REPORT_CHOICES,
        blank=True,
        null=True,
        help_text="Which of the following is mentioned in your biopsy report?"
    )

    # Family History
    family_history_female = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had family history of breast cancer in your mother, sister or daughter?"
    )
    family_history_count = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text="How many of your family (mother, sister, daughter) have had breast cancer?"
    )
    family_history_male = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had family history of breast cancer in your father or brother?"
    )
    personal_history = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had personal history of breast cancer in one breast?"
    )

    # Physical Characteristics
    tall = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Are you taller than 170 centimeters?"
    )

    # Genetic Testing
    genetic_test = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Have you had genetic test for breast cancer related gene mutations (BRCA1, BRCA2)?"
    )
    genetic_test_result = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        blank=True,
        null=True,
        help_text="Is your test result positive for BRCA1 or BRCA2?"
    )

    # Diet and Lifestyle
    diet = models.CharField(
        max_length=1,
        choices=DIET_CHOICES,
        help_text="Which of the following do you use in your daily regimen?"
    )
    smoking = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Do you smoke 20 or more cigarettes per day?"
    )
    smoking_timing = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        blank=True,
        null=True,
        help_text="Did you begin smoking before the first pregnancy?"
    )
    night_shift = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Do you have night shift work?"
    )

    # Environmental Factors
    chemicals_environment = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Do you think chemicals in the environment are risk factors for breast cancer?"
    )
    controversial_factors = models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        help_text="Do you think antiperspirants, bras, or abortion are risk factors for breast cancer?"
    )

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'breast_cancer_risk_assessment'
        verbose_name = 'Breast Cancer Risk Assessment'
        verbose_name_plural = 'Breast Cancer Risk Assessments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Assessment for {self.get_gender_display()} aged {self.age} - {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def bmi(self):
        """Calculate BMI from weight and height"""
        if self.weight and self.height:
            height_m = float(self.height) / 100  # Convert cm to meters
            return round(float(self.weight) / (height_m ** 2), 2)
        return None

    @property
    def bmi_category(self):
        """Return BMI category"""
        bmi = self.bmi
        if bmi is None:
            return None
        elif bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def save(self, *args, **kwargs):
        """Override save to handle conditional field validation"""
        # Clear conditional fields if their parent field is 'n' or empty
        if self.alcohol != 'y':
            self.alcohol_amount = None

        if self.hormone_therapy != 'y':
            self.hormone_therapy_type = None

        if self.breast_biopsy != 'y':
            self.biopsy_report = None

        if self.family_history_female != 'y':
            self.family_history_count = None

        if self.genetic_test != 'y':
            self.genetic_test_result = None

        if self.smoking != 'y':
            self.smoking_timing = None

        super().save(*args, **kwargs)