from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from re_work.user.manager import UserManager


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField('Name', max_length=150, null=True, blank=True)
    user_image = models.ImageField(upload_to='user_image/', blank=True, null=True)
    phone = models.PositiveBigIntegerField('Phone Number', unique=True, blank=True, null=True)
    address = models.CharField('Address', max_length=80, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class UserType(models.IntegerChoices):
        CLIENT = 1, _('Client')
        ADMIN = 2, _('Admin')
        SCRIPT_WRITER = 3, _('Script Writer')
        VIDEO_EDITOR = 4, _('Video Editor')
        FULL_STACK = 5, _('Full Stack')
        STAFF_ADMIN = 6, _('Staff Admin')

    user_type = models.IntegerField(choices=UserType.choices, null=True, blank=True)
    is_verified = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.user_type == self.UserType.ADMIN

    @property
    def is_client(self):
        "Is the user a client member?"
        return self.user_type == self.UserType.CLIENT

    @property
    def is_staff_admin(self):
        "Is the user a staff admin member?"
        return self.user_type == self.UserType.STAFF_ADMIN

    @property
    def is_script_writer(self):
        "Is the user a developer member?"
        return self.user_type == self.UserType.SCRIPT_WRITER

    @property
    def is_video_editor(self):
        "Is the user a developer member?"
        return self.user_type == self.UserType.VIDEO_EDITOR

    @property
    def is_full_stack(self):
        "Is the user a developer member?"
        return self.user_type == self.UserType.FULL_STACK

    # def get_gender(self):
    #     if not self.gender:
    #         return 'Male'
    #     else:
    #         return self.gender

    def get_image(self):
        if not self.user_image:
            return '/media/user_image/user.jpg'
        else:
            return self.user_image
