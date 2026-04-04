import flet as ft
import calendar
import datetime
import threading
import time

def dialogo_racha_calendario(page, racha, ultima_interaccion, dias_jugados):
    dialog = ft.AlertDialog()
    corriendo = True
    
    hoy = datetime.date.today()
    ahora = datetime.datetime.now()

    # Calcular estado dinámico de la racha actual
    racha_activa = False
    segundos_restantes = 0
    
    if racha > 0 and ultima_interaccion:
        tiempo_pasado = (ahora - ultima_interaccion).total_seconds()
        if tiempo_pasado <= 86400: # 24 hrs
            racha_activa = True
            segundos_restantes = 86400 - tiempo_pasado
        else:
            racha = 0

    def cerrar(e):
        nonlocal corriendo
        corriendo = False
        dialog.open = False
        page.update()

    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
    }
    nombre_mes = f"{meses_es[hoy.month]} {hoy.year}"

    # UI del Temporizador y Animación
    texto_temporizador = ft.Text("", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_500, text_align=ft.TextAlign.CENTER)
    
    icono_fuego_grande = ft.Icon(
        ft.Icons.LOCAL_FIRE_DEPARTMENT, 
        color=ft.Colors.ORANGE_500 if racha_activa else ft.Colors.GREY_300, 
        size=60
    )
    
    # Contenedor para la animación de pulsación
    contenedor_fuego = ft.Container(
        content=icono_fuego_grande,
        animate_scale=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),
        scale=1.0,
        alignment=ft.Alignment.CENTER
    )

    # Días activos de este mes usando los datos reales
    dias_mes_racha = [d.day for d in dias_jugados if d.month == hoy.month and d.year == hoy.year]

    encabezado = ft.Row(
        [
            ft.Container(content=ft.Text(d, size=11, color=ft.Colors.GREY_400, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER), width=36, alignment=ft.Alignment(0, 0))
            for d in dias_semana
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=2,
    )

    cal = calendar.monthcalendar(hoy.year, hoy.month)
    filas = []

    for semana in cal:
        celdas = []
        for dia in semana:
            if dia == 0:
                celdas.append(ft.Container(width=36, height=44))
            elif dia in dias_mes_racha:
                es_hoy = dia == hoy.day
                celda = ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("🔥", size=16, text_align=ft.TextAlign.CENTER),
                            ft.Text(str(dia), size=10, color=ft.Colors.ORANGE_700, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    width=36, height=44, bgcolor=ft.Colors.ORANGE_50, border_radius=10, alignment=ft.Alignment(0, 0),
                    border=ft.border.all(2 if es_hoy else 1, ft.Colors.ORANGE_500 if es_hoy else ft.Colors.ORANGE_200),
                )
                celdas.append(celda)
            else:
                es_hoy = dia == hoy.day
                es_futuro = dia > hoy.day
                celda = ft.Container(
                    content=ft.Text(
                        str(dia), size=12, color=ft.Colors.GREY_300 if es_futuro else ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD if es_hoy else ft.FontWeight.NORMAL,
                    ),
                    width=36, height=44, alignment=ft.Alignment(0, 0), border_radius=10,
                    border=ft.border.all(2, ft.Colors.BLUE_300) if es_hoy else None,
                )
                celdas.append(celda)

        filas.append(ft.Row(celdas, alignment=ft.MainAxisAlignment.CENTER, spacing=2))

    stats = ft.Container(
        content=ft.Row(
            [
                ft.Column([ft.Row([ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.ORANGE_500, size=22), ft.Text(str(racha), size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_600)], spacing=4), ft.Text("Racha actual", color=ft.Colors.GREY_500, size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                ft.Container(width=1, height=40, bgcolor=ft.Colors.GREY_200),
                ft.Column([ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_400, size=22), ft.Text(str(len(dias_mes_racha)), size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_500)], spacing=4), ft.Text("Días este mes", color=ft.Colors.GREY_500, size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        bgcolor=ft.Colors.ORANGE_50, border_radius=14, padding=14, border=ft.border.all(1, ft.Colors.ORANGE_100), margin=ft.margin.only(bottom=14),
    )

    leyenda = ft.Row(
        [
            ft.Row([ft.Text("🔥", size=14), ft.Text("Día jugado", size=11, color=ft.Colors.GREY_500)], spacing=4),
            ft.Container(content=ft.Text("  ", size=11), width=16, height=16, bgcolor=ft.Colors.BLUE_50, border_radius=4, border=ft.border.all(2, ft.Colors.BLUE_300)),
            ft.Text("Hoy", size=11, color=ft.Colors.GREY_500),
        ], spacing=8, alignment=ft.MainAxisAlignment.CENTER,
    )

    dialog = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=25), # <-- NUEVO
        elevation=10, # <-- NUEVO
        title=ft.Row([ft.Text("Estado de tu racha", weight=ft.FontWeight.BOLD, size=18)], alignment=ft.MainAxisAlignment.CENTER),
        content=ft.Column(
            [
                ft.Container(content=contenedor_fuego, alignment=ft.Alignment.CENTER, height=70),
                ft.Container(content=texto_temporizador, alignment=ft.Alignment.CENTER, margin=ft.margin.only(bottom=10)),
                stats,
                ft.Row(
                    [ft.Icon(ft.Icons.CHEVRON_LEFT, color=ft.Colors.GREY_400, size=20),
                     ft.Text(nombre_mes, weight=ft.FontWeight.BOLD, size=15, color=ft.Colors.GREY_700),
                     ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400, size=20)],
                    alignment=ft.MainAxisAlignment.CENTER, spacing=10,
                ),
                ft.Container(height=6), encabezado, ft.Container(height=4),
                *filas,
                ft.Container(height=8), ft.Divider(color=ft.Colors.GREY_100), leyenda,
            ], tight=True, spacing=4, width=290,
        ),
        actions=[ft.TextButton("Cerrar", on_click=cerrar)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Función en Background para actualizar el timer y la animación
    def actualizar_timer_ui():
        nonlocal segundos_restantes, racha_activa, racha
        while corriendo and dialog.open:
            if racha_activa:
                segundos_restantes -= 1
                if segundos_restantes <= 0:
                    racha_activa = False
                    racha = 0
                    texto_temporizador.value = "Racha perdida"
                    icono_fuego_grande.color = ft.Colors.GREY_300
                    contenedor_fuego.scale = 1.0
                else:
                    h = int(segundos_restantes // 3600)
                    m = int((segundos_restantes % 3600) // 60)
                    s = int(segundos_restantes % 60)
                    texto_temporizador.value = f"⏳ Tiempo para perder racha: {h:02d}:{m:02d}:{s:02d}"
                    texto_temporizador.color = ft.Colors.RED_500
                    
                    # Logica de latido (Toggle entre scale 1.0 y 1.2)
                    contenedor_fuego.scale = 1.2 if contenedor_fuego.scale == 1.0 else 1.0
            else:
                texto_temporizador.value = "¡Completa una nueva lección\npara encender tu racha!"
                texto_temporizador.color = ft.Colors.GREY_500
                contenedor_fuego.scale = 1.0

            try:
                page.update()
            except Exception:
                break # Evita crasheo si se cierra de golpe
            time.sleep(1)

    dialog.on_dismiss = lambda e: cerrar(e)
    
    # Inicia el hilo en background
    threading.Thread(target=actualizar_timer_ui, daemon=True).start()

    return dialog