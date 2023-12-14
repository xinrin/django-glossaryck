from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('concepts/',views.allconcepts,name="concepts"),
    path('concept/<int:concept_id>',views.concept,name="concept_view"),
    path('concept/comment/<int:concept_id>',views.concept_comment,name="concept_comment"),
    path('concept/reaction/<int:concept_id>',views.concept_reaction,name="concept_reaction"),
    path('defconcepts/',views.defconcepts,name="defconcepts"),
    path('concepts/user/<str:username>',views.userconcepts,name="userconcepts"),
    path('defconcepts/<int:concept_id>',views.concept_detail,name="concept_detail"),
    path('defconcepts/<int:concept_id>/delete',views.concept_delete,name="concept_delete"),
    path('newconcept/',views.newconcept,name="newconcept"),
    path('login/',views.lin,name="login"),
    path('register/',views.reg,name="register"),
    path('logout/',views.lout,name="logout"),
    path('profile/<str:username>',views.profile,name="profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
