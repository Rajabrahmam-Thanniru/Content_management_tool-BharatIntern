
from . import views
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name= 'login'),
    path('register/',views.register,name= 'register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/',views.about, name= 'about'),
    path('privacy/',views.privacy, name= 'privacy'),
    path('terms/',views.terms, name= 'terms'),
    path('create_post/',views.create_post,name='create_post'),
	path('post/<slug:slug>/', postdetail.as_view(), name='postdetail'),
    path('logout/', views.logout_view, name='logout_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
