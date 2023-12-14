from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from .models import Concepts, Reviews, Comentarios, ComentariosPerfil, Perfil
from .forms import ConceptsForm, ReviewsForm

# Create your views here.


def home(request):
    if User.is_authenticated:
        username = request.user

    return render(request, "home.html", {
        'username': username,
    })


def allconcepts(request):
    
    if request.method == "GET":
        concept = Concepts.objects.filter().order_by('-pk')[:1000]
        return render(request, "defconcepts.html", {
            'concept': concept,
            'global': True,
        })

    else:
        consulta = request.POST['search'] 
        if (consulta != "") and (consulta.isspace() == False):
         concept = Concepts.objects.filter(title__icontains=request.POST['search'])#.order_by('-pk')
        else:
         concept = Concepts.objects.filter().order_by('-pk')[:1000]
        return render(request, "defconcepts.html", {
            'concept': concept,
            'global': True,
        })


@login_required
def concept(request, concept_id):

    concept = get_object_or_404(Concepts, pk=concept_id)
    pos_reviews = Reviews.objects.filter(concept=concept, review=True)
    comentarios = Comentarios.objects.filter(concept=concept)
    neg_reviews = Reviews.objects.filter(concept=concept, review=False)
    user_review = None

    user_review = Reviews.objects.filter(
        concept=concept, user=request.user).first()

    comentarios_avanzados = []

    for comentario in comentarios:
        try:
            perfil = Perfil.objects.get(user=comentario.user)
        except Perfil.DoesNotExist:
            perfil = None

        # Agrega los resultados a la lista final
        comentarios_avanzados.append([perfil,comentario])
    
    print(comentarios_avanzados)
    return render(request, "concept.html", {
        'concept': concept,
        'positive': len(pos_reviews),
        'negative': len(neg_reviews),
        'user_review': user_review,
        'actual_user': request.user.username,
        #'comentarios': comentarios,
        'comentarios': comentarios_avanzados
    })

@login_required
def concept_comment(request,concept_id): 

    if request.method == "GET":
        return redirect("concept_view", concept_id=concept_id)
    else:
        concept = get_object_or_404(Concepts, pk=concept_id)
        comentado = request.POST['comentario'] 
        if (comentado != "") and (comentado.isspace() == False):
         comentario = Comentarios(texto=comentado,user=request.user, concept=concept)
         comentario.save()

        return redirect("concept_view", concept_id=concept_id)

@login_required
def concept_reaction(request, concept_id):

    if request.method == "GET":
        return redirect("concept_view", concept_id=concept_id)
    else:
        concept = get_object_or_404(Concepts, pk=concept_id)
        user_review = Reviews.objects.filter(
            concept=concept, user=request.user).first()
        reaccion = None

        if request.POST['reaction'] == "like":
            reaccion = True
        else:
            reaccion = False

        if user_review is None:
            # Crear una instancia de MiModelo
            nueva_review = Reviews(
                review=reaccion, user=request.user, concept=concept)

            nueva_review.save()
        else:
            if user_review.review == reaccion:
                user_review.delete()
            else:
                user_review.review = reaccion
                user_review.save()

        return redirect("concept_view", concept_id=concept_id)


@login_required
def defconcepts(request):
 
    if request.method == "GET":
        concept = Concepts.objects.filter(user=request.user).order_by('-pk')[:1000]
        return render(request, "defconcepts.html", {
            'concept': concept,
            'autor': True,
        })

    else:
        consulta = request.POST['search'] 
        if (consulta != "") and (consulta.isspace() == False):
         concept = Concepts.objects.filter(title__icontains=request.POST['search'],user=request.user)
        else:
         concept = Concepts.objects.filter(user=request.user).order_by('-pk')[:1000]
        return render(request, "defconcepts.html", {
            'concept': concept,
            'autor': True,
        })


