import flet as ft
import datetime
from perfil import vista_perfil
from tienda_vidas import dialogo_tienda_vidas
from tienda_diamantes import dialogo_tienda_diamantes
from racha_calendario import dialogo_racha_calendario
from leccion_visual import vista_leccion
from ligas import vista_ligas
from database import actualizar_recursos, actualizar_perfil_bd, actualizar_progreso_juego, autenticar_jugador, registrar_jugador, obtener_datos_jugador, obtener_configuracion_app

async def main(page: ft.Page):
    VERSION_APP = "0.6.7-alpha"

    page.title = "Numo"

    page.title = "Numo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.WHITE

    estado_juego = {}
    
    # UI Elements Topbar
    texto_vidas_topbar = ft.Text("", color=ft.Colors.RED_500, weight=ft.FontWeight.BOLD)
    texto_diamantes_topbar = ft.Text("", color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD)
    
    icono_racha_topbar = ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.GREY_400)
    texto_racha_topbar = ft.Text("0", color=ft.Colors.GREY_400, weight=ft.FontWeight.BOLD)
    
    contenedor_principal = ft.Container(expand=True)

    # --- FUNCIONES DE BASE DE DATOS Y ESTADO ---
    def guardar_recursos():
        actualizar_recursos(estado_juego["id"], estado_juego["vidas"], estado_juego["diamantes"])

    def actualizar_vidas(nuevas_vidas):
        estado_juego["vidas"] = nuevas_vidas
        texto_vidas_topbar.value = str(estado_juego["vidas"])
        guardar_recursos()
        page.update()

    def actualizar_diamantes(nuevos_diamantes):
        estado_juego["diamantes"] = nuevos_diamantes
        texto_diamantes_topbar.value = str(estado_juego["diamantes"])
        guardar_recursos()
        page.update()

    def al_perder_vida():
        if estado_juego["vidas"] > 0:
            estado_juego["vidas"] -= 1
            texto_vidas_topbar.value = str(estado_juego["vidas"])
            guardar_recursos()
            page.update()

    def evaluar_estado_racha():
        """Verifica si han pasado más de 24 horas y actualiza la UI superior"""
        ahora = datetime.datetime.now()
        if estado_juego["racha"] > 0 and estado_juego["ultima_interaccion"]:
            tiempo_pasado = (ahora - estado_juego["ultima_interaccion"]).total_seconds()
            if tiempo_pasado > 86400: # Pasaron 24 horas
                estado_juego["racha"] = 0
                estado_juego["ultima_interaccion"] = None
                
        racha_activa = estado_juego["racha"] > 0
        color_racha = ft.Colors.ORANGE_500 if racha_activa else ft.Colors.GREY_400
        icono_racha_topbar.color = color_racha
        texto_racha_topbar.color = color_racha
        texto_racha_topbar.value = str(estado_juego["racha"])
        page.update()

    def abrir_tienda_vidas(e):
        dialog = dialogo_tienda_vidas(page, estado_juego["vidas"], estado_juego["diamantes"], abrir_tienda_diamantes, actualizar_vidas, actualizar_diamantes)
        if dialog not in page.overlay: page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    def abrir_tienda_diamantes(e=None):
        dialog_diamantes = dialogo_tienda_diamantes(page, diamantes=estado_juego["diamantes"], on_diamantes_cambiados=actualizar_diamantes)
        if dialog_diamantes not in page.overlay: page.overlay.append(dialog_diamantes)
        dialog_diamantes.open = True
        page.update()

    def abrir_racha_calendario(e):
        evaluar_estado_racha()
        dialog_racha = dialogo_racha_calendario(
            page, 
            racha=estado_juego["racha"], 
            ultima_interaccion=estado_juego["ultima_interaccion"],
            dias_jugados=estado_juego["dias_jugados"]
        )
        if dialog_racha not in page.overlay: page.overlay.append(dialog_racha)
        dialog_racha.open = True
        page.update()

    def actualizar_datos_perfil(nuevo_nombre, nueva_descripcion, nuevo_icono, nuevo_color):
        estado_juego["usuario"] = nuevo_nombre
        estado_juego["descripcion"] = nueva_descripcion
        estado_juego["avatar_icono"] = nuevo_icono
        estado_juego["avatar_color"] = nuevo_color

        nombre_icono = nuevo_icono.name if hasattr(nuevo_icono, 'name') else str(nuevo_icono)
        actualizar_perfil_bd(estado_juego["id"], nuevo_nombre, nueva_descripcion, nombre_icono, nuevo_color)

        page.snack_bar = ft.SnackBar(content=ft.Text("¡Perfil actualizado! 🥳"), bgcolor=ft.Colors.GREEN_500)
        page.snack_bar.open = True
        page.update()

    def restaurar_vista_principal():
        evaluar_estado_racha()
        if page.appbar: page.appbar.visible = True
        if page.navigation_bar: page.navigation_bar.visible = True
        contenedor_principal.content = crear_vista_inicio()
        page.update()

    def abrir_perfil_publico(jugador_publico):
        """Renderiza la vista de perfil de otro jugador, bloqueando la edición."""
        
        # Función "trampa" para evitar que editen a otros jugadores
        def edicion_denegada(n, d, i, c):
            page.snack_bar = ft.SnackBar(content=ft.Text("Estás viendo un perfil público. No puedes editarlo.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_500)
            if hasattr(page, 'open'): page.open(page.snack_bar)
            else:
                page.snack_bar.open = True
                page.update()

        insignias_str = jugador_publico.get("insignias") or "novato"
        lista_insignias = insignias_str.split(",")

        # 1. Protegemos contra datos Nulos (None) que vienen de la base de datos
        desc_segura = jugador_publico.get("descripcion")
        if not desc_segura:
            desc_segura = "Sin descripción..."

        niveles_seguros = jugador_publico.get("niveles_completados")
        if niveles_seguros is None:
            niveles_seguros = 0

        # 2. Formateamos el icono exactamente como lo procesa el login
        icono_str = jugador_publico.get("avatar_icono") or "ACCOUNT_CIRCLE"
        icono_resuelto = getattr(ft.Icons, icono_str, ft.Icons.ACCOUNT_CIRCLE)
        
        color_seguro = jugador_publico.get("avatar_color") or "blue"

        # 3. Sincronizamos la barra inferior para que indique que estamos en el Perfil (Índice 2)
        if page.navigation_bar:
            page.navigation_bar.selected_index = 2

        # Reemplazamos el contenido principal con los datos totalmente seguros
        contenedor_principal.content = vista_perfil(
            page=page, 
            usuario=jugador_publico.get("usuario", "Jugador"), 
            descripcion=desc_segura,
            xp_total=jugador_publico.get("xp_total", 0), 
            insignias=lista_insignias,
            racha_total=0, 
            niveles_total=niveles_seguros,
            avatar_icono=icono_resuelto, # Pasamos el icono procesado
            avatar_color=color_seguro,
            on_guardar_perfil=edicion_denegada,
            on_cerrar_sesion=None,
            es_perfil_propio=False
        )
        page.update()

    def al_completar_leccion(nivel_completado, xp_ganada):
        estado_juego["xp_total"] += xp_ganada
        ahora = datetime.datetime.now()

        # Solo sube racha si es un nivel NUEVO
        if nivel_completado > estado_juego["niveles_completados"]:
            estado_juego["niveles_completados"] = nivel_completado
            
            # Lógica de temporizador de 24 hrs
            if estado_juego["ultima_interaccion"]:
                tiempo_pasado = (ahora - estado_juego["ultima_interaccion"]).total_seconds()
                if tiempo_pasado <= 86400: # Menos de 24h
                    estado_juego["racha"] += 1
                else:
                    estado_juego["racha"] = 1 # Pasaron 24h, reinicia
            else:
                estado_juego["racha"] = 1 # Primera vez
            
            estado_juego["ultima_interaccion"] = ahora
            estado_juego["dias_jugados"].add(ahora.date())
            # NOTA: Asegúrate de guardar `racha`, `ultima_interaccion` y `dias_jugados` en tu base de datos aquí.

        actualizar_progreso_juego(estado_juego["id"], estado_juego["niveles_completados"], estado_juego["xp_total"])
        restaurar_vista_principal()

    def al_salir_leccion():
        restaurar_vista_principal()

    def iniciar_leccion(nivel):
        es_teoria = nivel in [1, 3, 6, 8, 10]
        if not es_teoria and estado_juego["vidas"] <= 0:
            abrir_tienda_vidas(None)
            return
            
        if page.appbar: page.appbar.visible = False
        if page.navigation_bar: page.navigation_bar.visible = False
        
        contenedor_principal.content = vista_leccion(
            page=page, nivel=nivel, vidas_actuales=estado_juego["vidas"], 
            on_completado=al_completar_leccion, on_salir=al_salir_leccion, on_perder_vida=al_perder_vida         
        )
        page.update()

    # --- VISTAS DEL JUEGO ---
    def crear_vista_inicio():
        camino_lecciones = ft.Column(scroll=ft.ScrollMode.HIDDEN, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, expand=True)

        seccion_1_header = ft.Container(
            content=ft.Column([
                ft.Text("SECCIÓN 1", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                ft.Text("Aritmética Básica", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=22),
                ft.Text("Domina los números desde cero. Sumas, Restas, Multiplicaciones, Divisiones y Orden de Operaciones.", color=ft.Colors.WHITE70, size=14),
            ], spacing=5),
            bgcolor=ft.Colors.PURPLE_500, padding=20, border_radius=15, margin=ft.margin.symmetric(horizontal=15, vertical=10), width=float('inf')
        )
        camino_lecciones.controls.append(seccion_1_header)

        niveles_seccion_1 = 12
        progreso_actual = estado_juego["niveles_completados"] 

        for i in range(niveles_seccion_1):
            if i % 4 == 0: alineacion = ft.Alignment.CENTER
            elif i % 4 == 1: alineacion = ft.Alignment.CENTER_LEFT
            elif i % 4 == 2: alineacion = ft.Alignment.CENTER
            else: alineacion = ft.Alignment.CENTER_RIGHT

            es_completado = i < progreso_actual
            es_nivel_actual = i == progreso_actual
            es_bloqueado = i > progreso_actual

            numero_nivel = i + 1
            es_ultimo_nivel = (numero_nivel == niveles_seccion_1) 

            if es_ultimo_nivel:
                icono_boton = ft.Icons.EMOJI_EVENTS
                if es_bloqueado:
                    color_boton = ft.Colors.GREY_300
                    color_icono = ft.Colors.WHITE
                    evento_click = None
                else:
                    color_boton = ft.Colors.AMBER_400 
                    color_icono = ft.Colors.BROWN_700 
                    evento_click = lambda e, n=numero_nivel: iniciar_leccion(n)
            else:
                es_teoria = numero_nivel in [1, 3, 6, 8, 10]
                color_icono = ft.Colors.WHITE
                
                if es_teoria:
                    icono_boton = ft.Icons.MENU_BOOK 
                    if es_completado:
                        color_boton = ft.Colors.CYAN_500 
                        evento_click = lambda e, n=numero_nivel: iniciar_leccion(n)
                    elif es_nivel_actual:
                        color_boton = ft.Colors.CYAN_500 
                        evento_click = lambda e, n=numero_nivel: iniciar_leccion(n)
                    else: 
                        color_boton = ft.Colors.GREY_300 
                        evento_click = None
                else:
                    if es_completado:
                        color_boton = ft.Colors.PURPLE_500
                        icono_boton = ft.Icons.STAR
                        evento_click = lambda e, n=numero_nivel: iniciar_leccion(n)
                    elif es_nivel_actual:
                        color_boton = ft.Colors.PURPLE_500
                        icono_boton = ft.Icons.PLAY_ARROW
                        evento_click = lambda e, n=numero_nivel: iniciar_leccion(n)
                    else: 
                        color_boton = ft.Colors.GREY_300
                        icono_boton = ft.Icons.LOCK
                        evento_click = None

            boton_nivel = ft.Container(
                content=ft.Button(
                    content=ft.Icon(icono_boton, color=color_icono, size=40 if es_ultimo_nivel else 35),
                    style=ft.ButtonStyle(
                        shape=ft.CircleBorder(), padding=25, bgcolor=color_boton,
                        elevation=12 if es_nivel_actual and not es_ultimo_nivel else 3,
                    ),
                    width=110 if es_ultimo_nivel else (100 if es_nivel_actual else 90),
                    height=110 if es_ultimo_nivel else (100 if es_nivel_actual else 90),
                    on_click=evento_click
                ),
                alignment=alineacion, padding=ft.padding.symmetric(horizontal=50)
            )
            camino_lecciones.controls.append(boton_nivel)
            
        seccion_2_header = ft.Container(
            content=ft.Column([
                ft.Text("SECCIÓN 2", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                ft.Text("Aritmética Intermedia", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=22),
                ft.Text("Números negativos, Fracciones, Decimales y Porcentajes.", color=ft.Colors.WHITE70, size=14),
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_500, padding=20, border_radius=15, margin=ft.margin.only(left=15, right=15, top=30, bottom=10), width=float('inf')
        )
        camino_lecciones.controls.append(seccion_2_header)

        boton_bloqueado = ft.Container(
            content=ft.Button(
                content=ft.Icon(ft.Icons.LOCK, color=ft.Colors.WHITE, size=35),
                style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=25, bgcolor=ft.Colors.GREY_300, shadow_color=ft.Colors.BLACK, elevation=3),
                width=90, height=90,
            ),
            alignment=ft.Alignment.CENTER, padding=ft.padding.symmetric(horizontal=50)
        )
        camino_lecciones.controls.append(boton_bloqueado)
        camino_lecciones.controls.append(ft.Container(height=50))
        
        return camino_lecciones

    def cambiar_seccion(e):
            index = e.control.selected_index
            if index == 0: 
                contenedor_principal.content = crear_vista_inicio()
            elif index == 1: 
                # Llama a la nueva vista de ligas pasando la page y el ID del usuario actual
                contenedor_principal.content = vista_ligas(page, estado_juego["id"], abrir_perfil_publico) 
            elif index == 2: 
                contenedor_principal.content = vista_perfil(
                    page=page, usuario=estado_juego["usuario"], descripcion=estado_juego["descripcion"],
                    xp_total=estado_juego["xp_total"], insignias=estado_juego["insignias"],
                    racha_total=estado_juego["racha"], niveles_total=estado_juego["niveles_completados"],
                    avatar_icono=estado_juego["avatar_icono"], avatar_color=estado_juego["avatar_color"],
                    on_guardar_perfil=actualizar_datos_perfil,
                    on_cerrar_sesion=cerrar_sesion,
                    es_perfil_propio=True
                )
            page.update()

    # --- INICIALIZAR LA INTERFAZ TRAS LOGIN ---
    def iniciar_app_principal():
        page.clean() 
        
        texto_vidas_topbar.value = str(estado_juego["vidas"])
        texto_diamantes_topbar.value = str(estado_juego["diamantes"])
        evaluar_estado_racha()

        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.CALCULATE, color=ft.Colors.BLUE_500, size=30), leading_width=60,
            title=ft.Row(
                [
                    ft.Container(content=ft.Row([icono_racha_topbar, texto_racha_topbar]), on_click=abrir_racha_calendario, ink=True, padding=5, border_radius=5),
                    ft.Container(content=ft.Row([ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_500), texto_vidas_topbar]), on_click=abrir_tienda_vidas, ink=True, padding=5, border_radius=5),
                    ft.Container(content=ft.Row([ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.BLUE_400), texto_diamantes_topbar]), on_click=abrir_tienda_diamantes, ink=True, padding=5, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, expand=True,
            ), bgcolor=ft.Colors.WHITE, toolbar_height=70,
        )

        contenedor_principal.content = crear_vista_inicio()
        page.navigation_bar = ft.NavigationBar(
            selected_index=0, bgcolor=ft.Colors.WHITE, on_change=cambiar_seccion, 
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Aprender"),
                ft.NavigationBarDestination(icon=ft.Icons.LEADERBOARD, label="Ligas"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
            ]
        )

        page.add(contenedor_principal)
        page.update()

    # ==========================================
    # --- SISTEMA DE AUTENTICACIÓN INTERNO ---
    # ==========================================
    
    def procesar_entrada_juego(datos_bd):
        texto_insignias = datos_bd.get("insignias", "novato")
        lista_insignias = texto_insignias.split(",") if texto_insignias else []

        # Inicializa valores de racha (Asegurar que la BD devuelve esto, de lo contrario valores por defecto)
        estado_juego.update({
            "id": datos_bd["id"], 
            "niveles_completados": datos_bd["niveles_completados"],
            "xp_total": datos_bd.get("xp_total", 0),
            "insignias": lista_insignias,
            "vidas": datos_bd["vidas"],
            "diamantes": datos_bd["diamantes"],
            "usuario": datos_bd["usuario"],
            "descripcion": datos_bd["descripcion"],
            "avatar_icono": getattr(ft.Icons, datos_bd.get("avatar_icono", "ACCOUNT_CIRCLE"), ft.Icons.ACCOUNT_CIRCLE),
            "avatar_color": datos_bd.get("avatar_color", "blue").lower(),
            
            # NUEVAS VARIABLES
            "racha": datos_bd.get("racha", 0), 
            "ultima_interaccion": datos_bd.get("ultima_interaccion", None), # Debe ser un objeto datetime o None
            "dias_jugados": set(datos_bd.get("dias_jugados", [])) # Set de objetos datetime.date
        })
        iniciar_app_principal()

    def mostrar_error(mensaje):
        snack = ft.SnackBar(content=ft.Text(mensaje, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_500)
        if hasattr(page, 'open'): page.open(snack)
        else:
            page.overlay.append(snack)
            snack.open = True
            page.update()

    def mostrar_exito(mensaje):
        snack = ft.SnackBar(content=ft.Text(mensaje, color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_500)
        if hasattr(page, 'open'): page.open(snack)
        else:
            page.overlay.append(snack)
            snack.open = True
            page.update()

    def cerrar_sesion(e=None):
        # 1. Borramos el ID del dispositivo de forma asíncrona usando una tarea
        page.run_task(ft.SharedPreferences().remove, "sesion_usuario_id")
        
        # 2. Limpiamos la pantalla actual y quitamos las barras de navegación
        page.clean()
        page.appbar = None
        page.navigation_bar = None
        
        # 3. Reseteamos el estado local del juego
        estado_juego.clear()
        
        # 4. Volvemos a mostrar la pantalla de login
        vista_login.visible = True
        vista_registro.visible = False
        page.add(vista_login, vista_registro)
        page.update()

    def btn_iniciar_sesion(e):
        identificador = campo_login_id.value.strip()
        password = campo_login_pass.value.strip()

        if not identificador or not password:
            mostrar_error("Por favor, llena todos los campos.")
            return

        jugador, mensaje = autenticar_jugador(identificador, password)
        if jugador:
            page.run_task(ft.SharedPreferences().set, "sesion_usuario_id", jugador["id"])
            procesar_entrada_juego(jugador)
        else:
            mostrar_error(mensaje)

    def btn_registrar(e):
        email = campo_reg_email.value.strip()
        usuario = campo_reg_user.value.strip()
        password = campo_reg_pass.value.strip()

        if not email or not usuario or not password:
            mostrar_error("Todos los campos son obligatorios.")
            return
        
        if "@" not in email or "." not in email:
            mostrar_error("Introduce un correo electrónico válido.")
            return

        exito, mensaje = registrar_jugador(email, usuario, password)
        if exito:
            mostrar_exito("¡Cuenta creada! Inicia sesión para continuar.")
            cambiar_a_login(None)
            campo_reg_email.value = ""
            campo_reg_user.value = ""
            campo_reg_pass.value = ""
        else: mostrar_error(mensaje)

    def cambiar_a_registro(e):
        vista_login.visible = False
        vista_registro.visible = True
        page.update()

    def cambiar_a_login(e):
        vista_registro.visible = False
        vista_login.visible = True
        page.update()

    # --- INTERFAZ DE LOGIN ---
    campo_login_id = ft.TextField(label="Correo o Usuario", prefix_icon=ft.Icons.PERSON, width=300)
    campo_login_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK, width=300)

    async def intentar_auto_login():
        """Revisa si hay una sesión guardada e inicia automáticamente."""
        usuario_id = await ft.SharedPreferences().get("sesion_usuario_id")
        if usuario_id:
            # Si hay un ID guardado, pedimos los datos a la BD
            jugador = obtener_datos_jugador(usuario_id)
            if jugador:
                procesar_entrada_juego(jugador)
                return True # Auto-login exitoso
        return False # No hay sesión o el jugador ya no existe

    vista_login = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.CALCULATE, size=80, color=ft.Colors.BLUE_500),
            ft.Text("Numo", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_500),
            ft.Container(height=20),
            campo_login_id,
            campo_login_pass,
            ft.Container(height=10),
            ft.Button("Iniciar Sesión", icon=ft.Icons.LOGIN, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE, padding=15), width=300, on_click=btn_iniciar_sesion),
            ft.TextButton("¿No tienes cuenta? Regístrate aquí", on_click=cambiar_a_registro)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.Alignment.CENTER, expand=True, visible=True
    )

    # --- INTERFAZ DE REGISTRO ---
    campo_reg_email = ft.TextField(label="Correo Electrónico", prefix_icon=ft.Icons.EMAIL, width=300)
    campo_reg_user = ft.TextField(label="Nombre de Usuario", prefix_icon=ft.Icons.PERSON_OUTLINE, width=300)
    campo_reg_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK, width=300)

    vista_registro = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.PERSON_ADD, size=70, color=ft.Colors.PURPLE_500),
            ft.Text("Crear Cuenta", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Container(height=10),
            campo_reg_email,
            campo_reg_user,
            campo_reg_pass,
            ft.Container(height=10),
            ft.Button("Registrarse", icon=ft.Icons.HOW_TO_REG, style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_500, color=ft.Colors.WHITE, padding=15), width=300, on_click=btn_registrar),
            ft.TextButton("¿Ya tienes cuenta? Inicia Sesión", on_click=cambiar_a_login)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.Alignment.CENTER, expand=True, visible=False
    )

    def verificar_actualizacion():
        """Verifica en la BD si existe una versión más nueva."""
        config = obtener_configuracion_app()
        
        # Si la versión de la BD es diferente a la de este código
        if config and config["version_actual"] != VERSION_APP:
            dialogo_actualizacion = ft.AlertDialog(
                modal=True, # Evita que se cierre haciendo clic fuera
                title=ft.Text("¡Nueva versión disponible!", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_600),
                content=ft.Text(f"Tienes la versión {VERSION_APP} pero la {config['version_actual']} ya está lista.\n\nEs necesario actualizar para seguir jugando."),
                actions=[
                    ft.ElevatedButton(
                        "Descargar Actualización", 
                        icon=ft.Icons.DOWNLOAD,
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_500,
                        on_click=lambda e: page.launch_url(config["enlace_descarga"])
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            page.overlay.append(dialogo_actualizacion)
            dialogo_actualizacion.open = True
            page.update()
            return True # Retorna True si hay una actualización que bloquea la app
            
        return False # Todo está al día

    # 1. Creamos las vistas pero no las añadimos a la página todavía
    vista_login.visible = True
    vista_registro.visible = False
    
    hay_actualizacion = verificar_actualizacion()

    # 2. Intentamos el auto-login
    if not hay_actualizacion:
        if not await intentar_auto_login():
            # Si falla (no hay sesión), entonces sí mostramos la pantalla de inicio de sesión
            page.add(vista_login, vista_registro)

ft.run(main)
#ft.app(target=main, view=ft.AppView.WEB_BROWSER)
