from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Persona, Carrera, Tutor, Expediente, Usuario,Tusuario,Mencion, Procesos,TProcesos,User
from django.utils import timezone
import csv
import datetime

# Create your views here.

def index(request):
    
    if request.method == 'GET':
        return render(request, 'index.html')
    
    elif request.method == 'POST':   
        
        try:
            try:
                usuario = Usuario.objects.get(usuario=request.POST.get('usuario'), clave=request.POST.get('clave'))
                tipo = Persona.objects.filter(id_usuario=usuario.id_usuario).values_list('tipo_usuario', flat=True).first()

                user = authenticate(request, username=usuario.usuario, password=usuario.clave)
                login(request, user)  # Iniciar sesión del usuario

            except IntegrityError as e:
                return render(request, 'index.html', {'error': f"Error al autenticar el usuario: {e}"})
            except Usuario.DoesNotExist:    
                return render(request, 'index.html', {'error': "Usuario no encontrado, validar credenciales."})
                #
            if usuario:
                if tipo == 1:
                    return render(request, 'dashboard.html') 
                elif tipo == 2:
                    return HttpResponse("Página de Tutor - En construcción")                 
                elif tipo == 3:
                    return HttpResponse("Página de Consultor - En construcción")     
                elif tipo == 4:
                    return redirect('participante')  # Redirigir a la vista participante con el ID del usuario        
                else:
                    return HttpResponse("Tipo de usuario no reconocido", status=400)
            else:
                print("Credenciales inválidas")
                return HttpResponse("Credenciales inválidas", status=401)
            
        except Exception as e:
            print(f"Error durante el inicio de sesión: {e}")       
    else:
        return HttpResponse("Metodo no permitido", status=405)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Registro de usuarios
@login_required
def registro(request):

    if request.method == 'GET':
        Tusuarios = Tusuario.objects.all()
        return render(request, 'registro.html', {'tusuarios': Tusuarios,} )

    elif request.method == 'POST':
        # crear el usuario
        Tusuarios = Tusuario.objects.all()
        try:
            crearuser = User.objects.create_user(
                first_name = request.POST.get('nombre'),
                last_name = request.POST.get('apellido'),
                email = request.POST.get('correo'),
                username = 'V' + request.POST.get('cedula'),
                password = request.POST.get('cedula'),
            )
            crearuser.save()

            creacion_usuario = Usuario(
                usuario= 'V' + request.POST.get('cedula'),
                clave= request.POST.get('cedula'),                
            )
            creacion_usuario.save()
        
        except IntegrityError as e:
            return HttpResponse(f"Error al crear el usuario: {e}")
            
        try:
            usuario = Usuario.objects.get(usuario= 'V' + request.POST.get('cedula'))
            print(f"ID de usuario creado: {usuario.id_usuario}")
                # crear la persona       

            creacion_persona = Persona(
                id_usuario= Usuario.objects.get(id_usuario=usuario.id_usuario),
                cedule= request.POST.get('cedula'),
                nombre= request.POST.get('nombre'),
                apellido= request.POST.get('apellido'),
                fecha_nacimiento= request.POST.get('fNacimiento'),
                correo= request.POST.get('correo'),
                tlf_princimal= request.POST.get('tprincipal'),
                tlf_secundario= request.POST.get('tsecundario'),
                tipo_usuario=Tusuario.objects.get(id_tipo=request.POST.get('tusuario')) ,
                estado= request.POST.get('estado'),
                ciudad= request.POST.get('capital'),
                cpostal= request.POST.get('cpostal'),
                nucleo= request.POST.get('nucleo'),
            )
            print(f"Persona a crear: {creacion_persona}")
            creacion_persona.save()

            return redirect('registro')

        except IntegrityError as e:
            return HttpResponse(f"Error al crear la persona: {e}")
        except Tusuario.DoesNotExist:
           return  HttpResponse(f"Tipo de usuario no encontrado")

    else:
        return HttpResponse("Metodo no permitido", status=405)

