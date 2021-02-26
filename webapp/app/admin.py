from django.contrib import admin

from .models import UserProfile


from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

AdminSite.site_title = ugettext_lazy('Admin')
AdminSite.site_header = ugettext_lazy('Administration')
AdminSite.index_title = ugettext_lazy('Shaking Shamrocks')



admin.site.register(UserProfile)
