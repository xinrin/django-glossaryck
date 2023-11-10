from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User
from .models import Concepts
from .forms import ConceptsForm

# Create your views here.


def home(request):
    if User.is_authenticated:
        username=request.user
        
    return render(request,"home.html",{
        'username':username,
    })


@login_required
def defconcepts(request):
    concept = Concepts.objects.filter(user=request.user)
    
    #print(concept)
    return render(request,"defconcepts.html",{
        'concept':concept,
    })

@login_required
def concept_detail(request,concept_id):
    if request.method == "GET":
        concept = get_object_or_404(Concepts,pk=concept_id, user=request.user)
        form=ConceptsForm(instance=concept)
        try:
            concept_img = concept.exampleImg.url
            return render(request,"concept_detail.html",{
                'concept_id':concept_id,
                'form':form,
                'concept_img':concept_img
            })
        except:
            return render(request,"concept_detail.html",{
                'concept_id':concept_id,
                'form':form,
            })
    else:
        try:
            concept = get_object_or_404(Concepts,pk=concept_id,user=request.user)
            form = ConceptsForm(request.POST, request.FILES, instance=concept)
            form.save()
            return redirect("defconcepts")

        except:
            return render(request,"concept_detail.html",{
            'concept_id':concept_id,
            'form':form,
            'message':"No sé qué pasó, pero no tenía que pasar D:"
        })

@login_required
def concept_delete(request,concept_id):
    if request.method == "GET":
        concept = get_object_or_404(Concepts,pk=concept_id, user=request.user)
        print(concept.title)
        return render(request,"concept_delete.html",{
            'concept_id':concept_id,
            'concept':concept
        })
    else:
        concept = get_object_or_404(Concepts,pk=concept_id,user=request.user)
        concept.delete()
        return redirect("defconcepts")


@login_required
def newconcept(request):
    if request.method == "GET":
        concept = Concepts.objects.filter(user=request.user)
        return render(request,"newconcept.html",{
            'form':ConceptsForm,
            'concept':concept
        })
    else:
        try:
            form = ConceptsForm(request.POST, request.FILES)
            nconcept = form.save(commit=False)
            nconcept.user = request.user
            nconcept.save()
            return render(request,"newconcept.html",{
                'message':"Guardado con éxito",
                'form':ConceptsForm
            })
        except:
            return render(request,"newconcept.html",{
                'message':"¡Uy! No se pudo guardar el concepto :(",
                'form':ConceptsForm
            })



def lin(request):
    if request.method == "GET":
        return render(request,"login.html")
    else:
        try:
            user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request,"login.html",{
                    'error':"Usuario o contraseña incorrectos, intenta otra vez"
                })
            else:
                login(request,user)
                return redirect("home")
            
        except:
            return render(request,"login.html",{
                'error':'Usuario o contraseña incorrectos, intenta de nuevo'
            })


def reg(request):
    if request.method == "GET":
        return render(request,"register.html")
    else:
        if " " in request.POST['username']:
            return render(request,"register.html",{
                'error':'No se permiten espacios en el nombre de usuario'
            })
        elif len(request.POST['password']) < 6:
            return render(request,"register.html",{
                'error':'Tu contraseña debe contener al menos 6 caracteres'
            })
        
        if request.POST['password'] == request.POST['password2']:
            #print(request.POST)
            #try:
                user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'])
                user.save()
                login(request,user)
                return render(request,"home.html",{
                    'username': user.username,
                })
            
            #except Exception as e:
                print(e)
                return render(request,"register.html",{
                'error':'Algo salio mal :('
            })
            
        else:
            return render(request,"register.html",{
                'error':'No coinciden las contraseñas'
            })
                
@login_required
def profile(request,username):
    return render(request,"profile.html",{
        'username':username,
    })


@login_required
def lout(request):
    if request.method == 'GET':
        
        
        return render(request,"logout.html",{
            
        })
    else:
        logout(request)
        return redirect("home")
    
