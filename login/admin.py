from django.contrib import admin

# Register your models here.
from .models import Problem
admin.site.register(Problem)

from .models import TestCases
admin.site.register(TestCases)
