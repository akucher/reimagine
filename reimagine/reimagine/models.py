from django.db import models


class LinkedIn(models.Model):
    user_name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=250, null=True, blank=True)
    token = models.CharField(max_length=250, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

class LinkedInData(models.Model):
    user_name = models.CharField(max_length=50, null=True, blank=True)
    data = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)