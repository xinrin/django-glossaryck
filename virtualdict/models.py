from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Concepts(models.Model):
    title = models.CharField(max_length=200)
    definition = models.TextField(default="")
    exampleText = models.TextField(null=True, blank=True)
    exampleImg = models.ImageField(upload_to='posts_img/',null=True, blank=True)
    source = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title + " - " + self.user.username

class Reviews(models.Model):
    # V: Bien / F: Mal 
    review = models.BooleanField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concepts, on_delete=models.CASCADE)

    def __str__(self):
        return self.concept.title + " by " + self.concept.user.username + " - Review de " + self.user.username


class Comentarios(models.Model):

    texto = models.TextField(null=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concepts, on_delete=models.CASCADE)

    def __str__(self):
        return self.concept.title + " by " + self.concept.user.username + " - comentado por " + self.user.username

class ComentariosPerfil(models.Model):

    texto = models.TextField(null=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    user_perfil = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_perfil')
    comentador = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comentador')

    def __str__(self):
        return self.user_perfil.username + " - comentado por " + self.comentador.username
    
class Perfil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    foto = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return "perfil de " + self.user.username 
    