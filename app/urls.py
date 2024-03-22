from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('create/', create, name='create'),
    path('error/', error, name='error'),

    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout')
]
