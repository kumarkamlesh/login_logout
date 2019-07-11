from django.urls import path, re_path
from login_user_model.views import user_login, user_logout, success, index, registration
from login_user_model import views

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('success/', success, name='success'),
    path('logout/', user_logout, name='logout'),
    path('registrationt/', registration, name='registration'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),

]
