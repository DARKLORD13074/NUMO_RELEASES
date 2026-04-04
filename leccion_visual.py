import flet as ft
import time
import random

def vista_leccion(page: ft.Page, nivel: int, vidas_actuales: int, on_completado, on_salir, on_perder_vida):
    # --- 1. BASE DE DATOS DE LA LECCIÓN ---
    es_teoria = False
    usa_emojis = False
    preguntas = []
    parrafos = []

    # NUEVA ESTRUCTURA: 12 Niveles (Teoría intercalada con Práctica)
    if nivel == 1:
        titulo_leccion = "El Concepto de Sumar"
        es_teoria = True
        parrafos = [
            "¡Hola! Bienvenido a tu primera lección teórica. Hoy hablaremos de la Suma.",
            "Sumar es simplemente juntar o agrupar cosas en un solo total. Imagina que tienes 2 manzanas y un amigo te regala 3 más.",
            "Al juntarlas todas, ahora tienes 5 manzanas. ¡Eso es sumar!",
            "En las matemáticas universales usamos el símbolo '+' para representar esta acción. ¡Vamos a practicarlo!"
        ]
    elif nivel == 2:
        titulo_leccion = "Sumas Básicas (Visuales)"
        instruccion = "¿Cuántos hay en total?"
        usa_emojis = True
        preguntas = [
            {"emoji": "🍎", "c1": 2, "c2": 3, "op": "+", "opciones": [4, 5, 6], "correcta": 5},
            {"emoji": "🍩", "c1": 4, "c2": 4, "op": "+", "opciones": [7, 8, 9], "correcta": 8},
            {"emoji": "🚀", "c1": 5, "c2": 2, "op": "+", "opciones": [6, 7, 8], "correcta": 7},
            {"emoji": "⭐", "c1": 6, "c2": 3, "op": "+", "opciones": [8, 9, 10], "correcta": 9},
        ]
    elif nivel == 3:
        titulo_leccion = "El Concepto de Restar"
        es_teoria = True
        parrafos = [
            "Ahora veamos la otra cara de la moneda: la Resta. Restar es quitar o separar elementos de un grupo.",
            "Si tienes 5 rebanadas de pizza y te comes 2, lógicamente te quedan 3. Eso es restar.",
            "Usamos el símbolo '-' para la resta. ¡Acompáñame al siguiente nivel para resolver unos ejercicios!"
        ]
    elif nivel == 4:
        titulo_leccion = "Restas Básicas (Visuales)"
        instruccion = "Si quitas, ¿cuántos quedan?"
        usa_emojis = True
        preguntas = [
            {"emoji": "🍕", "c1": 5, "c2": 2, "op": "-", "opciones": [2, 3, 4], "correcta": 3},
            {"emoji": "🎈", "c1": 8, "c2": 4, "op": "-", "opciones": [3, 4, 5], "correcta": 4},
            {"emoji": "🚗", "c1": 7, "c2": 5, "op": "-", "opciones": [1, 2, 3], "correcta": 2},
            {"emoji": "⚽", "c1": 9, "c2": 6, "op": "-", "opciones": [2, 3, 4], "correcta": 3},
        ]
    elif nivel == 5:
        titulo_leccion = "Sumas y Restas (Números)"
        instruccion = "Resuelve la operación abstracta:"
        preguntas = [
            {"eq": "15 + 7", "opciones": [21, 22, 23], "correcta": 22},
            {"eq": "24 - 9", "opciones": [13, 15, 17], "correcta": 15},
            {"eq": "32 + 18", "opciones": [40, 50, 60], "correcta": 50},
            {"eq": "45 - 27", "opciones": [16, 18, 20], "correcta": 18},
            {"eq": "100 - 43", "opciones": [57, 67, 47], "correcta": 57},
        ]
    elif nivel == 6:
        titulo_leccion = "El Concepto de Multiplicar"
        es_teoria = True
        parrafos = [
            "Sumar muchas veces lo mismo puede ser cansado. Imagina sumar 4 + 4 + 4 + 4 + 4... Para eso existe la Multiplicación.",
            "Multiplicar es una forma súper rápida de sumar el mismo número. Si tienes 3 bolsas y cada bolsa tiene 4 dulces, simplemente multiplicas 3 x 4 = 12.",
            "El símbolo clásico es 'x', aunque a veces verás un punto '·'. Es una herramienta muy poderosa."
        ]
    elif nivel == 7:
        titulo_leccion = "Multiplicación Básica"
        instruccion = "Encuentra el producto:"
        preguntas = [
            {"eq": "4 x 5", "opciones": [16, 20, 24], "correcta": 20},
            {"eq": "7 x 3", "opciones": [18, 21, 24], "correcta": 21},
            {"eq": "6 x 8", "opciones": [42, 48, 54], "correcta": 48},
            {"eq": "9 x 9", "opciones": [72, 81, 90], "correcta": 81},
            {"eq": "12 x 4", "opciones": [36, 48, 60], "correcta": 48},
        ]
    elif nivel == 8:
        titulo_leccion = "El Concepto de Dividir"
        es_teoria = True
        parrafos = [
            "Dividir es el arte de repartir cosas en partes exactamente iguales.",
            "Si tienes 10 galletas y quieres repartirlas entre 2 amigos de forma justa, a cada uno le tocan 5.",
            "La división es el opuesto de la multiplicación. Usamos el símbolo '÷' o a veces '/'. Vamos a practicar tu precisión."
        ]
    elif nivel == 9:
        titulo_leccion = "División Básica"
        instruccion = "Encuentra el cociente:"
        preguntas = [
            {"eq": "15 ÷ 3", "opciones": [4, 5, 6], "correcta": 5},
            {"eq": "24 ÷ 6", "opciones": [3, 4, 5], "correcta": 4},
            {"eq": "42 ÷ 7", "opciones": [6, 7, 8], "correcta": 6},
            {"eq": "64 ÷ 8", "opciones": [7, 8, 9], "correcta": 8},
            {"eq": "81 ÷ 9", "opciones": [8, 9, 10], "correcta": 9},
        ]
    elif nivel == 10:
        titulo_leccion = "Jerarquía (PEMDAS)"
        es_teoria = True
        parrafos = [
            "¿Qué pasa si tienes un problema largo como 3 + 4 x 2? Si sumas primero (3+4=7) y multiplicas por 2, da 14. Pero eso es INCORRECTO.",
            "Las matemáticas tienen leyes de tráfico para no chocar. A esto se le llama Jerarquía de Operaciones, conocida como PEMDAS.",
            "P: Paréntesis primero.\nE: Exponentes.\nM/D: Multiplicaciones y Divisiones (de izquierda a derecha).\nA/S: Adiciones y Sustracciones (sumas/restas al final).",
            "En '3 + 4 x 2', la Multiplicación gana. Primero hacemos 4 x 2 = 8, y luego le sumamos el 3. Resultado real: 11."
        ]
    elif nivel == 11:
        titulo_leccion = "Jerarquía de Operaciones"
        instruccion = "Resuelve respetando PEMDAS:"
        preguntas = [
            {"eq": "3 + 4 x 2", "opciones": [11, 14, 10], "correcta": 11}, 
            {"eq": "(5 + 3) x 2", "opciones": [11, 16, 13], "correcta": 16},
            {"eq": "10 - 6 ÷ 2", "opciones": [2, 7, 5], "correcta": 7},    
            {"eq": "4 x (8 - 3)", "opciones": [20, 29, 32], "correcta": 20},
            {"eq": "12 + 18 ÷ 3 - 2", "opciones": [8, 16, 14], "correcta": 16},
        ]
    elif nivel == 12:
        titulo_leccion = "🏆 EXAMEN FINAL 🏆"
        instruccion = "REPASO GENERAL: Resuelve con cuidado."
        preguntas_pool = [
            {"eq": "45 + 38", "opciones": [73, 83, 93], "correcta": 83},
            {"eq": "120 - 55", "opciones": [65, 75, 55], "correcta": 65},
            {"eq": "8 x 7", "opciones": [48, 56, 64], "correcta": 56},
            {"eq": "13 x 3", "opciones": [26, 39, 42], "correcta": 39},
            {"eq": "54 ÷ 6", "opciones": [8, 9, 7], "correcta": 9},
            {"eq": "96 ÷ 8", "opciones": [10, 12, 14], "correcta": 12},
            {"eq": "5 + 2 x (10 - 4)", "opciones": [42, 17, 24], "correcta": 17}, 
            {"eq": "20 ÷ 4 + 3", "opciones": [2, 8, 5], "correcta": 8},
            {"eq": "(8 + 4) ÷ 2", "opciones": [6, 10, 8], "correcta": 6},
            {"eq": "3 x 3 x 3", "opciones": [9, 27, 81], "correcta": 27},
        ]
        if len(preguntas_pool) > 8:
            preguntas = random.sample(preguntas_pool, 8) 
        else:
            preguntas = preguntas_pool
    else:
        titulo_leccion = f"Nivel {nivel}"
        instruccion = "Resuelve:"
        preguntas = [{"eq": "1 + 1", "opciones": [1, 2, 3], "correcta": 2}]

    # ---> BUG FIX: Mezclamos las opciones una sola vez al cargar la lección <---
    if not es_teoria:
        for p in preguntas:
            random.shuffle(p["opciones"])
    
    # --- 2. ESTADO DE LA LECCIÓN ---
    # Si es teoría, avanzamos por párrafos. Si es práctica, por preguntas.
    estado = {
        "paso_actual": 0, 
        "total_pasos": len(parrafos) if es_teoria else len(preguntas),
        "vidas": vidas_actuales,
        "tiempo_inicio": time.time()
    }

    # --- 3. ELEMENTOS DE LA INTERFAZ ---
    barra_progreso = ft.ProgressBar(value=0, color=ft.Colors.GREEN_500 if not es_teoria else ft.Colors.CYAN_500, bgcolor=ft.Colors.GREY_200, height=15, border_radius=10, expand=True)
    texto_vidas = ft.Text(str(estado["vidas"]) if not es_teoria else "∞", color=ft.Colors.RED_500 if not es_teoria else ft.Colors.GREY_400, weight=ft.FontWeight.BOLD, size=18)
    
    zona_visual = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=10, wrap=True)
    zona_opciones = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    texto_instruccion = ft.Text(size=16, color=ft.Colors.GREY_500)

    # --- 4. LÓGICA DEL JUEGO ---
    def cargar_paso():
        if estado["paso_actual"] >= estado["total_pasos"]:
            mostrar_pantalla_victoria()
            return

        zona_visual.controls.clear()
        zona_opciones.controls.clear()
        
        # LOGICA PARA LECCIONES DE TEORÍA
        if es_teoria:
            texto_instruccion.value = "Lee con atención:"
            
            # Mostramos el texto como párrafos que van apareciendo
            col_parrafos = ft.Column(spacing=20)
            for i in range(estado["paso_actual"] + 1):
                es_el_ultimo = (i == estado["paso_actual"])
                col_parrafos.controls.append(
                    ft.Text(
                        parrafos[i], 
                        size=18, 
                        color=ft.Colors.BLUE_900 if es_el_ultimo else ft.Colors.GREY_600, 
                        weight=ft.FontWeight.BOLD if es_el_ultimo else ft.FontWeight.NORMAL, 
                        text_align=ft.TextAlign.CENTER
                    )
                )
            zona_visual.controls.append(col_parrafos)
            
            # Botón para revelar el siguiente párrafo o terminar
            btn_continuar = ft.ElevatedButton(
                "Siguiente" if estado["paso_actual"] < estado["total_pasos"] - 1 else "¡Entendido!",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=15),
                    padding=ft.padding.symmetric(horizontal=40, vertical=20),
                    bgcolor=ft.Colors.CYAN_600,
                    color=ft.Colors.WHITE,
                ),
                on_click=lambda e: avanzar_teoria()
            )
            zona_opciones.controls.append(btn_continuar)

        # LOGICA PARA LECCIONES DE PRÁCTICA (Examen y Ejercicios)
        else:
            texto_instruccion.value = instruccion
            p = preguntas[estado["paso_actual"]]
            
            if usa_emojis:
                for _ in range(p["c1"]):
                    zona_visual.controls.append(ft.Text(p["emoji"], size=40))
                zona_visual.controls.append(ft.Text(p["op"], size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700))
                for _ in range(p["c2"]):
                    zona_visual.controls.append(ft.Text(p["emoji"], size=40))
                zona_visual.controls.append(ft.Text("=", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700))
                zona_visual.controls.append(ft.Text("?", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_500))
            else:
                zona_visual.controls.append(ft.Text(p["eq"] + " = ?", size=50, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800))

            for opcion in p["opciones"]:
                btn = ft.ElevatedButton(
                    content=ft.Text(str(opcion), size=24, weight=ft.FontWeight.BOLD),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        padding=ft.padding.symmetric(horizontal=30, vertical=20),
                        bgcolor=ft.Colors.WHITE, color=ft.Colors.BLUE_600, elevation=3, side=ft.BorderSide(2, ft.Colors.BLUE_200)
                    ),
                    on_click=verificar_respuesta(opcion, p["correcta"])
                )
                zona_opciones.controls.append(btn)
        
        barra_progreso.value = estado["paso_actual"] / estado["total_pasos"]
        page.update()

    def avanzar_teoria():
        estado["paso_actual"] += 1
        cargar_paso()

    def verificar_respuesta(opcion_elegida, correcta):
        def handler(e):
            if opcion_elegida == correcta:
                snack_correcto = ft.SnackBar(content=ft.Text("¡Excelente! 🎉"), bgcolor=ft.Colors.GREEN_500, duration=1500)
                page.overlay.append(snack_correcto)
                snack_correcto.open = True
                estado["paso_actual"] += 1
                cargar_paso()
            else:
                estado["vidas"] -= 1
                texto_vidas.value = str(estado["vidas"])
                on_perder_vida()
                snack_incorrecto = ft.SnackBar(content=ft.Text("Casi... Intenta de nuevo 😅"), bgcolor=ft.Colors.RED_500, duration=1500)
                page.overlay.append(snack_incorrecto)
                snack_incorrecto.open = True
                
                if estado["vidas"] <= 0:
                    mostrar_pantalla_derrota()
            page.update()
        return handler

    # --- 5. PANTALLAS DE FIN ---
    def mostrar_pantalla_victoria():
        tiempo_fin = time.time()
        segundos_totales = int(tiempo_fin - estado["tiempo_inicio"])
        minutos = segundos_totales // 60
        segundos = segundos_totales % 60
        texto_tiempo = f"{minutos}m {segundos}s" if minutos > 0 else f"{segundos}s"

        es_examen = (nivel == 12)
        
        # Lógica de experiencia y mensajes dependiendo del tipo de lección
        if es_teoria:
            xp_total = 5  # XP Fija reducida para teorías
            titulo_fin = "¡Teoría Completada!"
            mensaje_velocidad = "¡Conocimiento adquirido! 🧠"
            color_mensaje = ft.Colors.CYAN_600
            texto_tiempo = "--" # El tiempo no importa en la teoría
            icono_final = ft.Icons.MENU_BOOK
            color_icono_final = ft.Colors.CYAN_500
        else:
            promedio_segundos = segundos_totales / estado["total_pasos"] if estado["total_pasos"] > 0 else 0
            xp_base = 50 if es_examen else 10
            
            if promedio_segundos <= 5:
                mensaje_velocidad = "¡Velocidad a nivel cuántico! ⚡"
                xp_extra = 15
                color_mensaje = ft.Colors.PURPLE_500
            elif promedio_segundos <= 10:
                mensaje_velocidad = "¡Súper rápido y preciso! 🚀"
                xp_extra = 10
                color_mensaje = ft.Colors.BLUE_500
            elif promedio_segundos <= 20:
                mensaje_velocidad = "Buen ritmo, constante. 🏃‍♂️"
                xp_extra = 5
                color_mensaje = ft.Colors.GREEN_600
            else:
                mensaje_velocidad = "Paso a paso, construyendo bases sólidas. 🐢"
                xp_extra = 0
                color_mensaje = ft.Colors.ORANGE_600

            if es_examen: xp_extra *= 2
            xp_total = xp_base + xp_extra
            titulo_fin = "¡EXAMEN COMPLETADO! 🏆" if es_examen else "¡Lección Completada! 🎉"
            icono_final = ft.Icons.EMOJI_EVENTS if es_examen else ft.Icons.STARS
            color_icono_final = ft.Colors.AMBER_400

        contenedor_principal.content = ft.Column(
            controls=[
                ft.Icon(icono_final, color=color_icono_final, size=80),
                ft.Text(titulo_fin, size=26, weight=ft.FontWeight.BOLD, color=color_icono_final, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column([
                        ft.Text("📊 ESTADÍSTICAS", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        ft.Divider(color=ft.Colors.GREY_300),
                        ft.Row([
                            ft.Icon(ft.Icons.TIMER, color=ft.Colors.BLUE_500, size=24),
                            ft.Text(f"Tiempo: {texto_tiempo}", size=18, weight=ft.FontWeight.W_500),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(mensaje_velocidad, size=14, color=color_mensaje, italic=True),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Icon(ft.Icons.BOLT, color=ft.Colors.AMBER_500, size=28),
                            ft.Text(f"+{xp_total} XP", size=24, color=ft.Colors.AMBER_500, weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.BLUE_GREY_50, padding=20, border_radius=15, width=300
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Continuar", bgcolor=ft.Colors.GREEN_500, color=ft.Colors.WHITE, 
                    style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=40, vertical=15)),
                    on_click=lambda e: on_completado(nivel, xp_total)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        )
        page.update()

    def mostrar_pantalla_derrota():
        contenedor_principal.content = ft.Column(
            [
                ft.Icon(ft.Icons.HEART_BROKEN, color=ft.Colors.RED_500, size=100),
                ft.Text("Te quedaste sin vidas", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
                ft.ElevatedButton("Salir", bgcolor=ft.Colors.GREY_300, color=ft.Colors.BLACK, on_click=lambda e: on_salir())
            ],
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        )
        page.update()

    # --- 6. CONSTRUCCIÓN DE LA VISTA COMPLETA ---
    cabecera = ft.Row(
        [
            ft.IconButton(ft.Icons.CLOSE, icon_color=ft.Colors.GREY_500, on_click=lambda e: on_salir()),
            barra_progreso,
            ft.Row([ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_500 if not es_teoria else ft.Colors.GREY_400), texto_vidas], spacing=2)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    contenedor_principal = ft.Container(
        content=ft.Column(
            [
                cabecera,
                ft.Container(height=20),
                ft.Text(titulo_leccion, size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                texto_instruccion,
                ft.Container(height=40),
                zona_visual,
                ft.Container(expand=True), 
                zona_opciones,
                ft.Container(height=40),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        ),
        padding=20, expand=True, bgcolor=ft.Colors.WHITE
    )

    cargar_paso()
    return contenedor_principal