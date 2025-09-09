from django.urls import path
from .views import SignupView, LoginView

app_name = 'auth_app'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
