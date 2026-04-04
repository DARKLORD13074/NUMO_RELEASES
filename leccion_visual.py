import flet as ft
import time
import random
import asyncio

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
    elif nivel == 13:
        titulo_leccion = "El Mundo Subterráneo (Negativos)"
        es_teoria = True
        parrafos = [
            "¡Bienvenido a la Sección 2! Hasta ahora hemos contado cosas que existen, pero ¿qué pasa cuando debes algo?",
            "Imagina que tienes $0, pero le pides prestado $5 a un amigo. Ahora tienes '-5' dólares. ¡Ese es un número negativo!",
            "En un edificio, el lobby es el piso 0. Si bajas al sótano, estás en el piso -1. Los negativos representan ausencias, deudas o lo que está 'debajo' de cero."
        ]
    elif nivel == 14:
        titulo_leccion = "Suma y Resta (Negativos)"
        instruccion = "Calcula tu saldo:"
        preguntas = [
            {"eq": "-5 + 3", "opciones": [-2, 2, -8], "correcta": -2},
            {"eq": "4 - 7", "opciones": [-3, 3, 11], "correcta": -3},
            {"eq": "-2 - 4", "opciones": [2, -6, -2], "correcta": -6},
            {"eq": "-10 + 15", "opciones": [-5, 5, 25], "correcta": 5},
            {"eq": "0 - 8", "opciones": [0, -8, 8], "correcta": -8},
        ]
    elif nivel == 15:
        titulo_leccion = "Los Enemigos de mis Amigos"
        es_teoria = True
        parrafos = [
            "Para multiplicar o dividir números con signos (+ y -), existen reglas universales llamadas 'La Ley de los Signos'.",
            "Regla 1: Si los signos son IGUALES, el resultado siempre es positivo (+).\n• Positivo x Positivo = Positivo\n• Negativo x Negativo = Positivo (¡Los enemigos de tus enemigos son tus amigos!)",
            "Regla 2: Si los signos son DIFERENTES, chocan y el negativo siempre gana (-).\n• Positivo x Negativo = Negativo.",
            "Recuerda: Estas reglas solo aplican para multiplicar (x) y dividir (÷), ¡no te confundas al sumar y restar!"
        ]
    elif nivel == 16:
        titulo_leccion = "Práctica: Ley de Signos"
        instruccion = "Multiplica y divide con cuidado:"
        preguntas = [
            {"eq": "(-3) x (-4)", "opciones": [12, -12, -7], "correcta": 12},
            {"eq": "5 x (-2)", "opciones": [-10, 10, -7], "correcta": -10},
            {"eq": "(-15) ÷ 3", "opciones": [5, -5, -12], "correcta": -5},
            {"eq": "(-20) ÷ (-4)", "opciones": [-5, 5, -24], "correcta": 5},
            {"eq": "(-6) x 2", "opciones": [-12, 12, 8], "correcta": -12},
        ]
    elif nivel == 17:
        titulo_leccion = "Partiendo el Pastel (Fracciones)"
        es_teoria = True
        parrafos = [
            "A veces no tenemos un objeto completo. Si partimos una pizza en 4 pedazos iguales y tomas 1, tienes '1/4' de pizza.",
            "El número de abajo (Denominador) dice en cuántas partes se cortó. El de arriba (Numerador) dice cuántas partes tomaste.",
            "Si tienes 2/2, ¡tienes la pizza completa! Las fracciones son solo una forma de representar partes de un todo."
        ]
    elif nivel == 18:
        titulo_leccion = "Entendiendo Fracciones"
        instruccion = "Resuelve estas operaciones (Misma base):"
        preguntas = [
            {"eq": "1/4 + 2/4", "opciones": ["3/4", "3/8", "1/2"], "correcta": "3/4"},
            {"eq": "5/8 - 2/8", "opciones": ["3/8", "3/0", "7/8"], "correcta": "3/8"},
            {"eq": "1/3 + 1/3", "opciones": ["2/6", "2/3", "1"], "correcta": "2/3"},
            {"eq": "4/5 - 1/5", "opciones": ["3/5", "5/5", "3/0"], "correcta": "3/5"},
            {"eq": "1/2 + 1/2", "opciones": ["1/4", "2/4", "1 (Entero)"], "correcta": "1 (Entero)"},
        ]
    elif nivel == 19:
        titulo_leccion = "Puntos y Comas (Decimales)"
        es_teoria = True
        parrafos = [
            "Los decimales son primos hermanos de las fracciones. Son otra forma de escribir 'un pedazo' de algo.",
            "Nuestro sistema se basa en el 10. Si partes 1 peso en 10 monedas, cada moneda es 0.10 (un décimo).",
            "Por lo tanto, 1/2 es exactamente lo mismo que 0.5 (la mitad de uno). El punto decimal separa lo entero de lo incompleto."
        ]
    elif nivel == 20:
        titulo_leccion = "Operando Decimales"
        instruccion = "Suma y resta con punto decimal:"
        preguntas = [
            {"eq": "1.5 + 2.5", "opciones": [3.0, 4.0, 3.5], "correcta": 4.0},
            {"eq": "5.0 - 2.5", "opciones": [2.5, 3.5, 2.0], "correcta": 2.5},
            {"eq": "0.5 + 0.1", "opciones": [0.6, 0.51, 1.5], "correcta": 0.6},
            {"eq": "10.5 - 0.5", "opciones": [10.0, 9.5, 11.0], "correcta": 10.0},
            {"eq": "2.2 + 3.3", "opciones": [5.0, 5.5, 6.5], "correcta": 5.5},
        ]
    elif nivel == 21:
        titulo_leccion = "El famoso Porcentaje (%)"
        es_teoria = True
        parrafos = [
            "La palabra porcentaje significa literalmente 'por cada 100'.",
            "Si decimos que el 50% de la gente ama los gatos, significa que 50 de cada 100 personas los aman. (¡Es decir, la mitad!)",
            "Porcentajes, fracciones y decimales son el mismo concepto con diferente traje: 50% = 1/2 = 0.5. Conocer esto te dará superpoderes."
        ]
    elif nivel == 22:
        titulo_leccion = "Cálculo de Porcentajes"
        instruccion = "Encuentra el porcentaje:"
        preguntas = [
            {"eq": "50% de 20", "opciones": [10, 5, 15], "correcta": 10},
            {"eq": "10% de 100", "opciones": [1, 10, 50], "correcta": 10},
            {"eq": "25% de 40", "opciones": [10, 20, 15], "correcta": 10},
            {"eq": "100% de 85", "opciones": [0, 85, 100], "correcta": 85},
            {"eq": "20% de 50", "opciones": [10, 25, 20], "correcta": 10},
        ]
    elif nivel == 23:
        titulo_leccion = "Traductores (Equivalencias)"
        instruccion = "¿Cuál es su equivalente?"
        preguntas = [
            {"eq": "Fracción de 0.5", "opciones": ["1/4", "1/2", "3/4"], "correcta": "1/2"},
            {"eq": "Decimal de 1/4", "opciones": [0.25, 0.50, 0.40], "correcta": 0.25},
            {"eq": "Porcentaje de 1/2", "opciones": ["20%", "50%", "100%"], "correcta": "50%"},
            {"eq": "Fracción de 100%", "opciones": ["1/1", "1/2", "1/100"], "correcta": "1/1"},
            {"eq": "Decimal de 10%", "opciones": [1.0, 0.10, 0.01], "correcta": 0.10},
        ]
    elif nivel == 24:
        titulo_leccion = "Repaso Intermedio"
        instruccion = "Combina tus habilidades:"
        preguntas = [
            {"eq": "-5 + 10", "opciones": [5, -5, 15], "correcta": 5},
            {"eq": "3.5 + 1.5", "opciones": [5.0, 4.0, 4.5], "correcta": 5.0},
            {"eq": "1/2 + 0.5", "opciones": ["1.0", "0.5", "1/4"], "correcta": "1.0"},
            {"eq": "50% de 200", "opciones": [100, 50, 20], "correcta": 100},
            {"eq": "(-2) x (-5)", "opciones": [10, -10, 7], "correcta": 10},
        ]
    elif nivel == 25:
        titulo_leccion = "🏆 EXAMEN SECCIÓN 2 🏆"
        instruccion = "DEMUESTRA TU MAESTRÍA:"
        preguntas_pool = [
            {"eq": "-8 + 3", "opciones": [-5, 5, -11], "correcta": -5},
            {"eq": "(-6) x (-3)", "opciones": [18, -18, 9], "correcta": 18},
            {"eq": "3/4 + 1/4", "opciones": ["1", "4/8", "2/4"], "correcta": "1"},
            {"eq": "2.7 + 1.3", "opciones": [4.0, 3.0, 4.1], "correcta": 4.0},
            {"eq": "25% de 80", "opciones": [20, 40, 25], "correcta": 20},
            {"eq": "0.5 equivale a", "opciones": ["50%", "5%", "0.05%"], "correcta": "50%"},
            {"eq": "(-10) ÷ 2", "opciones": [-5, 5, -20], "correcta": -5},
            {"eq": "1.5 - 0.5", "opciones": [1.0, 0.5, 2.0], "correcta": 1.0},
            {"eq": "20% de 50", "opciones": [10, 20, 25], "correcta": 10},
            {"eq": "1/2 equivale a", "opciones": ["0.5", "0.2", "0.12"], "correcta": "0.5"},
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
    
    fondo_ref = ft.Ref[ft.Container]()
    corazon_ref = ft.Ref[ft.Icon]()
    
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
                
                # --- ANIMACIÓN DE DAÑO (FLASH ROJO Y LATIDO) ---
                if fondo_ref.current and corazon_ref.current:
                    # El fondo se vuelve rojo tenue y el corazón crece
                    fondo_ref.current.bgcolor = ft.Colors.RED_100
                    corazon_ref.current.scale = 1.5
                    page.update()
                    
                    # Pausa de milisegundos para "sentir" el golpe
                    time.sleep(0.15)
                    
                    # Todo regresa a la normalidad
                    fondo_ref.current.bgcolor = ft.Colors.WHITE
                    corazon_ref.current.scale = 1.0
                # -----------------------------------------------
                
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

        es_examen = (nivel in [12, 25])
        
        # Lógica de experiencia y mensajes
        if es_teoria:
            xp_total = 5  
            titulo_fin = "¡Teoría Completada!"
            mensaje_velocidad = "¡Conocimiento adquirido! 🧠"
            color_mensaje = ft.Colors.CYAN_600
            texto_tiempo = "--" 
            color_tema = ft.Colors.CYAN_500
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
            color_tema = ft.Colors.AMBER_400

        # --- REFERENCIAS PARA LA ANIMACIÓN MÁGICA ---
        estrellas_refs = [ft.Ref[ft.Icon]() for _ in range(3)]
        xp_text_ref = ft.Ref[ft.Text]()
        btn_glow_ref = ft.Ref[ft.Container]()
        stats_ref = ft.Ref[ft.Container]()

        # --- ELEMENTOS DE LA INTERFAZ ---
        estrellas_ui = ft.Row(
            [
                ft.Icon(ft.Icons.STAR_ROUNDED, color=color_tema, size=50, opacity=0, scale=0, ref=estrellas_refs[0], animate_opacity=200, animate_scale=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT)),
                ft.Icon(ft.Icons.STAR_ROUNDED, color=color_tema, size=75, opacity=0, scale=0, ref=estrellas_refs[1], animate_opacity=200, animate_scale=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT)),
                ft.Icon(ft.Icons.STAR_ROUNDED, color=color_tema, size=50, opacity=0, scale=0, ref=estrellas_refs[2], animate_opacity=200, animate_scale=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT)),
            ],
            alignment=ft.MainAxisAlignment.CENTER, spacing=5
        )

        boton_continuar = ft.Container(
            ref=btn_glow_ref,
            opacity=0, # Oculto al inicio para forzarlos a ver la recompensa
            animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN),
            animate=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT), 
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=2, color=ft.Colors.LIGHT_GREEN_400, offset=ft.Offset(0, 0)),
            content=ft.ElevatedButton(
                "Continuar", bgcolor=ft.Colors.GREEN_500, color=ft.Colors.WHITE, 
                style=ft.ButtonStyle(
                    padding=ft.Padding(left=40, right=40, top=20, bottom=20), 
                    shape=ft.RoundedRectangleBorder(radius=25)
                ),
                on_click=lambda e: on_completado(nivel, xp_total)
            )
        )

        contenedor_principal.content = ft.Column(
            controls=[
                ft.Container(height=40),
                estrellas_ui,
                ft.Text(titulo_fin, size=28, weight=ft.FontWeight.BOLD, color=color_tema, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                
                # El contador de XP inicializado en 0
                ft.Text("+0 XP", size=45, color=ft.Colors.AMBER_500, weight=ft.FontWeight.W_900, ref=xp_text_ref),
                ft.Container(height=10),
                
                # Estadísticas que aparecerán suavemente
                ft.Container(
                    ref=stats_ref,
                    opacity=0,
                    animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN),
                    content=ft.Column([
                        ft.Row([ft.Icon(ft.Icons.TIMER, color=ft.Colors.BLUE_500, size=20), ft.Text(f"Tiempo: {texto_tiempo}", size=16, weight=ft.FontWeight.W_500)], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(mensaje_velocidad, size=14, color=color_mensaje, italic=True, text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.BLUE_GREY_50, padding=15, border_radius=15, width=280
                ),
                
                ft.Container(expand=True),
                boton_continuar,
                ft.Container(height=30),
            ],
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        )
        page.update()

        # --- ORQUESTADOR DE LA ANIMACIÓN ---
        async def secuencia_victoria():
            await asyncio.sleep(0.2)

            # 1. Pop-up de las tres estrellas en cascada
            for ref_estrella in estrellas_refs:
                if ref_estrella.current:
                    ref_estrella.current.opacity = 1
                    ref_estrella.current.scale = 1.0
                    ref_estrella.current.update()
                    await asyncio.sleep(0.15) # Tiempo entre cada estrella
            
            await asyncio.sleep(0.2)

            # 2. Contador de XP acelerado
            paso_xp = max(1, xp_total // 15) # Asegura que cuente rápido aunque ganes mucha XP
            xp_actual = 0
            while xp_actual < xp_total:
                xp_actual += paso_xp
                if xp_actual > xp_total:
                    xp_actual = xp_total
                
                if xp_text_ref.current:
                    xp_text_ref.current.value = f"+{xp_actual} XP"
                    xp_text_ref.current.update()
                await asyncio.sleep(0.04)

            # 3. Revelar las estadísticas de velocidad
            if stats_ref.current:
                stats_ref.current.opacity = 1
                stats_ref.current.update()
            
            await asyncio.sleep(0.4)

            # 4. Revelar el botón y comenzar el GLOW infinito
            if btn_glow_ref.current:
                btn_glow_ref.current.opacity = 1
                btn_glow_ref.current.update()

            while True:
                if btn_glow_ref.current:
                    sombra = btn_glow_ref.current.shadow
                    # Intercala el radio de la sombra para crear el efecto de respiración/latido
                    sombra.blur_radius = 25 if sombra.blur_radius <= 5 else 5
                    try:
                        btn_glow_ref.current.update()
                    except:
                        break # Se detiene silenciosamente si el usuario hace clic y la pantalla cambia
                    await asyncio.sleep(0.8)
                else:
                    break

        # Ejecutamos la magia en segundo plano
        page.run_task(secuencia_victoria)

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
            ft.Row([
                # Aquí inyectamos el corazón animado
                ft.Icon(
                    ft.Icons.FAVORITE, 
                    color=ft.Colors.RED_500 if not es_teoria else ft.Colors.GREY_400,
                    ref=corazon_ref,
                    scale=1.0,
                    animate_scale=ft.Animation(150, ft.AnimationCurve.BOUNCE_OUT)
                ), 
                texto_vidas
            ], spacing=2)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    contenedor_principal = ft.Container(
        ref=fondo_ref, # <-- Referencia inyectada al fondo
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
        padding=20, expand=True, bgcolor=ft.Colors.WHITE,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT) # <-- Suaviza el regreso al blanco
    )

    cargar_paso()
    return contenedor_principal