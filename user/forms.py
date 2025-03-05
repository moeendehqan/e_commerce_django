from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Otp
from .models import Address


class OtpForm(forms.Form):
    mobile = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='شماره موبایل'
    )

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        
        if not mobile.startswith('09'):
            raise forms.ValidationError('شماره موبایل باید با 09 شروع شود.')
        if len(mobile) != 11:
            raise forms.ValidationError('شماره موبایل باید 11 رقم باشد.')
        if not mobile.isdigit():
            raise forms.ValidationError('شماره موبایل فقط باید شامل اعداد باشد.')
        if User.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        if Otp.objects.filter(
            mobile=mobile, 
            is_used=False, 
            created_at__gt=timezone.now() - timedelta(minutes=2)
        ).exists():
            raise forms.ValidationError('لطفاً 2 دقیقه صبر کنید و دوباره امتحان کنید.')
        
        return mobile

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, label='نام کاربری')
    otp = forms.CharField(max_length=4, label='کد تأیید')
    gender = forms.ChoiceField(choices=[('male', 'مرد'), ('female', 'زن')], label='جنسیت')
    email = forms.EmailField(required=False, label='ایمیل (اختیاری)')
    first_name = forms.CharField(max_length=100, required=False, label='نام (اختیاری)')
    last_name = forms.CharField(max_length=100, required=False, label='نام خانوادگی (اختیاری)')
    password = forms.CharField(max_length=16, widget=forms.PasswordInput, label='رمز عبور')
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput, label='تکرار رمز عبور')
    invite_code = forms.CharField(max_length=6, required=False, label='کد دعوت (اختیاری)')

    def clean_otp(self):
        otp = self.cleaned_data['otp']
        if not Otp.objects.filter(
            otp=otp,
            is_used=False,
            created_at__gt=timezone.now() - timedelta(minutes=10)
        ).exists():
            raise forms.ValidationError('کد تأیید نامعتبر است یا منقضی شده.')
        return otp

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('رمز عبور و تکرار آن مطابقت ندارند.')
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً ثبت شده است.')
        return username

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        if invite_code and not User.objects.filter(referral_code=invite_code).exists():
            raise forms.ValidationError('کد دعوت نامعتبر است.')
        return invite_code

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد.')
        if password.isdigit() or password.isalpha():
            raise forms.ValidationError('رمز عبور باید ترکیبی از حروف و اعداد باشد.')
        return password

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender not in ['male', 'female']:
            raise forms.ValidationError('جنسیت نامعتبر است.')
        return gender
    


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='نام کاربری')
    password = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput,
        label='رمز عبور'
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است.')
        return cleaned_data




class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'city', 'province', 'full_address', 'postal_code', 'phone', 'is_default']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'عنوان آدرس (مثلاً خانه)'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'شهر'}),
            'province': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'استان'}),
            'full_address': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 4, 'placeholder': 'آدرس کامل'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'کد پستی'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'شماره تماس'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600'}),
        }
        labels = {
            'title': 'عنوان آدرس',
            'city': 'شهر',
            'province': 'استان',
            'full_address': 'آدرس کامل',
            'postal_code': 'کد پستی',
            'phone': 'شماره تماس',
            'is_default': 'آدرس پیش‌فرض',
        }



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name','mobile']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'w-full p-3 border rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'ایمیل'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'نام خانوادگی'}),
            'mobile': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'شماره همراه'}),
            'gender': forms.Select(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }
        labels = {
            'avatar': 'آواتار',
            'email': 'ایمیل',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'mobile': 'شماره همراه',
            'gender': 'جنسیت',
        }
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.startswith('09'):
            raise forms.ValidationError('شماره موبایل باید با 09 شروع شود')
        if len(mobile) != 11:
            raise forms.ValidationError('شماره موبایل باید 11 رقم باشد')
        return mobile



# فرم اول: گرفتن شماره موبایل برای فراموشی رمز عبور
class PasswordResetRequestForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=11,
        label='شماره موبایل',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثال: 09123456789',
            'class': 'form-control'
        }),
        help_text='شماره موبایل خود را با فرمت 09123456789 وارد کنید'
    )

    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number']
        # چک کردن اینکه شماره موبایل معتبر باشه (مثلاً 11 رقم و با 09 شروع بشه)
        if not mobile.startswith('09') or len(mobile) != 11 or not mobile.isdigit():
            raise forms.ValidationError('شماره موبایل معتبر نیست')
        return mobile


class PasswordResetRequestForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=11,
        label='شماره موبایل',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثال: 09123456789',
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        help_text='شماره موبایل خود را با فرمت 09123456789 وارد کنید'
    )

    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number']
        if not mobile.startswith('09') or len(mobile) != 11 or not mobile.isdigit():
            raise forms.ValidationError('شماره موبایل معتبر نیست')
        return mobile



class PasswordResetConfirmForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        label='کد تأیید',
        widget=forms.TextInput(attrs={
            'placeholder': 'کد 6 رقمی',
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز جدید',
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز',
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    def clean_verification_code(self):
        code = self.cleaned_data['verification_code']
        if len(code) != 6 or not code.isdigit():
            raise forms.ValidationError('کد تأیید باید 6 رقمی و عددی باشد')
        return code

    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get('new_password')
        confirm_pass = cleaned_data.get('confirm_password')

        if new_pass and confirm_pass and new_pass != confirm_pass:
            raise forms.ValidationError('رمزهای عبور با هم مطابقت ندارند')
        return cleaned_data