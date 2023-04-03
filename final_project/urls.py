"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from AccountMaintenance.views import WelcomeView, AddAccountView, DeleteAccountView, ChangeAccountView
from AccountMaintenance.views import upload_excel, account_add_upload, account_change_upload, account_delete_upload


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WelcomeView.as_view(), name="home"),
    path('add/', AddAccountView.as_view(), name="account_add"),
    path('change/', ChangeAccountView.as_view(), name="account_change"),
    path('delete/', DeleteAccountView.as_view(), name="account_delete"),
    path('upload/', upload_excel, name="upload_excel"),
    path('upload-add/', account_add_upload, name='account_add_upload'),
    path('upload-change/', account_change_upload, name='account_change_upload'),
    path('upload-delete/', account_delete_upload, name='account_delete_upload')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