@login_required
def userconcepts(request,username):
    user = get_object_or_404(User,username=username)
    autorizado = False
    if request.user.username == username:
      autorizado = True
    if request.method == "GET":
        concept = Concepts.objects.filter(user=user).order_by('-pk')
        return render(request, "defconcepts.html", {
            'concept': concept,
            'autor': autorizado,
        })

    else:
        consulta = request.POST['search'] 
        if (consulta != "") and (consulta.isspace() == False):
         concept = Concepts.objects.filter(title__icontains=request.POST['search'],user=user)
        else:
         concept = Concepts.objects.filter(user=user).order_by('-pk')[:1000]
        return render(request, "defconcepts.html", {
            'concept': concept,
            'autor': autorizado,
        })        


@login_required
def concept_detail(request, concept_id):
    if request.method == "GET":
        concept = get_object_or_404(Concepts, pk=concept_id, user=request.user)
        form = ConceptsForm(instance=concept)
        try:
            concept_img = concept.exampleImg.url
            return render(request, "concept_detail.html", {
                'concept_id': concept_id,
                'form': form,
                'concept_img': concept_img
            })
        except:
            return render(request, "concept_detail.html", {
                'concept_id': concept_id,
                'form': form,
            })
    else:
        try:
            concept = get_object_or_404(
                Concepts, pk=concept_id, user=request.user)
            form = ConceptsForm(request.POST, request.FILES, instance=concept)
            form.save()
            return redirect("defconcepts")

        except:
            return render(request, "concept_detail.html", {
                'concept_id': concept_id,
                'form': form,
                'message': "No sé qué pasó, pero no tenía que pasar D:"
            })


@login_required
def concept_delete(request, concept_id):
    if request.method == "GET":
        concept = get_object_or_404(Concepts, pk=concept_id, user=request.user)
        print(concept.title)
        return render(request, "concept_delete.html", {
            'concept_id': concept_id,
            'concept': concept
        })
    else:
        concept = get_object_or_404(Concepts, pk=concept_id, user=request.user)
        concept.delete()
        return redirect("defconcepts")


@login_required
def newconcept(request):
    if request.method == "GET":
        concept = Concepts.objects.filter(user=request.user)
        return render(request, "newconcept.html", {
            'form': ConceptsForm,
            'concept': concept
        })
    else:
        try:
            form = ConceptsForm(request.POST, request.FILES)
            nconcept = form.save(commit=False)
            nconcept.user = request.user
            nconcept.save()
            return render(request, "newconcept.html", {
                'message': "Guardado con éxito",
                'form': ConceptsForm
            })
        except:
            return render(request, "newconcept.html", {
                'message': "¡Uy! No se pudo guardar el concepto :(",
                'form': ConceptsForm
            })


def lin(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        try:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, "login.html", {
                    'error': "Usuario o contraseña incorrectos, intenta otra vez"
                })
            else:
                login(request, user)
                return redirect("home")

        except:
            return render(request, "login.html", {
                'error': 'Usuario o contraseña incorrectos, intenta de nuevo'
            })


def reg(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        if " " in request.POST['username']:
            return render(request, "register.html", {
                'error': 'No se permiten espacios en el nombre de usuario'
            })
        elif len(request.POST['password']) < 6:
            return render(request, "register.html", {
                'error': 'Tu contraseña debe contener al menos 6 caracteres'
            })

        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
                user.save()
                login(request, user)
                return render(request, "home.html", {
                    'username': user.username,
                })

            except Exception as e:
                print(e)
                return render(request, "register.html", {
                    'error': 'Algo salio mal :('
                })

        else:
            return render(request, "register.html", {
                'error': 'No coinciden las contraseñas'
            })


@login_required
def profile(request, username):
    user = get_object_or_404(User ,username=username)
    try:
        perfil = Perfil.objects.get(user=user)
    except Perfil.DoesNotExist:
        perfil = None
    return render(request, "profile.html", {
        'user': user,
        'perfil': perfil
    })



@login_required
def lout(request):
    if request.method == 'GET':

        return render(request, "logout.html", {

        })
    else:
        logout(request)
        return redirect("home")