#Mantenimiento de usuarios
@login_required
def seguridad_admin(request):
    id = Usuario.objects.filter(usuario=request.user.username).values_list('id_usuario', flat=True).first()    
    rol = Persona.objects.filter(id_usuario=id).values_list('tipo_usuario', flat=True).first()  # Obtener los datos del usuario logueado       
    carrera = Carrera.objects.all()

    if request.method == 'GET':
        return render(request,'seguridad _admin.html', {'roles': rol, 'carreras':carrera} )
    else:
        parametros = request.POST
        resultado = Persona.objects.filter( Q(cedule__startswith =parametros.get('search_cedula')) & Q(nombre__icontains =parametros.get('search_nombre')) )
        return render(request,'seguridad _admin.html', {'roles': rol, 'carreras':carrera, 'resultados':resultado} )

@login_required
def modificar_usuario(request,persona_id):
    usuario = Usuario.objects.get(usuario=request.user.username)
    tipo = Persona.objects.filter(id_usuario=usuario.id_usuario).values_list('tipo_usuario', flat=True).first()


    try:
        data = get_object_or_404(Persona, id_persona=persona_id)
    except Persona.DoesNotExist:
        return redirect('seguridad_admin')
    
    return render(request, 'seguridad.html', {'datos': data, 'tipos': tipo})

@login_required
def actualizar(request):
    recepcion = request.user
    print(f"Datos recibidos para actualizar: {recepcion}")

    usuario = Usuario.objects.get(usuario=request.user.username)
    tipo = Persona.objects.filter(id_usuario=usuario.id_usuario).values_list('tipo_usuario', flat=True).first()

    
    if request.method == 'POST':
            
        try: 
            creacion_persona = Persona(
                id_persona= Persona.objects.get(id_usuario=Usuario.objects.get(usuario=request.user.username)).id_persona,
                id_usuario= Usuario.objects.get(usuario=request.user.username),
                cedule= Persona.objects.get(id_usuario=Usuario.objects.get(usuario=request.user.username)).cedule,
                nombre= request.POST.get('nombre'),
                apellido= request.POST.get('apellido'),
                fecha_nacimiento= request.POST.get('fNacimiento'),
                tipo_usuario= Persona.objects.get(id_usuario=Usuario.objects.get(usuario=request.user.username)).tipo_usuario,
                correo= request.POST.get('correo'),
                tlf_princimal= request.POST.get('tprincipal'),
                tlf_secundario= request.POST.get('tsecundario'),
                estado= request.POST.get('estado'),
                ciudad= request.POST.get('capital'),
                cpostal= request.POST.get('cpostal'),
                nucleo= request.POST.get('nucleo'),
                fecha_creacion= Persona.objects.get(id_usuario=Usuario.objects.get(usuario=request.user.username)).fecha_creacion,
            )
            
            creacion_persona.save()

            modificarUser = User.objects.get(username = request.user.username)
            
            modificarUser.first_name = Persona.objects.get(id_usuario=Usuario.objects.get(usuario=request.user.username)).nombre
            modificarUser.last_name = Persona.objects.get(id_usuario=Usuario.objects.get(usuario=request.user.username)).apellido
            modificarUser.email = Persona.objects.get(id_usuario=Usuario.objects.get(usuario=request.user.username)).correo
        
            modificarUser.save()

            if tipo == 1:
                return redirect('seguridad_admin') 
            elif tipo == 3:
                return redirect('seguridad_admin')      
            elif tipo == 2:
                return HttpResponse("Página de Tutor - En construcción")
            elif tipo == 4:
                return redirect('participante')
            else:                
                return HttpResponse("Tipo de usuario no reconocido", status=400)

        except IntegrityError as e:
            return HttpResponse(f"Error al crear la persona: {e}")
        except Tusuario.DoesNotExist:
           return  HttpResponse(f"Tipo de usuario no encontrado")

    else:
        return HttpResponse("Metodo no permitido", status=405)

# Tutores 
@login_required
def tutor(request):
    carrera = Carrera.objects.all()
    tutores = Tutor.objects.all().values('id_persona')
    profesor = Persona.objects.filter(tipo_usuario=2).exclude(id_persona__in=tutores)
    existente = Tutor.objects.all()

    if request.method == 'GET':
        return render(request, 'tutor.html',{'carreras': carrera, 'profesores':profesor, 'existentes':existente})
    else:

        tutor = Tutor (
            id_persona = Persona.objects.get(id_persona = request.POST.get('facilitador')),
            id_carrera = Mencion.objects.get(id_mencion = request.POST.get('mencion'))
        )

        tutor.save()
        
        existente = Tutor.objects.all()
        
        return redirect('tutor')

