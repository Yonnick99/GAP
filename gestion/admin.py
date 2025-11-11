from django.contrib import admin
from .models import Persona, Carrera, Tutor, Expediente, Usuario,Tusuario,Mencion, Procesos,TProcesos
# Register your models here.

# app_name/admin.py (continuación)
@admin.register(Usuario)
class ProcesoAdmin(admin.ModelAdmin):
    pass

@admin.register(Tusuario)
class TUsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    pass

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    pass

# Y así sucesivamente con todos tus modelos...
@admin.register(Mencion)
class MencionAdmin(admin.ModelAdmin):
    pass

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    pass

# ... y los demás modelos
@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    pass

@admin.register(TProcesos)
class TProcesoAdmin(admin.ModelAdmin):
    pass

@admin.register(Procesos)
class ProcesoAdmin(admin.ModelAdmin):
    pass