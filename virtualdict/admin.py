from django.contrib import admin
from .models import Concepts

# Register your models here.
class ConceptsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Concepts, ConceptsAdmin)