@login_required
def eliminar_tutor(request):

    tutot_Id = request.GET.get('tutot_Id')        
    aperturado = Expediente.objects.filter(id_tutor = tutot_Id, estado = 'En Proceso').exists()
    #existente = Tutor.objects.exists()

    if aperturado == True:
        mensaje = 'El Tutor seleccionado posee expedientes abiertos, debe comunicarse con el Administrador del Sistema o Cerrar los expedientes con el estadus: EN PROCESO'
        return JsonResponse({'success': False, 'message': mensaje}, status=200) # 409 Conflict
    else:
        Tutor.objects.filter(id_tutor = tutot_Id).delete()
        return JsonResponse({'success': True, 'message': 'Tutor eliminado exitosamente.'}, status=200)

# Gestión de procesos (Todo lo relacionado con expedientes)
@login_required
def proceso_gestion(request):
    id = Usuario.objects.filter(usuario=request.user.username).values_list('id_usuario', flat=True).first()    
    rol = Persona.objects.filter(id_usuario=id).values_list('tipo_usuario', flat=True).first()  # Obtener los datos del usuario logueado       
    expediente = Expediente.objects.all()
    carrera = Carrera.objects.all()

    if request.method == 'GET':
        return render(request, 'proceso_gestion.html', {'expedientes': expediente, 'carreras':carrera, 'roles': rol} )
    else:
        parametros = request.POST
        print (f"Parametros recibidos: {parametros}")
        resultado = Expediente.objects.all()
        return render(request, 'proceso_gestion.html', {'expedientes': expediente, 'carreras':carrera, 'roles': rol ,'resultados':resultado})

@login_required
def gestion_usuario(request,expediente_id):
    if request.method == 'GET':
        try:
            datos_expediente = get_object_or_404(Expediente, id_expediente=expediente_id)
            print(f"Datos del expediente: {datos_expediente}")
            datos = Persona.objects.get(id_persona=datos_expediente.id_persona.id_persona)
            proceso_activo= Procesos.objects.filter(id_expediente=expediente_id).order_by()
            proceso_pendiente = proceso_activo.filter(estado='Pendiente').exists()    
            carrera = Carrera.objects.all()
            tutor = Tutor.objects.all()
            mencion = Mencion.objects.all()
        except Expediente.DoesNotExist:
            return redirect('proceso_gestion')    
        return render(request, 'gestion_usuario.html', {'carreras': carrera, 'tutores': tutor, 'menciones': mencion, 'datos': datos, 'procesos_activos': proceso_activo, 'datos_expedientes': datos_expediente, 'procesos_pendientes': proceso_pendiente})
    
    elif request.method == 'POST':
        datos = request.POST
        print (f"Datos recibidos para actualizar el expediente: {datos}")

        datos_expediente = get_object_or_404(Expediente, id_expediente=expediente_id)
        datos_expediente.id_tutor = Tutor.objects.get(id_tutor=request.POST.get('tutor')) 
        datos_expediente.id_mencion = Mencion.objects.get(id_mencion=request.POST.get('mencion'))
        datos_expediente.periodo_inicio = datos_expediente.periodo_inicio
        datos_expediente.periodo_fin = datos_expediente.periodo_fin
        datos_expediente.acreditacion = request.POST.get('acredit')
        datos_expediente.estado = request.POST.get('estado') or datos_expediente.estado
        
        if request.POST.get('estado') == 'Aprobado' or request.POST.get('estado') == 'Rechazado':
            datos_expediente.periodo_cierre = timezone.now()

        datos_expediente.doc_identidad = request.FILES.get('fcedula') or datos_expediente.doc_identidad
        datos_expediente.foto_perfil = request.FILES.get('ftipocarnet') or datos_expediente.foto_perfil
        datos_expediente.const_notas = request.FILES.get('fconstnotas') or datos_expediente.const_notas
        datos_expediente.const_inscripcion = request.FILES.get('fincrpcion') or datos_expediente.const_inscripcion    
        datos_expediente.asistencia = request.FILES.get('fasistaller') or datos_expediente.asistencia   
        datos_expediente.forma_1 = request.FILES.get('fforma1') or datos_expediente.forma_1

        datos_expediente.save()

        return redirect ('proceso_gestion')
        
