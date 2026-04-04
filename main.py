import flet as ft
import datetime
import time
import asyncio
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
    contenedor_icono_racha = ft.Container(
        content=icono_racha_topbar,
        scale=1.0,
        animate_scale=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT)
    )
    texto_racha_topbar = ft.Text("0", color=ft.Colors.GREY_400, weight=ft.FontWeight.BOLD)
    
    contenedor_principal = ft.AnimatedSwitcher(
        content=ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=400, # 400 ms de desvanecimiento
        reverse_duration=400,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
        expand=True
    )

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
        vista_inicio = crear_vista_inicio()
        vista_inicio.key = "inicio"

        evaluar_estado_racha()
        if page.appbar: page.appbar.visible = True
        if page.navigation_bar: page.navigation_bar.visible = True
        contenedor_principal.content = vista_inicio
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
        vista = vista_perfil(
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
        vista.key = f"perfil_publico_{jugador_publico.get('id', 'temp')}"
        contenedor_principal.content = vista
        page.update()

    def al_completar_leccion(nivel_completado, xp_ganada):
        estado_juego["xp_total"] += xp_ganada
        ahora = datetime.datetime.now()

        # 1. LÓGICA DE RACHA (Se activa/mantiene con CUALQUIER lección jugada en el día)
        if estado_juego["ultima_interaccion"]:
            tiempo_pasado = (ahora - estado_juego["ultima_interaccion"]).total_seconds()
            es_mismo_dia = ahora.date() == estado_juego["ultima_interaccion"].date()

            if es_mismo_dia:
                pass # Ya jugó hoy, la racha se mantiene igual (no suma múltiples veces al día)
            elif tiempo_pasado <= 86400:
                estado_juego["racha"] += 1 # Jugó al día siguiente dentro de las 24 hrs
            else:
                estado_juego["racha"] = 1 # Pasaron más de 24 hrs sin jugar, pierde racha y vuelve a 1
        else:
            estado_juego["racha"] = 1 # Primera vez en la vida que juega

        # Reiniciamos el temporizador de 24 horas exactas a este momento
        estado_juego["ultima_interaccion"] = ahora
        estado_juego["dias_jugados"].add(ahora.date())

        # 2. LÓGICA DE PROGRESO (Solo avanza la ruta si es un nivel NUEVO)
        if nivel_completado > estado_juego["niveles_completados"]:
            estado_juego["niveles_completados"] = nivel_completado

        # ---> NUEVO: Convertimos las fechas a un texto para la BD <---
        dias_str = ",".join([d.strftime("%Y-%m-%d") for d in estado_juego["dias_jugados"]])

        actualizar_progreso_juego(
            estado_juego["id"], 
            estado_juego["niveles_completados"], 
            estado_juego["xp_total"],
            estado_juego["racha"],
            estado_juego["ultima_interaccion"],
            dias_str
        )
        restaurar_vista_principal()

    def al_salir_leccion():
        restaurar_vista_principal()

    def iniciar_leccion(nivel):
        es_teoria = nivel in [1, 3, 6, 8, 10, 13, 15, 17, 29, 21]
        if not es_teoria and estado_juego["vidas"] <= 0:
            abrir_tienda_vidas(None)
            return
            
        if page.appbar: page.appbar.visible = False
        if page.navigation_bar: page.navigation_bar.visible = False
        
        vista = vista_leccion(
            page=page, nivel=nivel, vidas_actuales=estado_juego["vidas"], 
            on_completado=al_completar_leccion, on_salir=al_salir_leccion, on_perder_vida=al_perder_vida         
        )
        vista.key = f"leccion_{nivel}"
        contenedor_principal.content = vista
        page.update()

    async def motor_latido_racha():
        while True:
            # Solo late si la racha es mayor a 0
            if estado_juego.get("racha", 0) > 0:
                # Intercala entre escala 1.0 y 1.15
                contenedor_icono_racha.scale = 1.15 if contenedor_icono_racha.scale == 1.0 else 1.0
            else:
                contenedor_icono_racha.scale = 1.0 # Se queda quieto si no hay racha
            
            try:
                contenedor_icono_racha.update()
            except:
                pass # Evita errores si la app se está cerrando
                
            await asyncio.sleep(0.8) # Velocidad del latido

    # Ejecutamos el motor en segundo plano sin bloquear la app
    page.run_task(motor_latido_racha)

    # --- VISTAS DEL JUEGO ---
    def crear_vista_inicio():
        camino_lecciones = ft.Column(scroll=ft.ScrollMode.HIDDEN, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, expand=True)
        botones_a_animar = []

        seccion_1_header = ft.Container(
            content=ft.Column([
                ft.Text("SECCIÓN 1", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                ft.Text("Aritmética Básica", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=22),
                ft.Text("Domina los números desde cero. Sumas, Restas, Multiplicaciones, Divisiones y Orden de Operaciones.", color=ft.Colors.WHITE70, size=14),
            ], spacing=5),
            bgcolor=ft.Colors.PURPLE_500, padding=20, border_radius=15, margin=ft.Margin.only(left=15, right=15, top=10, bottom=10), width=float('inf')
        )
        camino_lecciones.controls.append(seccion_1_header)

        def animar_y_ejecutar(e, n):
            # 1. Escala hacia abajo al 90%
            e.control.scale = 0.9
            e.control.update()
            
            # 2. Pausa muy breve para percibir la contracción
            time.sleep(0.1)
            
            # 3. Regresa a su tamaño original (el AnimationCurve hará el rebote)
            e.control.scale = 1.0
            e.control.update()
            
            # 4. Pausa para terminar el rebote antes de congelar la UI para cargar la lección
            time.sleep(0.15)
            
            # 5. Ejecutar la acción real
            iniciar_leccion(n)

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
                    evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
            else:
                es_teoria = numero_nivel in [1, 3, 6, 8, 10]
                color_icono = ft.Colors.WHITE
                
                if es_teoria:
                    icono_boton = ft.Icons.MENU_BOOK 
                    if es_completado:
                        color_boton = ft.Colors.CYAN_500 
                        evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
                    elif es_nivel_actual:
                        color_boton = ft.Colors.CYAN_500 
                        evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
                    else: 
                        color_boton = ft.Colors.GREY_300 
                        evento_click = None
                else:
                    if es_completado:
                        color_boton = ft.Colors.PURPLE_500
                        icono_boton = ft.Icons.STAR
                        evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
                    elif es_nivel_actual:
                        color_boton = ft.Colors.PURPLE_500
                        icono_boton = ft.Icons.PLAY_ARROW
                        evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
                    else: 
                        color_boton = ft.Colors.GREY_300
                        icono_boton = ft.Icons.LOCK
                        evento_click = None

            boton_nivel = ft.Container(
                key="nivel_actual" if es_nivel_actual else None,
                
                # ---> AÑADE ESTAS PROPIEDADES DE ANIMACIÓN
                opacity=0, 
                offset=ft.Offset(0, 0.3), # Empieza un 30% más abajo
                animate_opacity=ft.Animation(400, ft.AnimationCurve.DECELERATE),
                animate_offset=ft.Animation(400, ft.AnimationCurve.DECELERATE),
                content=ft.Button(
                    content=ft.Icon(icono_boton, color=color_icono, size=40 if es_ultimo_nivel else 35),
                    style=ft.ButtonStyle(
                        shape=ft.CircleBorder(), padding=25, bgcolor=color_boton,
                        elevation=12 if es_nivel_actual and not es_ultimo_nivel else 3,
                    ),
                    width=110 if es_ultimo_nivel else (100 if es_nivel_actual else 90),
                    height=110 if es_ultimo_nivel else (100 if es_nivel_actual else 90),
                    on_click=evento_click,
                    scale=1.0,
                    animate_scale=ft.Animation(duration=150, curve=ft.AnimationCurve.EASE_OUT_BACK)
                ),
                alignment=alineacion, padding=ft.Padding.symmetric(horizontal=50)
            )
            camino_lecciones.controls.append(boton_nivel)
            botones_a_animar.append(boton_nivel)        
        seccion_2_header = ft.Container(
            content=ft.Column([
                ft.Text("SECCIÓN 2", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                ft.Text("Aritmética Intermedia", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=22),
                ft.Text("Números negativos, Fracciones, Decimales y Porcentajes.", color=ft.Colors.WHITE70, size=14),
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_500, padding=20, border_radius=15, margin=ft.Margin.only(left=15, right=15, top=30, bottom=10), width=float('inf')
        )
        camino_lecciones.controls.append(seccion_2_header)

        niveles_seccion_2 = 13
        for i in range(12, 12 + niveles_seccion_2):
            numero_nivel = i + 1 # Va del 13 al 25
            
            if i % 4 == 0: alineacion = ft.Alignment.CENTER
            elif i % 4 == 1: alineacion = ft.Alignment.CENTER_LEFT
            elif i % 4 == 2: alineacion = ft.Alignment.CENTER
            else: alineacion = ft.Alignment.CENTER_RIGHT

            es_completado = i < progreso_actual
            es_nivel_actual = i == progreso_actual
            es_bloqueado = i > progreso_actual
            es_ultimo_nivel = (numero_nivel == 25) # El examen de la sección 2

            if es_ultimo_nivel:
                icono_boton = ft.Icons.EMOJI_EVENTS
                if es_bloqueado:
                    color_boton = ft.Colors.GREY_300
                    color_icono = ft.Colors.WHITE
                    evento_click = None
                else:
                    color_boton = ft.Colors.AMBER_400 
                    color_icono = ft.Colors.BROWN_700 
                    evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
            else:
                es_teoria = numero_nivel in [13, 15, 17, 19, 21]
                color_icono = ft.Colors.WHITE
                
                if es_teoria:
                    icono_boton = ft.Icons.MENU_BOOK 
                    if es_completado or es_nivel_actual:
                        color_boton = ft.Colors.CYAN_500 
                        evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
                    else: 
                        color_boton = ft.Colors.GREY_300 
                        evento_click = None
                else:
                    if es_completado:
                        # Color distintivo azul para la Sección 2
                        color_boton = ft.Colors.BLUE_500 
                        icono_boton = ft.Icons.STAR
                        evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
                    elif es_nivel_actual:
                        color_boton = ft.Colors.BLUE_500
                        icono_boton = ft.Icons.PLAY_ARROW
                        evento_click = lambda e, n=numero_nivel: animar_y_ejecutar(e, n)
                    else: 
                        color_boton = ft.Colors.GREY_300
                        icono_boton = ft.Icons.LOCK
                        evento_click = None

            boton_nivel = ft.Container(
                key="nivel_actual" if es_nivel_actual else None,
                opacity=0, offset=ft.Offset(0, 0.3),
                animate_opacity=ft.Animation(400, ft.AnimationCurve.DECELERATE),
                animate_offset=ft.Animation(400, ft.AnimationCurve.DECELERATE),
                content=ft.Button(
                    content=ft.Icon(icono_boton, color=color_icono, size=40 if es_ultimo_nivel else 35),
                    style=ft.ButtonStyle(
                        shape=ft.CircleBorder(), padding=25, bgcolor=color_boton,
                        elevation=12 if es_nivel_actual and not es_ultimo_nivel else 3,
                    ),
                    width=110 if es_ultimo_nivel else (100 if es_nivel_actual else 90),
                    height=110 if es_ultimo_nivel else (100 if es_nivel_actual else 90),
                    on_click=evento_click, scale=1.0, animate_scale=ft.Animation(duration=150, curve=ft.AnimationCurve.EASE_OUT_BACK)
                ),
                alignment=alineacion, padding=ft.Padding.symmetric(horizontal=50)
            )
            camino_lecciones.controls.append(boton_nivel)
            botones_a_animar.append(boton_nivel)

        # Agregamos el header y el candado estático de la Sección 3 para mantener la estructura visual
        seccion_3_header = ft.Container(
            content=ft.Column([
                ft.Text("SECCIÓN 3", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                ft.Text("Álgebra Básica", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=22),
                ft.Text("Variables, Ecuaciones, y el lenguaje de las letras.", color=ft.Colors.WHITE70, size=14),
            ], spacing=5),
            bgcolor=ft.Colors.GREEN_500, padding=20, border_radius=15, margin=ft.Margin.only(left=15, right=15, top=30, bottom=10), width=float('inf')
        )
        camino_lecciones.controls.append(seccion_3_header)
        camino_lecciones.controls.append(
            ft.Container(
                content=ft.Button(
                    content=ft.Icon(ft.Icons.LOCK, color=ft.Colors.WHITE, size=35),
                    style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=25, bgcolor=ft.Colors.GREY_300, shadow_color=ft.Colors.BLACK, elevation=3),
                    width=90, height=90,
                ),
                alignment=ft.Alignment.CENTER, padding=ft.Padding.symmetric(horizontal=50)
            )
        )
        camino_lecciones.controls.append(ft.Container(height=50))

        # --- ANIMACIÓN EN CASCADA Y AUTO-SCROLL ---
        async def entrada_triunfal_niveles():
            await asyncio.sleep(0.1) 
            
            # 1. SCROLL MATEMÁTICO (Funciona en cualquier versión)
            # Calculamos la altura de píxeles (cada botón mide ~110px, los banners ~120px)
            progreso = estado_juego["niveles_completados"]
            offset_y = 0
            
            if progreso < 12: # Si está en la sección 1
                offset_y = 120 + (progreso * 110)
            else:             # Si está en la sección 2
                offset_y = 120 + (12 * 110) + 120 + ((progreso - 12) * 110)
                
            # Restamos 300px para que el nivel actual quede "en medio" de la pantalla, no hasta arriba
            offset_y -= 300
            if offset_y < 0: 
                offset_y = 0
                
            try:
                await camino_lecciones.scroll_to(offset=offset_y, duration=800, curve=ft.AnimationCurve.EASE_OUT)
            except Exception as e:
                pass # Ignorar si la app se cierra a la mitad de la carga
            
            # 2. Hacemos aparecer los botones uno tras otro
            for btn in botones_a_animar:
                btn.opacity = 1
                btn.offset = ft.Offset(0, 0)
                try:
                    btn.update()
                except:
                    break
                await asyncio.sleep(0.04)

        page.run_task(entrada_triunfal_niveles)
        
        return camino_lecciones

    def cambiar_seccion(e):
            index = e.control.selected_index
            if index == 0: 
                nueva_vista = crear_vista_inicio()
                nueva_vista.key = "inicio"
                contenedor_principal.content = nueva_vista
            elif index == 1: 
                nueva_vista = vista_ligas(page, estado_juego["id"], abrir_perfil_publico) 
                nueva_vista.key = "ligas"
                contenedor_principal.content = nueva_vista
            elif index == 2: 
                nueva_vista = vista_perfil(
                    page=page, usuario=estado_juego["usuario"], descripcion=estado_juego["descripcion"],
                    xp_total=estado_juego["xp_total"], insignias=estado_juego["insignias"],
                    racha_total=estado_juego["racha"], niveles_total=estado_juego["niveles_completados"],
                    avatar_icono=estado_juego["avatar_icono"], avatar_color=estado_juego["avatar_color"],
                    on_guardar_perfil=actualizar_datos_perfil,
                    on_cerrar_sesion=cerrar_sesion,
                    es_perfil_propio=True
                )
                nueva_vista.key = "perfil"
                contenedor_principal.content = nueva_vista
            page.update()

    def animar_hover_boton(e):
        # Si el mouse entra (true) crece a 1.05, si sale (false) regresa a 1.0
        e.control.scale = 1.05 if e.data == "true" else 1.0
        e.control.update()

    # --- INICIALIZAR LA INTERFAZ TRAS LOGIN ---
    def iniciar_app_principal():
        page.clean()

        vista_inicio = crear_vista_inicio()
        vista_inicio.key = "inicio"
        contenedor_principal.content = vista_inicio
        
        texto_vidas_topbar.value = str(estado_juego["vidas"])
        texto_diamantes_topbar.value = str(estado_juego["diamantes"])
        evaluar_estado_racha()

        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.CALCULATE, color=ft.Colors.BLUE_500, size=30), leading_width=60,
            title=ft.Row(
                [
                    ft.Container(content=ft.Row([contenedor_icono_racha, texto_racha_topbar]), on_click=abrir_racha_calendario, ink=True, padding=5, border_radius=5),
                    ft.Container(content=ft.Row([ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_500), texto_vidas_topbar]), on_click=abrir_tienda_vidas, ink=True, padding=5, border_radius=5),
                    ft.Container(content=ft.Row([ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.BLUE_400), texto_diamantes_topbar]), on_click=abrir_tienda_diamantes, ink=True, padding=5, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, expand=True,
            ), bgcolor=ft.Colors.WHITE, toolbar_height=70,
        )

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

        # ---> NUEVO: Convertimos el texto de la BD de vuelta a Fechas reales <---
        dias_jugados_str = datos_bd.get("dias_jugados")
        set_dias = set()
        if dias_jugados_str:
            for fecha_str in dias_jugados_str.split(","):
                try:
                    # Convertimos "YYYY-MM-DD" a un objeto date
                    set_dias.add(datetime.datetime.strptime(fecha_str.strip(), "%Y-%m-%d").date())
                except:
                    pass

        # Inicializa valores
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
            
            # VARIABLES DE RACHA REPARADAS
            "racha": datos_bd.get("racha", 0) or 0, 
            "ultima_interaccion": datos_bd.get("ultima_interaccion", None), 
            "dias_jugados": set_dias
        })
        iniciar_app_principal()

    def mostrar_error(mensaje):
        snack = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), 
            bgcolor=ft.Colors.RED_500,
            behavior=ft.SnackBarBehavior.FLOATING, # <-- Efecto flotante
            margin=20, # <-- Separación de los bordes
            border_radius=10, # <-- Bordes redondeados
            elevation=4
        )
        if hasattr(page, 'open'): page.open(snack)
        else:
            page.overlay.append(snack)
            snack.open = True
            page.update()

    def mostrar_exito(mensaje):
        snack = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), 
            bgcolor=ft.Colors.GREEN_500,
            behavior=ft.SnackBarBehavior.FLOATING, 
            margin=20, 
            border_radius=10,
            elevation=4
        )
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
            ft.ElevatedButton(
                "Iniciar Sesión", 
                icon=ft.Icons.LOGIN, 
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE, padding=15, shape=ft.RoundedRectangleBorder(radius=15)), 
                width=300, 
                on_click=btn_iniciar_sesion,
                # -- ANIMACIÓN HOVER --
                scale=1.0,
                animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
                on_hover=animar_hover_boton
            ),
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
            ft.ElevatedButton(
                "Registrarse", 
                icon=ft.Icons.HOW_TO_REG, 
                style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_500, color=ft.Colors.WHITE, padding=15, shape=ft.RoundedRectangleBorder(radius=15)), 
                width=300, 
                on_click=btn_registrar,
                # -- ANIMACIÓN HOVER --
                scale=1.0,
                animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
                on_hover=animar_hover_boton
            ),
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
                shape=ft.RoundedRectangleBorder(radius=25),
                elevation=10,
                title=ft.Text("¡Nueva versión disponible!", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_600),
                content=ft.Text(f"Tienes la versión {VERSION_APP} pero la {config['version_actual']} ya está lista.\n\nEs necesario actualizar para seguir jugando."),
                actions=[
                    ft.ElevatedButton(
                        "Descargar Actualización", 
                        icon=ft.Icons.DOWNLOAD,
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_500,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
                        on_click=lambda e: page.launch_url(config["enlace_descarga"]),
                        # -- ANIMACIÓN HOVER AQUÍ TAMBIÉN --
                        scale=1.0,
                        animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
                        on_hover=animar_hover_boton
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
