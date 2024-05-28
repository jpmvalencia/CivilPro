from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login ),
    path('signup/', views.signup ),
    path('signout/', views.signout, name='signout'),
    path('signupcon/',views.signupcon)
]