@login_required
def eliminar_documento(request, valor, doc_type):
    print(f"Valor recibido: {valor}, Tipo de documento: {doc_type}")

    if doc_type in ['doc_identidad', 'foto_perfil', 'const_notas', 'const_inscripcion', 'asistencia', 'forma_1']:
        try:
            expediente = get_object_or_404(Expediente, id_expediente=valor)

            if doc_type == 'doc_identidad':
                expediente.doc_identidad.delete(save=False)
                expediente.doc_identidad = None
            elif doc_type == 'foto_perfil':
                expediente.foto_perfil.delete(save=False)
                expediente.foto_perfil = None
            elif doc_type == 'const_notas':
                expediente.const_notas.delete(save=False)
                expediente.const_notas = None
            elif doc_type == 'const_inscripcion':
                expediente.const_inscripcion.delete(save=False)
                expediente.const_inscripcion = None
            elif doc_type == 'asistencia':
                expediente.asistencia.delete(save=False)
                expediente.asistencia = None
            elif doc_type == 'forma_1':
                expediente.forma_1.delete(save=False)
                expediente.forma_1 = None
            else:
                return HttpResponse("Tipo de documento no válido", status=400)

            expediente.save()
            return redirect('gestion_usuario', expediente_id=valor)

        except Expediente.DoesNotExist:
            return HttpResponse("Expediente no encontrado", status=404)
    elif doc_type == 'anexo':
        try:
            proceso = get_object_or_404(Procesos, id_proceso=valor)
            proceso.anexo.delete(save=False)
            proceso.anexo = None
            proceso.estado = 'Pendiente'
            proceso.save()
            return redirect('gestion_usuario', expediente_id=proceso.id_expediente.id_expediente)
        except Procesos.DoesNotExist:
            return HttpResponse("Proceso no encontrado", status=404)
    else:
        return HttpResponse ("Tipo de documento no válido", status=400)

# Nota: comparte relacion con la vista de participante
@login_required
def actualizar_documentos(request):

    user = Usuario.objects.get(usuario=request.user.username)   
    perosona = Persona.objects.get(id_usuario=user.id_usuario)
    datos = Expediente.objects.get(id_persona=perosona.id_persona, estado="En Proceso")

    if request.method == 'POST':
        datos.doc_identidad = request.FILES.get('fcedula') or datos.doc_identidad
        datos.foto_perfil = request.FILES.get('ftipocarnet') or datos.foto_perfil
        datos.const_notas = request.FILES.get('fconstnotas') or datos.const_notas
        datos.const_inscripcion = request.FILES.get('fincrpcion') or datos.const_inscripcion
        datos.asistencia = request.FILES.get('fasistaller') or datos.asistencia
        datos.forma_1 = request.FILES.get('fforma1') or datos.forma_1
        datos.save()
        return redirect ('participante')
    else:
        return HttpResponse("Metodo no permitido", status=405)
        
# Nota: comparte relacion con la vista de participante
@login_required
def procesos(request, expediente_id):

    datos = Persona.objects.get(id_usuario=(Usuario.objects.get(usuario=request.user.username))  ) 
    datos_expediente = Expediente.objects.get(id_expediente=expediente_id)
    proceso_activo = Procesos.objects.filter(id_expediente=datos_expediente.id_expediente).order_by()
    print (f"Datos del expediente existente: {proceso_activo}")
    for i in range(proceso_activo.count()):
        if request.FILES.get(f'{proceso_activo[i].id_proceso}'):

            proceso = Procesos.objects.get(id_proceso=proceso_activo[i].id_proceso)
            proceso.anexo = request.FILES.get(f'{proceso.id_proceso}')
            proceso.estado = 'En Revisión'
            proceso.save()

    if datos.tipo_usuario.id_tipo == 1 or datos.tipo_usuario.id_tipo == 3:
        return redirect ('proceso_gestion')
    else:    
        return redirect ('participante')


