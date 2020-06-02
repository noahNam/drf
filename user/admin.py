from django.contrib import admin

from .models import *

# admin page에서 보고 싶은면 이곳에 등록
# Register your models here.

admin.site.register(User)
