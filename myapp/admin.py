from django.contrib import admin

from .models import UserCreation, CreateVocabulary

class VocabularyInLineAdmin(admin.TabularInline):
    #model = UserCreation
    pass

class UserAdmin(admin.ModelAdmin):
    #inlines = [VocabularyInLineAdmin]
    pass

admin.site.register(UserCreation)
admin.site.register(CreateVocabulary)
