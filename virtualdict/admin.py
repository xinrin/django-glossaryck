from django.contrib import admin
from .models import Concepts, Reviews, Comentarios, ComentariosPerfil, Perfil

# Register your models here.
class ConceptsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ReviewsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ComentariosAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ComentariosPerfilAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)    

class PerfilAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)    

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(ComentariosPerfil, ComentariosPerfilAdmin)
admin.site.register(Comentarios, ComentariosAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Concepts, ConceptsAdmin)

