from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from PIL import Image

from .validators import ASCIIUsernameValidator



# LEVEL_COURSE = "Level course"
BACHELOR_DEGREE = _("Bachelor")
MASTER_DEGREE = _("Master")

LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (BACHELOR_DEGREE, _("Bachelor Degree")),
    (MASTER_DEGREE, _("Master Degree")),
)

FATHER = _("Father")
MOTHER = _("Mother")
BROTHER = _("Brother")
SISTER = _("Sister")
GRAND_MOTHER = _("Grand mother")
GRAND_FATHER = _("Grand father")
OTHER = _("Other")

RELATION_SHIP = (
    (FATHER, _("Father")),
    (MOTHER, _("Mother")),
    (BROTHER, _("Brother")),
    (SISTER, _("Sister")),
    (GRAND_MOTHER, _("Grand mother")),
    (GRAND_FATHER, _("Grand father")),
    (OTHER, _("Other")),
)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Program
class CustomUser(AbstractUser):
    # Add custom fields here, if needed
    pass
class SignupForm(UserCreationForm):
    # Custom fields for the User model
    gender = forms.ChoiceField(choices=User.GENDERS, required=True)
    phone = forms.CharField(max_length=60, required=False)
    address = forms.CharField(max_length=60, required=False)
    picture = forms.ImageField(required=False)
    
    # Custom fields for the Student model
    level = forms.ChoiceField(choices=Student.LEVEL, required=False)
    program = forms.ModelChoiceField(queryset=Program.objects.all(), required=False)

    # Determine whether the user is a student or lecturer during signup
    is_student = forms.BooleanField(required=False, initial=False)
    is_lecturer = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'gender', 'picture', 'is_student', 'is_lecturer', 'level', 'program', 'password1', 'password2']

    def save(self, commit=True):
        # Save user instance
        user = super().save(commit=False)
        
        # If you want to make sure the user is a student or lecturer
        if self.cleaned_data['is_student']:
            user.is_student = True
        if self.cleaned_data['is_lecturer']:
            user.is_lecturer = True

        if commit:
            user.save()

            # Now handle the Student model, if the user is a student
            if user.is_student:
                student = Student.objects.create(
                    student=user,
                    level=self.cleaned_data['level'],
                    program=self.cleaned_data['program']
                )

        return user
 
class Parent(models.Model):
    """
    Connect student with their parent, parents can
    only view their connected students information
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # What is the relationship between the student and
    # the parent (i.e. father, mother, brother, sister)
    relation_ship = models.TextField(choices=RELATION_SHIP, blank=True)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return self.user.username


class DepartmentHead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # department = models.ForeignKey('course.Program', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return "{}".format(self.user)
class User(AbstractUser):
    # Add custom fields if needed
    pass