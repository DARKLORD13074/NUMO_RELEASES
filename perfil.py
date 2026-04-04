import flet as ft
from insignias import crear_seccion_insignias

def vista_perfil(page: ft.Page, usuario, descripcion, xp_total, insignias, racha_total, niveles_total, avatar_icono, avatar_color, on_guardar_perfil, on_cerrar_sesion=None, es_perfil_propio=True):
    
    # --- REFERENCIAS PARA CONTROLES DINÁMICOS ---
    # Usamos referencias para cambiar el contenido de los contenedores
    contenedor_nombre_ref = ft.Ref[ft.Container]()
    contenedor_descripcion_ref = ft.Ref[ft.Container]()
    
    # Referencias para las entradas de texto (modo edición)
    nombre_edit_ref = ft.Ref[ft.TextField]()
    descripcion_edit_ref = ft.Ref[ft.TextField]()

    # Referencias para el botón y el avatar para actualizar su color/ícono
    boton_editar_ref = ft.Ref[ft.ElevatedButton]()
    avatar_icono_ref = ft.Ref[ft.Icon]()
    avatar_fondo_ref = ft.Ref[ft.Container]()

    # --- DATOS TEMPORALES DE EDICIÓN DEL AVATAR ---
    # Guardamos localmente las selecciones mientras editamos
    nuevo_avatar_data = {
        "icono": avatar_icono,
        "color": avatar_color
    }

    # --- FUNCIONES DE CONTROL DE EDICIÓN ---
    def alternar_modo_edicion(e):
        boton = boton_editar_ref.current
        
        if boton.data == "modo_vista":
            # ---> ENTRAR EN MODO EDICIÓN <---
            boton.data = "modo_edicion" # Cambiamos el estado
            boton.content.value = "Guardar Cambios" # Cambiamos el texto
            boton.icon = ft.Icons.SAVE
            boton.bgcolor = ft.Colors.GREEN_500
            
            # 1. Cambiamos el nombre por un cuadro de entrada
            contenedor_nombre_ref.current.content = ft.TextField(
                value=usuario,
                ref=nombre_edit_ref,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.PURPLE_600,
                border_radius=10,
                content_padding=ft.padding.symmetric(horizontal=15),
                border=ft.border.all(1, ft.Colors.PURPLE_200),
                label="Nombre de Usuario",
                label_style=ft.TextStyle(color=ft.Colors.WHITE70),
            )
            
            # 2. Cambiamos la descripción por un cuadro de entrada
            contenedor_descripcion_ref.current.content = ft.TextField(
                value=descripcion,
                ref=descripcion_edit_ref,
                multiline=True,
                min_lines=3,
                max_lines=5,
                color=ft.Colors.GREY_800,
                border_radius=15,
                border=ft.border.all(1, ft.Colors.GREY_300),
                label="Tu descripción",
            )
            
            # 3. Activamos el clic en el avatar para cambiarlo
            avatar_fondo_ref.current.on_click = abrir_selector_avatar
            avatar_fondo_ref.current.ink = True
            
        else:
            # ---> GUARDAR CAMBIOS Y SALIR <---
            
            # 1. Obtenemos los nuevos valores
            nuevo_nombre = nombre_edit_ref.current.value.strip()
            nueva_descripcion = descripcion_edit_ref.current.value.strip()
            
            # Validación básica
            if not nuevo_nombre:
                page.snack_bar = ft.SnackBar(content=ft.Text("El nombre no puede estar vacío"), bgcolor=ft.Colors.RED_500)
                page.snack_bar.open = True
                page.update()
                return

            # 2. Llamamos a main.py para guardar permanentemente
            on_guardar_perfil(
                nuevo_nombre, 
                nueva_descripcion, 
                nuevo_avatar_data["icono"], 
                nuevo_avatar_data["color"]
            )
            
            # 3. Restauramos el botón a su estado original
            boton.data = "modo_vista" # Restauramos el estado
            boton.content.value = "Editar Perfil" # Restauramos el texto
            boton.icon = ft.Icons.EDIT
            boton.bgcolor = ft.Colors.PURPLE_500
            
            # 4. Restauramos el texto original (ahora actualizado)
            contenedor_nombre_ref.current.content = ft.Text(
                nuevo_nombre,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=22,
                text_align=ft.TextAlign.CENTER,
            )
            
            contenedor_descripcion_ref.current.content = ft.Text(
                nueva_descripcion,
                color=ft.Colors.GREY_800,
                size=14,
                no_wrap=False,
                max_lines=10, 
            )
            
            # 5. Desactivamos el clic en el avatar
            avatar_fondo_ref.current.on_click = None
            avatar_fondo_ref.current.ink = False

        page.update()

    # --- DIÁLOGO DE SELECCIÓN DE AVATAR ---
    # Una ventana simple para elegir ícono y color
    def abrir_selector_avatar(e):
        
        # Opciones disponibles
        iconos = [ft.Icons.ACCOUNT_CIRCLE, ft.Icons.FACE, ft.Icons.STAR_PURPLE500, ft.Icons.CALCULATE]
        colores = [ft.Colors.BLUE, ft.Colors.RED, ft.Colors.GREEN, ft.Colors.PURPLE, ft.Colors.ORANGE]
        
        # Creamos una referencia para el avatar de vista previa dentro del diálogo
        avatar_previa_dialogo_ref = ft.Ref[ft.Container]()
        icon_previa_dialogo_ref = ft.Ref[ft.Icon]()

        # Función para aplicar el cambio solo a la previsualización del diálogo y de la vista
        def seleccionar(tipo, valor):
            nuevo_avatar_data[tipo] = valor # Actualizamos los datos temporales
            
            # Actualizamos la previsualización en el diálogo
            icon_previa_dialogo_ref.current.name = nuevo_avatar_data["icono"]
            avatar_previa_dialogo_ref.current.bgcolor = nuevo_avatar_data["color"]
            
            # Actualizamos la previsualización en la vista de perfil detrás
            avatar_icono_ref.current.name = nuevo_avatar_data["icono"]
            avatar_fondo_ref.current.bgcolor = nuevo_avatar_data["color"]
            
            page.update()

        # Cuadrícula de iconos
        iconos_row = ft.Row([
            ft.IconButton(
                icon=ico, 
                icon_color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREY_600,
                on_click=lambda e, i=ico: seleccionar("icono", i)
            ) for ico in iconos
        ], wrap=True)
        
        # Cuadrícula de colores
        colores_row = ft.Row([
            ft.Container(
                width=30, height=30, bgcolor=col, border_radius=5,
                on_click=lambda e, c=col: seleccionar("color", c)
            ) for col in colores
        ], wrap=True)

        def cerrar_dialogo(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Elige tu Avatar", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Vista previa:", size=12, color=ft.Colors.GREY_600),
                # Avatar de vista previa
                ft.Row([ft.Container(
                    content=ft.Icon(nuevo_avatar_data["icono"], size=40, color=ft.Colors.WHITE, ref=icon_previa_dialogo_ref),
                    width=70, height=70, bgcolor=nuevo_avatar_data["color"], shape=ft.BoxShape.CIRCLE,
                    ref=avatar_previa_dialogo_ref
                )], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20),
                ft.Text("Íconos:", size=12),
                iconos_row,
                ft.Text("Colores:", size=12),
                colores_row
            ], spacing=10, height=280, width=280),
            actions=[ft.TextButton("Hecho", on_click=cerrar_dialogo)],
        )
        
        if dialog not in page.overlay:
            page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # --- CONSTRUCCIÓN DE LA VISTA (LAYOUT) ---
    
    # Header del Perfil (Parte morada)
    header_perfil = ft.Container(
        content=ft.Column([
            ft.Row([
                # Avatar (Clickable solo en modo edición)
                ft.Container(
                    content=ft.Icon(avatar_icono, size=50, color=ft.Colors.WHITE, ref=avatar_icono_ref),
                    width=90, height=90, bgcolor=avatar_color, shape=ft.BoxShape.CIRCLE,
                    ref=avatar_fondo_ref # Lo necesitamosclickable
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            # Nombre del Usuario (Referenciado para cambiarlo)
            ft.Container(
                content=ft.Text(
                    usuario,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=22,
                    text_align=ft.TextAlign.CENTER,
                ),
                ref=contenedor_nombre_ref, # Ponemos la referencia aquí
                alignment=ft.Alignment.CENTER,
            ),
        ], spacing=10),
        bgcolor=ft.Colors.PURPLE_500,
        padding=ft.padding.only(top=30, bottom=20, left=20, right=20),
        border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
    )

    # Botón de Editar Perfil
    boton_editar = ft.Container(
        content=ft.Row([
            ft.ElevatedButton(
                content=ft.Text("Editar Perfil", weight=ft.FontWeight.BOLD), # Usamos content explícito
                icon=ft.Icons.EDIT,
                color=ft.Colors.WHITE, 
                bgcolor=ft.Colors.PURPLE_500,
                on_click=alternar_modo_edicion,
                style=ft.ButtonStyle(elevation=2, padding=10),
                ref=boton_editar_ref,
                data="modo_vista" # <--- NUEVO: Usamos data para controlar el estado
            )
        ], alignment=ft.MainAxisAlignment.END),
        padding=ft.padding.only(right=15)
    )

    # Tarjeta de Descripción (Referenciada para cambiarla)
    tarjeta_descripcion = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Sobre Mí", weight=ft.FontWeight.BOLD, size=16),
                ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.PURPLE_300),
            ]),
            ft.Container(
                content=ft.Text(
                    descripcion,
                    color=ft.Colors.GREY_800,
                    size=14,
                    no_wrap=False, # Permite saltos de línea
                    max_lines=10, # Máximo número de líneas a mostrar
                ),
                ref=contenedor_descripcion_ref, # Ponemos la referencia aquí
            ),
        ]),
        bgcolor=ft.Colors.WHITE,
        padding=20,
        margin=ft.margin.only(left=15, right=15, top=10, bottom=10),
        border_radius=15,
        border=ft.border.all(1, ft.Colors.GREY_100),
    )

    # --- RESTO DEL CÓDIGO (SECCIÓN DE ESTADÍSTICAS) SE QUEDA IGUAL ---
    
    # Sección de Estadísticas
    titulo_estadisticas = ft.Container(
        content=ft.Row([
            ft.Text("Tus Estadísticas", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.PURPLE_700),
            ft.Icon(ft.Icons.BAR_CHART_ROUNDED, color=ft.Colors.PURPLE_700)
        ]),
        padding=ft.padding.only(left=20, top=10) # El padding ahora está en el Container
    )

    def crear_tarjeta_estadistica(icono, color, valor, titulo):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, color=ft.Colors.WHITE, size=28),
                ft.Text(str(valor), color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=22),
                ft.Text(titulo, color=ft.Colors.WHITE70, size=11),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
            bgcolor=color,
            width=100,
            height=100,
            border_radius=15,
            padding=10,
            margin=5
        )

    grid_estadisticas = ft.Container(
        content=ft.Row([
            crear_tarjeta_estadistica(ft.Icons.STAR_PURPLE500, ft.Colors.ORANGE_500, xp_total, "XP Total"),
            crear_tarjeta_estadistica(ft.Icons.LOCAL_FIRE_DEPARTMENT, ft.Colors.RED_500, racha_total, "Días Racha"),
            crear_tarjeta_estadistica(ft.Icons.SCHOOL, ft.Colors.BLUE_500, niveles_total, "Niveles"),
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER),
        padding=10
    )

    seccion_practica = ft.Container(
        content=ft.ElevatedButton(
            "Ver Práctica Diaria",
            icon=ft.Icons.FITNESS_CENTER, # <--- ICONO CORREGIDO (Pesa de gimnasio / Entrenamiento)
            bgcolor=ft.Colors.LIGHT_GREEN_500,
            color=ft.Colors.WHITE,
            width=float('inf'), # Ancho completo
            on_click=lambda e: print("Navegando a Práctica")
        ),
        padding=20,
    )

    seccion_insignias_ui = crear_seccion_insignias(page,insignias)

    boton_cerrar_sesion = ft.Container(
        content=ft.OutlinedButton(
            "Cerrar Sesión",
            icon=ft.Icons.LOGOUT,
            icon_color=ft.Colors.RED_500,
            style=ft.ButtonStyle(color=ft.Colors.RED_500),
            on_click=on_cerrar_sesion,
            width=float('inf') # Para que ocupe todo el ancho
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10)
    )

    # --- CONSTRUCCIÓN FINAL DE LA VISTA ---
    # Armamos la lista de elementos básicos que TODOS los perfiles tienen
    controles_perfil = [
        header_perfil,
    ]

    # Si el perfil es TUYO, agregamos el botón de editar justo debajo del header
    if es_perfil_propio:
        controles_perfil.append(boton_editar)

    # Agregamos los elementos comunes
    controles_perfil.append(tarjeta_descripcion)
    controles_perfil.append(seccion_insignias_ui)
    controles_perfil.append(titulo_estadisticas)
    controles_perfil.append(grid_estadisticas)

    # Si el perfil es TUYO, agregamos el botón de práctica diaria
    if es_perfil_propio:
        controles_perfil.append(seccion_practica)

    if es_perfil_propio and on_cerrar_sesion:
        controles_perfil.append(boton_cerrar_sesion)

    # Siempre agregamos el espacio final para la barra inferior
    controles_perfil.append(ft.Container(height=50))

    # Retornamos la columna con los elementos seleccionados
    return ft.Column(controles_perfil, scroll=ft.ScrollMode.HIDDEN)

