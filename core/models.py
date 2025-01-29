from django.db import models

class Slider(models.Model):
    alt = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/sliders/')
    link = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alt


class SiteSettings(models.Model):
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enamad = models.CharField(max_length=1000, blank=True, null=True)
    telegram = models.CharField(max_length=1000, blank=True, null=True)
    instagram = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=1000, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='media/logo/')
    favicon = models.ImageField(upload_to='media/favicon/')
    about_us = models.TextField(blank=True, null=True)
    about_us_image = models.ImageField(upload_to='media/about_us_image/', blank=True, null=True)
    telegram_bot = models.CharField(max_length=1000, blank=True, null=True)
    contact_us = models.TextField(blank=True, null=True)
    contact_us_image = models.ImageField(upload_to='media/contact_us_image/', blank=True, null=True)
    def __str__(self):
        return self.meta_title



