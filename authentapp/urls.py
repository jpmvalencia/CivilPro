from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.signin, name='signin'),
    path('signup/', views.signup_usu, name='signup_usu' ),
    path('signout/', views.signout, name='signout'),
    path('signupcon/',views.signup_con, name='signup_con')
]