# Maneja la logica para crear el expediente desde el modulo de participante
@login_required
def participante(request):

    carrera = Carrera.objects.all()
    tutor = Tutor.objects.all()
    mencion = Mencion.objects.all()
    datos = Persona.objects.get(id_usuario=(Usuario.objects.get(usuario=request.user.username))  ) 
    expediente_existente = Expediente.objects.filter(id_persona=datos.id_persona, estado = "En Proceso").exists()

    if request.method == 'GET':# Obtener los datos del usuario logueado
        if expediente_existente:
            datos_expediente = Expediente.objects.get(id_persona=datos.id_persona, estado = "En Proceso")
            proceso_activo = Procesos.objects.filter(id_expediente=datos_expediente.id_expediente).order_by()
            print (f"Datos del expediente existente: {proceso_activo}")
            return render(request, 'participante.html', {'carreras': carrera, 'tutores': tutor, 'menciones': mencion, 'datos': datos, 'expediente': expediente_existente, 'datos_expedientes': datos_expediente , 'procesos_activos': proceso_activo })
        else:
            datos_expediente = None
            return render(request, 'participante.html', {'carreras': carrera, 'tutores': tutor, 'menciones': mencion, 'datos': datos, 'expediente': expediente_existente, 'datos_expedientes': datos_expediente  })

    elif request.method == 'POST':

        guardar = Expediente(

            id_persona = Persona.objects.get(id_persona=datos.id_persona),
            id_tutor = Tutor.objects.get(id_tutor=request.POST.get('tutor')), 
            id_mencion = Mencion.objects.get(id_mencion=request.POST.get('mencion')),
            periodo_inicio = request.POST.get('pInicio'),
            periodo_fin = request.POST.get('pFin'),
            periodo_cierre = request.POST.get('pFin'),
            acreditacion = request.POST.get('acredit'),
            doc_identidad = request.FILES.get('fcedula'),
            foto_perfil = request.FILES.get('ftipocarnet'),
            const_notas = request.FILES.get('fconstnotas'),
            const_inscripcion = request.FILES.get('fincrpcion'),
            asistencia = request.FILES.get('fasistaller'),
            forma_1 = request.FILES.get('fforma1'),
        )
        guardar.save()



        if request.POST.get('acredit') == 'False':

            procesos1 = [1,2,3,4,5,6,7]
            for proceso in procesos1:

                nuevo_proceso = Procesos(
                    id_expediente = Expediente.objects.get(id_expediente=guardar.id_expediente),
                    id_tproceso = TProcesos.objects.get(id_tproceso=proceso)               ,
                    aprobado = False,
                    estado = 'Pendiente',
                    anexo = None,
                )
                nuevo_proceso.save()            
        else:
            procesos2 = [7,4,8,9,10,11,12]

            for proceso in procesos2:

                nuevo_proceso = Procesos(
                    id_expediente = Expediente.objects.get(id_expediente=guardar.id_expediente),
                    id_tproceso = TProcesos.objects.get(id_tproceso=proceso),
                    aprobado = False,
                    estado = 'Pendiente',
                    anexo = None,
                )
                nuevo_proceso.save()
        return redirect('participante')

    else:
        return HttpResponse("Metodo no permitido", status=405)

@login_required
def consulta(request):
    return render(request, 'consulta.html')

@login_required
def seguridad(request):
    if request.method == 'GET':
        id = Usuario.objects.filter(usuario=request.user.username).values_list('id_usuario', flat=True).first()
        data = Persona.objects.get(id_usuario=id)  # Obtener los datos del usuario logueado         
        usuario = Usuario.objects.get(usuario=request.user.username)
        tipo = Persona.objects.filter(id_usuario=usuario.id_usuario).values_list('tipo_usuario', flat=True).first()
        print(f"datros de prueba", tipo)
        return render(request, 'seguridad.html', {'datos': data, 'tipos': tipo})
        
    else:
        return HttpResponse("Metodo no permitido", status=405)

