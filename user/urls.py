from django.urls import path
from .views import OtpView, RegisterView, LogoutView, LoginView, ProfileView, AddressManagementView, AddressDeleteView, PasswordResetRequestView,PasswordResetConfirmView


urlpatterns = [
    path('otp/', OtpView.as_view(), name='otp'),
    path('resetpasswordrequest/', PasswordResetRequestView.as_view(), name='resetpasswordrequest'),
    path('resetpassword/', PasswordResetConfirmView.as_view(), name='resetpassword'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('addresses/', AddressManagementView.as_view(), name='address_management'),
    path('addresses/delete/<int:address_id>/', AddressDeleteView.as_view(), name='address_delete'),
]
