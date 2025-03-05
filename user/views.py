from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from .forms import OtpForm, RegisterForm, LoginForm ,AddressForm,UserProfileForm, PasswordResetRequestForm, PasswordResetConfirmForm
from .models import Otp
import random
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Address
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone  
from datetime import timedelta
from .utiles import SendSms
User = get_user_model()

class OtpView(TemplateView):
    template_name = 'auth/otp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OtpForm()
        context['meta_tag'] = {
            'meta_title': 'تأیید شماره موبایل',
            'meta_description': 'شماره موبایل خود را برای دریافت کد تأیید وارد کنید.',
            'robots': 'noindex, nofollow',
        }
        return context

    def post(self, request, *args, **kwargs):
        form = OtpForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            # حذف OTPهای قدیمی برای این شماره
            Otp.objects.filter(mobile=mobile, is_used=False).delete()
            # ایجاد OTP جدید
            num_random = random.randint(1000, 9999)
            sender_sms = SendSms()
            sender_sms.send_otp(mobile, num_random)
            otp = Otp.objects.create(
                otp=num_random,
                mobile=mobile
            )
            # شبیه‌سازی ارسال (در عمل باید SMS بفرستی)
            messages.success(request, f"کد تأیید به شماره {mobile} ارسال شد.")
            return redirect('register')  # یا هر URL دیگه‌ای که لازم داری
        else:
            messages.error(request, "لطفاً خطاها را بررسی کنید.")
        return render(request, self.template_name, {
            'form': form,
            'meta_tag': {
                'meta_title': 'تأیید شماره موبایل',
                'meta_description': 'شماره موبایل خود را برای دریافت کد تأیید وارد کنید.',
                'robots': 'noindex, nofollow',
            }
        })





class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm()
        context['meta_tag'] = {
            'meta_title': 'ثبت‌نام در سایت',
            'meta_description': 'با وارد کردن اطلاعات خود در سایت ثبت‌نام کنید.',
            'robots': 'noindex, nofollow',  # صفحه ثبت‌نام نباید ایندکس بشه
        }
        return context

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                otp = Otp.objects.get(
                    otp=form.cleaned_data['otp'],
                    is_used=False,
                    created_at__gt=timezone.now() - timedelta(minutes=10)  # OTP فقط 10 دقیقه معتبره
                )
                otp.is_used = True
                otp.save()

                user = User.objects.create(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'] or None,
                    first_name=form.cleaned_data['first_name'] or '',
                    last_name=form.cleaned_data['last_name'] or '',
                )
                user.mobile = otp.mobile  # فرض می‌کنیم User یه فیلد mobile داره
                user.gender = form.cleaned_data['gender']
                user.invite_code = form.cleaned_data['invite_code'] or ''
                user.set_password(form.cleaned_data['password'])
                user.save()

                login(request, user)
                messages.success(request, 'ثبت‌نام با موفقیت انجام شد!')
                return redirect('home')

            except Otp.DoesNotExist:
                messages.error(request, 'کد تأیید نامعتبر است یا منقضی شده.')
        else:
            messages.error(request, 'لطفاً خطاها را بررسی کنید.')

        return render(request, self.template_name, {
            'form': form,
            'meta_tag': {
                'meta_title': 'ثبت‌نام در سایت',
                'meta_description': 'با وارد کردن اطلاعات خود در سایت ثبت‌نام کنید.',
                'robots': 'noindex, nofollow',
            }
        })

class LoginView(TemplateView):
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        context['meta_tag'] = {
            'meta_title': 'ورود به سایت',
            'meta_description': 'با نام کاربری و رمز عبور خود وارد سایت شوید.',
            'robots': 'noindex, nofollow',  # صفحه ورود نباید ایندکس بشه
        }
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید!')
                return redirect('home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        else:
            messages.error(request, 'لطفاً اطلاعات را درست وارد کنید.')

        return render(request, self.template_name, {
            'form': form,
            'meta_tag': {
                'meta_title': 'ورود به سایت',
                'meta_description': 'با نام کاربری و رمز عبور خود وارد سایت شوید.',
                'robots': 'noindex, nofollow',
            }
        })

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = UserProfileForm(instance=self.request.user)
        context['meta_tag'] = {
            'meta_title': 'پروفایل',
            'robots':'noindex, nofollow'
            }
        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل شما با موفقیت به‌روزرسانی شد!")
            return redirect(reverse('profile'))
        else:
            messages.error(request, "لطفاً اطلاعات را به درستی وارد کنید.")
            return self.render_to_response(self.get_context_data(form=form))

@method_decorator(login_required, name='dispatch')
class AddressManagementView(TemplateView):
    template_name = 'auth/address_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        context['form'] = AddressForm()
        context['meta_tag'] = {
            'meta_title': 'مدیریت ادرس ها',
            'robots':'noindex, nofollow'
            }
        return context

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "آدرس با موفقیت اضافه شد!")
            return redirect(reverse('address_management'))
        else:
            messages.error(request, "لطفاً اطلاعات را به درستی وارد کنید.")
            return self.render_to_response(self.get_context_data(form=form))

class AddressDeleteView(TemplateView):
    def post(self, request, *args, **kwargs):
        address_id = kwargs.get('address_id')
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.delete()
        messages.success(request, "آدرس با موفقیت حذف شد!")
        return redirect(reverse('address_management'))
    


class PasswordResetRequestView(TemplateView):
    template_name = 'auth/forget_password_otp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordResetRequestForm()
        context['meta_tag'] = {
            'meta_title': 'بازیابی رمز',
            'robots':'noindex, nofollow'
            }
        return context
    def post(self, request, *args, **kwargs):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile_number']
            user = User.objects.filter(mobile=mobile)
            print(user)

            if user.exists():
                print(mobile)
                Otp.objects.filter(mobile=mobile, is_used=False).delete()
                num_random = random.randint(1000, 9999)
                sender_sms = SendSms()
                sender_sms.send_otp(mobile, num_random)
                otp = Otp.objects.create(
                    otp=num_random,
                    mobile=mobile
                )
            messages.success(request, f"کد تأیید به شماره {mobile} ارسال شد.")
            return redirect('resetpassword')
        messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید.')
        return self.render_to_response(self.get_context_data(form=form))


class PasswordResetConfirmView(TemplateView):
    template_name = 'auth/reset_password_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', PasswordResetConfirmForm())
        context['meta_tag'] = {
            'meta_title': 'بازیابی رمز',
            'robots': 'noindex, nofollow'
        }
        return context

    def post(self, request, *args, **kwargs):
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            new_password = form.cleaned_data['new_password']
            otp = Otp.objects.filter(otp=entered_code, is_used=False).first()  # استفاده از .first() به جای exists()
            if not otp:
                messages.error(request, 'کد تأیید اشتباه است.')
                return self.render_to_response(self.get_context_data(form=form))
            if otp.is_expired():  # فرض: متد is_expired داری
                messages.error(request, 'کد تأیید منقضی شده است.')
                return self.render_to_response(self.get_context_data(form=form))
            otp.is_used = True
            otp.save()
            user = User.objects.get(mobile=otp.mobile)  # فرض: موبایل توی User ذخیره شده
            user.set_password(new_password)
            user.save()
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد.')
            return redirect('login')
        # اگه فرم معتبر نباشه
        messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید.')
        return self.render_to_response(self.get_context_data(form=form))