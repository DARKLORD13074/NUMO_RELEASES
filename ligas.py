import flet as ft
from database import obtener_leaderboard
from insignias import CATALOGO_INSIGNIAS # <-- 1. Importamos el catálogo de insignias

# <-- 2. Añadimos on_ver_perfil como parámetro
def vista_ligas(page: ft.Page, id_usuario_actual: int, on_ver_perfil): 
    jugadores = obtener_leaderboard()
    lista_clasificacion = ft.ListView(spacing=5, padding=15, expand=True)

    encabezado = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.EMOJI_EVENTS, size=70, color=ft.Colors.AMBER_500),
            ft.Text("Liga Oro", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_600),
            ft.Text("Los mejores de la semana", color=ft.Colors.GREY_500, size=14)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.Alignment.CENTER, padding=ft.padding.only(bottom=20, top=10)
    )
    lista_clasificacion.controls.append(encabezado)

    def abrir_mini_perfil(e, jugador):
        insignias_str = jugador.get("insignias", "novato")
        insignias_lista = insignias_str.split(",") if insignias_str else ["novato"]
        
        controles_insignias = []
        for ins in insignias_lista:
            if ins in CATALOGO_INSIGNIAS:
                datos = CATALOGO_INSIGNIAS[ins]
                es_fundador = (ins == "fundador")
                icono_ui = ft.Container(
                    content=ft.Icon(datos["icono"], color=ft.Colors.WHITE, size=20),
                    bgcolor=datos["color"],
                    padding=8,
                    shape=ft.BoxShape.CIRCLE,
                    border=ft.border.all(2, ft.Colors.AMBER_400) if es_fundador else None,
                    tooltip=datos["nombre"]
                )
                controles_insignias.append(icono_ui)
                
        fila_insignias = ft.Row(controles_insignias, alignment=ft.MainAxisAlignment.CENTER, wrap=True)

        icono_nombre = jugador.get("avatar_icono", "ACCOUNT_CIRCLE")
        icono_color = jugador.get("avatar_color", "blue")

        # Bandera para saber si cerramos el modal a propósito con el botón
        ir_al_perfil = [False] 

        def accion_ver_perfil(e):
            ir_al_perfil[0] = True # Activamos la bandera
            if hasattr(page, 'close'):
                page.close(mini_perfil)
            else:
                mini_perfil.open = False
                page.update()
                if mini_perfil in page.overlay:
                    page.overlay.remove(mini_perfil)
        
        # Esta función asegura que primero termine la animación de cierre y LUEGO viajemos
        def al_cerrar_modal(e):
            if ir_al_perfil[0]:
                on_ver_perfil(jugador)

        mini_perfil = ft.BottomSheet(
            ft.Container(
                padding=30,
                content=ft.Column(
                    [
                        ft.Icon(getattr(ft.Icons, icono_nombre, ft.Icons.ACCOUNT_CIRCLE), size=80, color=icono_color),
                        ft.Text(jugador["usuario"], size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{jugador['xp_total']} XP", color=ft.Colors.AMBER_500, weight=ft.FontWeight.BOLD, size=18),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Text("Insignias", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.GREY_500),
                        fila_insignias,
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Ver perfil completo", 
                            icon=ft.Icons.PERSON_SEARCH,
                            # SOLUCIÓN 1: Diccionario de MaterialState para recuperar el área táctil visual
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.BLUE_500,
                                    ft.ControlState.HOVERED: ft.Colors.BLUE_600,
                                },
                                color=ft.Colors.WHITE, 
                                padding=15
                            ),
                            width=280, 
                            on_click=accion_ver_perfil 
                        )
                    ],
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            # SOLUCIÓN 2: Ejecutar navegación limpiamente al terminar de cerrarse
            on_dismiss=al_cerrar_modal 
        )
        
        if hasattr(page, 'open'):
            page.open(mini_perfil)
        else:
            page.overlay.append(mini_perfil)
            mini_perfil.open = True
            page.update()

    # Generar las filas de la tabla de clasificación
    for index, jugador in enumerate(jugadores):
        rango = index + 1
        es_usuario_actual = jugador["id"] == id_usuario_actual

        # Colores para el Top 3
        color_rango = ft.Colors.GREY_400
        peso_fuente_rango = ft.FontWeight.NORMAL
        if rango == 1: 
            color_rango = ft.Colors.AMBER_500
            peso_fuente_rango = ft.FontWeight.BOLD
        elif rango == 2: 
            color_rango = ft.Colors.BLUE_GREY_400
            peso_fuente_rango = ft.FontWeight.BOLD
        elif rango == 3: 
            color_rango = ft.Colors.BROWN_400
            peso_fuente_rango = ft.FontWeight.BOLD

        icono_jugador = getattr(ft.Icons, jugador.get("avatar_icono", "ACCOUNT_CIRCLE"), ft.Icons.ACCOUNT_CIRCLE)
        color_icono = jugador.get("avatar_color", "blue")

        fila = ft.Container(
            content=ft.Row([
                ft.Text(str(rango), size=18, weight=peso_fuente_rango, color=color_rango, width=25, text_align=ft.TextAlign.CENTER),
                ft.CircleAvatar(content=ft.Icon(icono_jugador, color=ft.Colors.WHITE, size=20), bgcolor=color_icono, radius=20),
                ft.Text(jugador["usuario"], size=16, weight=ft.FontWeight.BOLD if es_usuario_actual else ft.FontWeight.NORMAL, expand=True),
                ft.Text(f"{jugador['xp_total']} XP", size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_600)
            ]),
            padding=ft.padding.symmetric(horizontal=10, vertical=12),
            border_radius=12,
            bgcolor=ft.Colors.BLUE_50 if es_usuario_actual else ft.Colors.TRANSPARENT,
            border=ft.border.all(2, ft.Colors.BLUE_200) if es_usuario_actual else None,
            ink=True,
            on_click=lambda e, j=jugador: abrir_mini_perfil(e, j)
        )
        lista_clasificacion.controls.append(fila)
        
        # Separador visual entre usuarios
        if index < len(jugadores) - 1:
            lista_clasificacion.controls.append(ft.Divider(height=1, color=ft.Colors.GREY_200))

    return ft.Container(content=lista_clasificacion, expand=True)