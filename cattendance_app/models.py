# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.db import models

# class User(AbstractUser):
#     """
#     Custom user model.
#     Inherits first_name, last_name, email from AbstractUser.
#     Adds user_type to distinguish between student and teacher.
#     """

#     USER_TYPE_CHOICES = (
#         ('student', 'Student'),
#         ('teacher', 'Teacher'),
#     )

#     user_type = models.CharField(
#         max_length=10,
#         choices=USER_TYPE_CHOICES,
#         default='student',
#         verbose_name='User Type'
#     )

#     # Fix for related_name clashes with auth.User
#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_set',
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups'
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions_set',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions'
#     )

#     def __str__(self):
#         return self.email or self.username


# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

#     def __str__(self):
#         return f"Student Profile for {self.user.email}"


# class TeacherProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

#     def __str__(self):
#         return f"Teacher Profile for {self.user.email}"
