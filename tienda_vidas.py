import flet as ft


def dialogo_tienda_vidas(page, vidas=5, diamantes=450, on_ir_diamantes=None, on_vidas_cambiadas=None, on_diamantes_cambiados=None):
    
    dialog = ft.AlertDialog()

    def cerrar(e):
        dialog.open = False
        page.update()

    def ir_a_diamantes(e):
        dialog.open = False
        page.update()
        if on_ir_diamantes:
            on_ir_diamantes()

    paquetes = [
        {"cantidad": 1, "precio": 50,  "label": "1 Vida",  "oferta": False},
        {"cantidad": 3, "precio": 130, "label": "3 Vidas", "oferta": False},
        {"cantidad": 5, "precio": 200, "label": "5 Vidas", "oferta": True},
    ]

    saldo_ref = [diamantes]
    vidas_ref = [vidas]

    saldo_txt = ft.Text(
        f"{saldo_ref[0]} diamantes disponibles",
        color=ft.Colors.BLUE_400,
        weight=ft.FontWeight.BOLD,
        size=13,
    )

    corazones_row = ft.Row(
        [ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_500, size=22) for _ in range(min(vidas, 5))],
        spacing=4,
    )

    barra_progreso = ft.ProgressBar(
        value=vidas / 5,
        color=ft.Colors.RED_400,
        bgcolor=ft.Colors.RED_100,
        height=8,
        border_radius=4,
    )

    def comprar(cantidad, precio):
        def handler(e):
            # 1. Validar si ya tenemos el máximo de vidas
            if vidas_ref[0] >= 5:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Ya tienes las vidas al máximo! 💖"),
                    bgcolor=ft.Colors.BLUE_500,
                )
                page.snack_bar.open = True
                page.update()
                return

            # 2. Validar saldo y comprar
            if saldo_ref[0] >= precio:
                saldo_ref[0] -= precio
                vidas_ref[0] = min(vidas_ref[0] + cantidad, 5) # Sumamos, con tope en 5
                
                saldo_txt.value = f"{saldo_ref[0]} diamantes disponibles"
                corazones_row.controls = [
                    ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_500, size=22)
                    for _ in range(vidas_ref[0])
                ]
                barra_progreso.value = vidas_ref[0] / 5
                
                # Le avisamos a main.py que las vidas subieron
                if on_vidas_cambiadas:
                    on_vidas_cambiadas(vidas_ref[0])

                if on_diamantes_cambiados:
                    on_diamantes_cambiados(saldo_ref[0])

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"¡Compraste vida(s)! Ahora tienes {vidas_ref[0]} 💖"),
                    bgcolor=ft.Colors.GREEN_500,
                )
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("No tienes suficientes diamantes 💎"),
                    bgcolor=ft.Colors.RED_400,
                )
                page.snack_bar.open = True
            page.update()
        return handler

    # Barra de vidas actuales
    barra_vidas = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Vidas actuales", color=ft.Colors.GREY_600, size=13),
                        corazones_row,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                barra_progreso,
            ],
            spacing=6,
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=12,
        border=ft.border.all(1, ft.Colors.RED_100),
        margin=ft.margin.only(bottom=10),
    )

    saldo_box = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.BLUE_400, size=18), saldo_txt],
            spacing=6,
        ),
        bgcolor=ft.Colors.BLUE_50,
        border_radius=10,
        padding=10,
        margin=ft.margin.only(bottom=12),
    )

    tarjetas = []
    for p in paquetes:
        badge = ft.Container(
            content=ft.Text("¡OFERTA!", color=ft.Colors.WHITE, size=10, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.GREEN_500,
            border_radius=6,
            padding=ft.padding.symmetric(horizontal=6, vertical=2),
            visible=p["oferta"],
        )
        tarjeta = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_500, size=28),
                            ft.Column(
                                [ft.Text(p["label"], weight=ft.FontWeight.BOLD, size=15), badge],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.WHITE, size=15),
                                ft.Text(str(p["precio"]), color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                            ],
                            tight=True,
                            spacing=5,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_400,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        ),
                        on_click=comprar(p["cantidad"], p["precio"]),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.Colors.RED_50,
            border_radius=12,
            padding=12,
            border=ft.border.all(1, ft.Colors.RED_200),
            margin=ft.margin.only(bottom=6),
        )
        tarjetas.append(tarjeta)

    btn_diamantes = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.PURPLE_500, size=18),
                ft.Text("Necesito más diamantes", color=ft.Colors.PURPLE_500, size=13),
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.PURPLE_300, size=12),
            ],
            spacing=6,
            tight=True,
        ),
        on_click=ir_a_diamantes,
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_500, size=26),
                ft.Text("Tienda de Vidas", weight=ft.FontWeight.BOLD, size=18),
            ],
            spacing=8,
        ),
        content=ft.Column(
            [
                barra_vidas,
                saldo_box,
                *tarjetas,
                ft.Divider(color=ft.Colors.GREY_200),
                btn_diamantes,
            ],
            tight=True,
            spacing=0,
            width=300,
            scroll=ft.ScrollMode.HIDDEN,
        ),
        actions=[ft.TextButton("Cerrar", on_click=cerrar)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dialog