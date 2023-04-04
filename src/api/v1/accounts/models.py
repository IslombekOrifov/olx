from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from multiselectfield import MultiSelectField

from .validators import validate_phone
from .services import upload_avatar_path, upload_resume_path
from .enums import Licences, Levels, Languages
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=12,
        unique=True,
        db_index=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone = models.CharField(
        max_length=13, blank=True, 
        validators=[validate_phone], 
        db_index=True
    )
    balance = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    REQUIRED_FIELDS = []

    about = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, blank=True, null=True)
    other_skills = models.CharField(max_length=300, blank=True)
    hobby = models.CharField(max_length=300, blank=True)
    resume = models.FileField(upload_to=upload_resume_path, blank=True, null=True)

    edu1_name = models.CharField(max_length=250, blank=True)
    edu1_direction = models.CharField(max_length=150, blank=True)
    edu1_start_date = models.DateField(blank=True, null=True)
    edu1_end_date = models.DateField(blank=True, null=True)
    edu1_now = models.BooleanField(default=False)

    edu2_name = models.CharField(max_length=250, blank=True)
    edu2_direction = models.CharField(max_length=150, blank=True)
    edu2_start_date = models.DateField(blank=True, null=True)
    edu2_end_date = models.DateField(blank=True, null=True)
    edu2_now = models.BooleanField(default=False)
    
    licence_category = MultiSelectField(
        choices=Licences.choices(), max_choices=3, 
        max_length=3, blank=True
    )
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.email} > {self.username}'


    def save(self, *args, **kwargs):
        self.edu1_name = ' '.join(self.edu1_name.strip().split())
        self.edu2_name = ' '.join(self.edu2_name.strip().split())
        self.about = ' '.join(self.about.strip().split())
        self.other_skills = ' '.join(self.other_skills.strip().split())
        self.hobby = ' '.join(self.hobby.strip().split())
        self.edu1_direction = ' '.join(self.edu1_direction.strip().split())
        return super().save(*args, **kwargs)


class UserLanguage(models.Model):   
    language = models.CharField(max_length=3, choices=Languages.choices())
    level = models.CharField(max_length=3, choices=Levels.choices())
    date_created = models.DateField(auto_now_add=True)

    user = models.ForeignKey(CustomUser, related_name='languages', on_delete=models.CASCADE)

    def __str__(self):
        return self.language




class Experience(models.Model):
    user = models.ForeignKey(CustomUser, related_name='experiences', on_delete=models.CASCADE)
    
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    work_start_date = models.DateField()
    work_end_date = models.DateField(blank=True, null=True)
    work_now = models.BooleanField(default=False)
    work_duties = models.CharField(max_length=500, blank=True)

    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.role


