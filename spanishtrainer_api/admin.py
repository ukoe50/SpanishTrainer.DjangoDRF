from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import Wordtype
from .models import Category
from .models import Word
from .models import Sentence
from .models import Lang
from .models import LookupGroup
from .models import Tense
# from .models import Conjugation

# Register your models here.

# this class is for the admin functionality for the admin webinterface
class MyUserAdmin(UserAdmin):
   pass

# Default variant
# with no customized field selection
admin.site.register(User, MyUserAdmin)
admin.site.register(Lang)
admin.site.register(Wordtype)
admin.site.register(Category)
admin.site.register(Word)
admin.site.register(Sentence)
admin.site.register(LookupGroup)
admin.site.register(Tense)
# admin.site.register(Conjugation)

# Customized variant
# We can control the fields to display by specifying them in a list_display property in the admin.py file.
# First create a WordEsDeAdmin() class and specify the list_display tuple, like this
#class WordAdmin(admin.ModelAdmin):
#    list_display = ("de", "es", "level", "createuser", "createdate")

# To include the Member model in the admin interface, we have to tell Django that this model should
# be visible in the admin interface
#admin.site.register(Word, WordAdmin)