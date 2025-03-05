# Generated by Django 5.1.6 on 2025-03-05 14:33

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('subject', models.CharField(max_length=200, verbose_name='موضوع')),
                ('message', models.TextField(verbose_name='پیام')),
                ('is_read', models.BooleanField(default=False, verbose_name='خوانده\u200cشده')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
            ],
            options={
                'verbose_name': 'پیام تماس',
                'verbose_name_plural': 'پیام\u200cهای تماس',
            },
        ),
        migrations.CreateModel(
            name='HomeOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider', models.BooleanField(default=True, verbose_name='نمایش اسلایدر')),
                ('best_viewed', models.BooleanField(default=True, verbose_name='نمایش پربازدیدها')),
                ('best_viewed_count', models.IntegerField(default=4, verbose_name='تعداد پربازدیدها')),
                ('new_products', models.BooleanField(default=True, verbose_name='نمایش محصولات جدید')),
                ('new_products_count', models.IntegerField(default=4, verbose_name='تعداد محصولات جدید')),
                ('best_sellers', models.BooleanField(default=True, verbose_name='نمایش پرفروش\u200cها')),
                ('best_sellers_count', models.IntegerField(default=4, verbose_name='تعداد پرفروش\u200cها')),
                ('offers', models.BooleanField(default=True, verbose_name='نمایش پر تخفیف\u200cها')),
                ('offers_count', models.IntegerField(default=4, verbose_name='تعداد پر تخفیف\u200cها')),
                ('random_products', models.BooleanField(default=True, verbose_name='نمایش محصولات تصادفی')),
                ('random_products_count', models.IntegerField(default=4, verbose_name='تعداد محصولات تصادفی')),
            ],
            options={
                'verbose_name': 'تنظیمات صفحه اصلی',
                'verbose_name_plural': 'تنظیمات صفحه اصلی',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('meta_title', models.CharField(max_length=200)),
                ('meta_description', models.TextField()),
                ('meta_keywords', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enamad', models.CharField(blank=True, max_length=1000, null=True)),
                ('telegram', models.CharField(blank=True, max_length=1000, null=True)),
                ('instagram', models.CharField(blank=True, max_length=1000, null=True)),
                ('phone', models.CharField(blank=True, max_length=1000, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(upload_to='media/logo/')),
                ('favicon', models.FileField(upload_to='media/favicon/', validators=[core.models.validate_favicon])),
                ('about_us', models.TextField(blank=True, null=True)),
                ('about_us_image', models.ImageField(blank=True, null=True, upload_to='media/about_us_image/')),
                ('telegram_bot', models.CharField(blank=True, max_length=1000, null=True)),
                ('contact_us', models.TextField(blank=True, null=True)),
                ('contact_us_image', models.ImageField(blank=True, null=True, upload_to='media/contact_us_image/')),
                ('clarity_tracking_id', models.CharField(blank=True, help_text='شناسه ردیابی Microsoft Clarity رو اینجا وارد کنید (مثل qgw9n7vv32)', max_length=20, null=True, verbose_name='شناسه ردیابی Clarity')),
                ('umami_id', models.CharField(blank=True, help_text='شناسه ردیابی Umami رو اینجا وارد کنید (مثل 1234567890)', max_length=255, null=True, verbose_name='شناسه ردیابی Umami')),
                ('goftino_id', models.CharField(blank=True, help_text='شناسه گفتینو رو اینجا وارد کنید (مثل 1234567890)', max_length=20, null=True, verbose_name='شناسه گفتینو')),
            ],
            options={
                'verbose_name': 'تنظیمات سایت',
                'verbose_name_plural': 'تنظیمات سایت',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt', models.CharField(max_length=200, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to='media/sliders/', verbose_name='تصویر')),
                ('link', models.URLField(blank=True, null=True, verbose_name='لینک')),
                ('active', models.BooleanField(default=True, verbose_name='فعال')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
            ],
            options={
                'verbose_name': 'اسلایدر',
                'verbose_name_plural': 'اسلایدرها',
            },
        ),
        migrations.CreateModel(
            name='SmsSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام کاربری')),
                ('password', models.CharField(blank=True, max_length=255, null=True, verbose_name='رمزعبور')),
                ('otp_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='کد الگو')),
            ],
            options={
                'verbose_name': 'تنظیمات سامانه پیامک',
                'verbose_name_plural': 'تنظیمات سامانه پیامک',
            },
        ),
        migrations.CreateModel(
            name='Zarinpal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_id', models.CharField(blank=True, max_length=255, null=True)),
                ('token', models.TextField(blank=True, null=True)),
                ('sandbox', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'تنظیمات زرین پال',
                'verbose_name_plural': 'تنظیمات زرین پال',
            },
        ),
    ]
