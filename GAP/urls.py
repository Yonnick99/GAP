"""
URL configuration for GAP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gestion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('index/', views.index, name='login'),
    path('signout/', views.signout, name='signout'),
    path(''
    '/', views.registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('participante/', views.participante, name='participante'),
    path('tutor/', views.tutor, name='tutor'),
    path('seguridad/', views.seguridad, name='seguridad'),
    path('actualizar/', views.actualizar, name='actualizar'),
    path('ajax/cargar-menciones/', views.cargar_menciones, name='ajax_cargar_menciones'),
    path('ajax/cargar-tutores/', views.cargar_tutores, name='ajax_cargar_tutores'),
    path('ajax/eliminar_tutor/', views.eliminar_tutor, name='ajax_eliminar_tutor'),
    path('seguridad_admin/', views.seguridad_admin, name='seguridad_admin'),
    path('modificar/<int:persona_id>/', views.modificar_usuario, name='modificar_usuario'),
    path('procesos/<int:expediente_id>/', views.procesos, name='procesos'),
    path('gestion/', views.proceso_gestion, name='proceso_gestion'),
    path('gestion_user/<int:expediente_id>/', views.gestion_usuario, name='gestion_usuario'),
    path('actualizar_documentos/', views.actualizar_documentos, name='actualizar_documentos'),
    path('eliminar_documento/<int:valor>/<str:doc_type>', views.eliminar_documento, name='eliminar_documento'),
    path('consulta/', views.consulta, name='consulta'),
    path('reporte/', views.reporte, name='reporte'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)