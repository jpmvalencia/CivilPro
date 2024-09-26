from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.signin ),
    path('signup/', views.signup_usu ),
    path('signout/', views.signout, name='signout'),
    path('signupcon/',views.signup_con)
]
