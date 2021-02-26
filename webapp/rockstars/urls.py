"""rockstars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, re_path, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from app import views as view



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', view.home, name='home'),
    url(r'about-us/', view.about_us),
    url(r'contact-us/', view.contact_us),
    url(r'accounts/', view.accounts),
    url(r'transactions/', view.transactions),
    url(r'alerts/', view.alerts),
    url(r'service/classify/', view.classify),
    url(r'service/forecast/', view.forecast),
    url(r'service/intelligent/saving/', view.saving),
    url(r'service/transactions/', view.service_transactions),
    url(r'service/transactions/rules/', view.rules),

    re_path('login/', auth_views.LoginView.as_view(), {
        'template_name': "registration/login.html"},
        name='login'),
    re_path('logout/', auth_views.LogoutView.as_view(),
        {'next_page': '/'}, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
