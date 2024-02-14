from django.contrib import admin
from .models import User, File_Upload
from .models import Category

# Register your models here.
admin.site.register(User)
admin.site.register(File_Upload)
admin.site.register(Category)