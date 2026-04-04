import flet as ft
import datetime

# Catálogo maestro: Le añadimos el concepto de "Rareza" a las insignias
CATALOGO_INSIGNIAS = {
    "fundador": {
        "nombre": "Presidente de Numo", 
        "icono": ft.Icons.VERIFIED, 
        "color": ft.Colors.BLUE_ACCENT_700, 
        "desc": "El mismísimo creador y desarrollador de la aplicación.",
        "rareza": "Mítica 👑"
    },
    "novato": {
        "nombre": "Primeros Pasos", 
        "icono": ft.Icons.DIRECTIONS_WALK, 
        "color": ft.Colors.GREEN_500, 
        "desc": "Ha comenzado su aventura matemática.",
        "rareza": "Común ⚪"
    },
    "matematico": {
        "nombre": "Mente Brillante", 
        "icono": ft.Icons.PSYCHOLOGY, 
        "color": ft.Colors.PURPLE_500, 
        "desc": "Completó la Sección 1 con honores.",
        "rareza": "Rara 🔵"
    },
    "ricachon": {
        "nombre": "Magnate", 
        "icono": ft.Icons.DIAMOND, 
        "color": ft.Colors.CYAN_400, 
        "desc": "Consiguió una fortuna de diamantes.",
        "rareza": "Épica 🟣"
    },
}

# ---> AHORA RECIBIMOS 'page' PARA PODER ABRIR LA TARJETA FLOTANTE <---
def crear_seccion_insignias(page: ft.Page, lista_ids_insignias):
    controles_insignias = []
    
    # Obtenemos la fecha de hoy para simular la fecha de obtención
    fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
    
    for id_insignia in lista_ids_insignias:
        if id_insignia in CATALOGO_INSIGNIAS:
            datos = CATALOGO_INSIGNIAS[id_insignia]
            es_fundador = (id_insignia == "fundador")
            
            # Usamos una función interna para atrapar correctamente los datos de CADA insignia
            def crear_evento_click(datos_insignia, es_fundador_flag):
                def al_clickear(e):
                    # Función para cerrar la tarjeta
                    def cerrar_tarjeta(e):
                        tarjeta_dialog.open = False
                        page.update()

                    # Diseñamos la tarjeta elegante que se abrirá
                    tarjeta_dialog = ft.AlertDialog(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        content_padding=0,
                        content=ft.Container(
                            width=300,
                            padding=30,
                            border_radius=20,
                            content=ft.Column([
                                # 1. Ícono grande arriba
                                ft.Container(
                                    content=ft.Icon(datos_insignia["icono"], size=60, color=ft.Colors.WHITE),
                                    bgcolor=datos_insignia["color"],
                                    width=100, height=100,
                                    shape=ft.BoxShape.CIRCLE,
                                    alignment=ft.Alignment.CENTER,
                                    border=ft.border.all(4, ft.Colors.AMBER_400) if es_fundador_flag else None,
                                    shadow=ft.BoxShadow(spread_radius=2, blur_radius=15, color=ft.Colors.AMBER_400) if es_fundador_flag else None,
                                ),
                                ft.Container(height=10),
                                # 2. Títulos y rareza
                                ft.Text(datos_insignia["nombre"], size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                ft.Text(datos_insignia["rareza"], size=14, color=ft.Colors.AMBER_600 if es_fundador_flag else ft.Colors.GREY_500, weight=ft.FontWeight.BOLD),
                                ft.Divider(height=20, color=ft.Colors.GREY_200),
                                # 3. Descripción
                                ft.Text(datos_insignia["desc"], size=16, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_700),
                                ft.Container(height=10),
                                # 4. Fecha de obtención
                                ft.Row([
                                    ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color=ft.Colors.GREY_400),
                                    ft.Text(f"Obtenida: {fecha_hoy}", size=12, color=ft.Colors.GREY_400, italic=True)
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Container(height=20),
                                # 5. Botón para cerrar
                                ft.ElevatedButton("¡Genial!", on_click=cerrar_tarjeta, bgcolor=datos_insignia["color"], color=ft.Colors.WHITE, width=150)
                            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        )
                    )
                    # Mostramos la tarjeta en la pantalla
                    page.overlay.append(tarjeta_dialog)
                    tarjeta_dialog.open = True
                    page.update()
                
                return al_clickear

            # Diseño visual de la insignia pequeña en el perfil
            insignia_ui = ft.Container(
                tooltip=f"{datos['nombre']}",
                content=ft.Container(
                    content=ft.Icon(datos["icono"], color=ft.Colors.WHITE, size=35 if es_fundador else 28),
                    bgcolor=datos["color"],
                    padding=15,
                    shape=ft.BoxShape.CIRCLE,
                    border=ft.border.all(3, ft.Colors.AMBER_400) if es_fundador else None,
                    shadow=ft.BoxShadow(spread_radius=2, blur_radius=10, color=ft.Colors.AMBER_400) if es_fundador else None,
                ),
                # ---> HACEMOS LA INSIGNIA CLICKEABLE <---
                on_click=crear_evento_click(datos, es_fundador),
                ink=True,          # Efecto visual al tocar
                border_radius=50,  # Que el toque sea circular
            )
            controles_insignias.append(insignia_ui)
    
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Insignias", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.PURPLE_700),
                ft.Icon(ft.Icons.MILITARY_TECH, color=ft.Colors.PURPLE_700)
            ]),
            ft.Row(controles_insignias, wrap=True, spacing=15) 
        ]),
        padding=ft.padding.only(left=20, right=20, top=10, bottom=10)
    )