@login_required
def cargar_menciones(request):
    carrera_id = request.GET.get('carrera_id')
    print (f"ID de carrera recibido: {carrera_id}")
    # Importante: Usar el nombre del campo ForeignKey correcto (ej. 'carrera')
    menciones = Mencion.objects.filter(id_carrera=carrera_id).order_by('nombre')
    print (f"Menciones encontradas: {menciones}")

    #tutores = Tutor.objects.filter(id_mencion=menciones).order_by('persona__apellido')

    
    # Crear una lista de diccionarios para enviar como JSON
    menciones_list = [{'id': m.id_mencion, 'nombre': m.nombre} for m in menciones]    
    return JsonResponse(menciones_list, safe=False)

@login_required
def cargar_tutores(request):

    mencion_id = request.GET.get('mencion_id')
    tutores = Tutor.objects.filter(id_carrera=mencion_id)
    
    print (f"ID de mención recibido: {tutores.count()}")
    tutores_list = [
        {'id': t.id_tutor, 'nombre_completo': f"{t.id_persona.nombre} {t.id_persona.apellido}"} 
        for t in tutores
    ]
    
    return JsonResponse(tutores_list, safe=False)

@login_required
def signout(request):
    print(f"Usuario que cierra sesión: {request.user.username}")
    logout(request)
    return redirect('index')    

# Función auxiliar para determinar si un FileField/ImageField tiene contenido
def check_file_status(file_field):
    """Devuelve 'Existente' si el campo tiene un archivo, 'Falta soporte' si es None/vacio."""
    # Los FileField/ImageField se evalúan como True si tienen un archivo cargado.
    if file_field:
        return 'Existente'
    return 'Falta soporte'

# Función auxiliar para formatear fechas que pueden ser nulas
def format_date_or_empty(date_field, is_datetime=False):
    """Formatea un campo de fecha o devuelve una cadena vacía si es nulo."""
    if date_field:
        fmt = '%Y-%m-%d %H:%M:%S' if is_datetime else '%Y-%m-%d'
        return date_field.strftime(fmt)
    return ''
@login_required
def reporte(request):
    """
    Genera un archivo CSV con todos los registros del modelo Expediente,
    incluyendo lógica personalizada para los campos de archivo.
    """
    
    # 1. Configuración de la Respuesta HTTP
    response = HttpResponse(content_type='text/csv')
    
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'expedientes_completos_{now}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # 2. Creación y Configuración del Escritor CSV
    writer = csv.writer(response)

    # 3. Escribir el Encabezado (Headers) - Incluye TODOS los campos del modelo
    headers = [
        'ID Expediente', 'ID Persona', 'ID Tutor', 'ID Mención', 
        'Periodo Inicio', 'Periodo Fin', 'Periodo Cierre', 'Acreditación', 
        'Fecha Registro', 'Estado',
        'Doc. Identidad', 'Foto Perfil', 'Const. Notas', 
        'Const. Inscripción', 'Const. Asistencia', 'Formulario 1'
    ]
    writer.writerow(headers)

    # 4. Escribir los Datos
    expedientes = Expediente.objects.all()

    for expediente in expedientes:

        # Construcción de la fila de datos
        row_data = [
            # 1. Campos directos / PK
            expediente.id_expediente,
            
            # 2. Foreign Keys (usamos .id para obtener solo el PK, manejando None)
            expediente.id_persona_id if expediente.id_persona_id else '',
            expediente.id_tutor_id if expediente.id_tutor_id else '',
            expediente.id_mencion_id if expediente.id_mencion_id else '',
            
            # 3. Campos de Fecha/Tiempo
            format_date_or_empty(expediente.periodo_inicio),
            format_date_or_empty(expediente.periodo_fin),
            format_date_or_empty(expediente.periodo_cierre),
            
            # 4. Booleanos
            'Sí' if expediente.acreditacion else 'No',
            
            # 5. DateTime
            format_date_or_empty(expediente.fecha_registro, is_datetime=True),
            
            # 6. CharField
            expediente.estado,
            
            # 7. Campos de Archivo (ImageField/FileField) - Lógica de 'Existente'/'Falta soporte'
            check_file_status(expediente.doc_identidad),
            check_file_status(expediente.foto_perfil),
            check_file_status(expediente.const_notas),
            check_file_status(expediente.const_inscripcion),
            check_file_status(expediente.asistencia),
            check_file_status(expediente.forma_1),
        ]
        
        # Escribe la fila en el CSV
        writer.writerow(row_data)

    return response