import flet as ft
import mysql.connector
from datetime import datetime
import smtplib
import locale
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurar locale para español/Argentina
locale.setlocale(locale.LC_TIME, 'spanish_argentina')

# Precios de las habitaciones (ARS)
PRECIOS_HABITACIONES = {
    " Servicio Familiar      ": 44000,
    " Servicio Spa           ": 35000,
    " Servicio Suite de lujo ": 128000,
    " Servicio Estandar      ": 22000
}

def main(page: ft.Page):
    page.window.maximized = True
    page.title = "Hotel Sheldon"
    page.theme_mode = "light"
    page.scroll = "auto"
    page.bgcolor = "#E3D8D4"
    selected_section = ft.Ref[ft.Text]()
    nav_bar = ft.Row(controls=[], alignment=ft.alignment.top_right, animate_size=25, spacing=20)
    nav_container = ft.Container(
        content=nav_bar,
        bgcolor="#FAFAFA",
        padding=ft.padding.all(10),
        border_radius=9,
        alignment=ft.alignment.top_right,
    )
    main_content = ft.Column([], expand=True)

    def guardar_reserva_en_db(fecha_ingreso, fecha_salida, nombre, telefono, email, preferencias, cantidad, tipo, total):
        conexion = mysql.connector.connect(
            host="localhost",
            user="tu_usuario",
            password="tu_contraseña",
            database="hotel_sheldon"
        )
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO reservas (fecha_ingreso, fecha_salida, nombre, telefono, email, preferencias, cantidad, tipo_habitacion, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (fecha_ingreso, fecha_salida, nombre, telefono, email, preferencias, cantidad, tipo, total)
        cursor.execute(consulta, valores)
        conexion.commit()
        cursor.close()
        conexion.close()

    def nav_button(text, route):
        return ft.TextButton(
            text,
            on_click=lambda _: go_to(route),
            style=ft.ButtonStyle(
                bgcolor="#ded1c4" if selected_section.current.value == text else None,
                shape=ft.RoundedRectangleBorder(radius=9),
                padding=10
            )
        )

    def go_to(section):
        section = section.lower()
        selected_section.current.value = section.capitalize()
        nav_bar.controls.clear()
        for name in ["Inicio", "Sobre Nosotros", "Servicios", "Contactos", "Reservas", "Reseñas"]:
            nav_bar.controls.append(nav_button(name, name.lower()))
        main_content.controls.clear()
        if section == "inicio":
            main_content.controls.append(inicio())
        elif section == "sobre nosotros":
            main_content.controls.append(sobre_nosotros())
        elif section == "servicios":
            main_content.controls.append(servicios())
        elif section == "contactos":
            main_content.controls.append(contactos())
        elif section == "reservas":
            main_content.controls.append(reserva())
        elif section == "reseñas":
            main_content.controls.append(ft.Text("Sección de reseñas..."))
        page.update()

    def inicio():
        return ft.Container(
            expand=True,
            content=ft.Stack([
                ft.Image(
                    src="https://images.unsplash.com/photo-1566073771259-6a8506099945",
                    width=page.width,
                    height=page.height,
                    fit=ft.ImageFit.COVER
                ),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.5, "Brown"),
                    width=page.width,
                    height=page.height
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Image(src="logo_sheldon.png", width=160, height=160),
                        ft.Text("Bienvenidos al Hotel Sheldon", size=32, weight="bold", color="white"),
                        ft.Text("Descansá. Disfrutá. Sentite como en casa.", size=20, italic=True, color="white"),
                        ft.ElevatedButton(
                            "Reservar ahora",
                            bgcolor="#D9BBA9",
                            color="black",
                            on_click=lambda _: go_to("reservas")
                        )
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ]))

    def sobre_nosotros():
        return ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "\n¡BIENVENIDOS AL HOTEL SHELDON!\n\n"
                        "Localizado en Unquillo, ofrece 100 habitaciones diseñadas para todo tipo de viajeros. "
                        "Incluyendo servicios como suites de lujo, espacios familiares y un spa exclusivo para el descanso total, entre muchos más.\n\n"
                        "Nuestro objetivo es brindar una experiencia única, combinando atención personalizada.\n\n"
                        "A futuro, buscamos consolidarnos como un referente en hospitalidad, apostando por la sostenibilidad, innovación "
                        "y nuevos servicios que enriquezcan cada estancia. En Sheldon, cada visita se transforma en un recuerdo memorable.\n\n"
                        "Entre nuestros servicios más destacados se encuentran nuestras exclusivas suites, pensadas para quienes buscan "
                        "un entorno refinado y lleno de detalles únicos. Las habitaciones familiares ofrecen el espacio ideal para compartir momentos "
                        "especiales, mientras que nuestro completo spa invita al relax profundo, cuidando cuerpo y mente en un ambiente sereno y moderno.",
                        size=18, italic= True
                    )
                ], scroll=ft.ScrollMode.ALWAYS),
                padding=20,
                bgcolor="#FAFAFA",
                border_radius=15,
                width=page.width * 0.5 if page.width else 500,
                height=600
            ),
            ft.Container(
                content=ft.Image(
                    src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                    width=600,
                    height=600,
                    border_radius=15,
                    fit=ft.ImageFit.COVER
                ),
                padding=10,
                alignment=ft.alignment.center
            )
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    def servicios():
        servicios_data = [
            {
                "img": "https://images.unsplash.com/photo-1667450799167-09e7dd903e59?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "titulo": "Servicio Familiar",
                "desc":
                    "• Habitaciones amplias y versátiles, con camas cómodas y espacio para toda la familia.\n"
                    "• Comodidades para niños como cunas y juguetes.\n"
                    "• Conexión Wi-Fi y entretenimiento para todos."
            },
            {
                "img": "https://images.unsplash.com/photo-1532926381893-7542290edf1d?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "titulo": "Servicio Spa",
                "desc":
                    "• Área de spa con sauna, jacuzzi y vapor.\n"
                    "• Masajes de lujo y tratamientos exclusivos.\n"
                    "• Piscina climatizada para relajación total."
            },
            {
                "img": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?q=80&w=580&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "titulo": "Suite de Lujo",
                "desc":
                    "• Suite presidencial con cama king size y sala privada.\n"
                    "• Servicio de concierge y barra gourmet exclusiva.\n"
                    "• Vista panorámica y amenities de alto nivel."
            },
            {
                "img": "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "titulo": "Servicio Estándar",
                "desc":
                    "• Cama confortable y clima ideal para un descanso reparador.\n"
                    "• Baño privado equipado con lo justo y necesario.\n"
                    "• Conexión Wi-Fi y entretenimiento para todos.\n"
                    "• Escritorio funcional, WiFi rápido y TV para tu entretenimiento.\n"
                    "• Extras útiles: cafetera/minibar, caja fuerte, plancha, secador."
            }
        ]

        def servicio_card(data: dict) -> ft.Column:
            def open_dialog(e):
                dlg = ft.AlertDialog(
                    title=ft.Text(data["titulo"], color=ft.Colors.WHITE, size=20, weight='bold'),
                    content=ft.Text(data["desc"], color=ft.Colors.WHITE, size=19, weight='bold'),
                    modal=True,
                    title_padding=ft.padding.all(20),
                    bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
                    on_dismiss=lambda e: print("Dialog dismissed!"),
                )
                def close_action(e):
                    dlg.open = False
                    page.update()
                dlg.actions = [
                    ft.TextButton("Cerrar", on_click=close_action)
                ]
                page.open(dlg)
            return ft.Column(
                [
                    ft.Container(
                        content=ft.Image(
                            src=data["img"],
                            width=299,
                            height=230,
                            border_radius=20,
                            fit=ft.ImageFit.COVER,
                        ),
                        border_radius=ft.border_radius.all(15),
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        ink=True,
                        on_click=open_dialog,
                    ),
                    ft.Text(
                        data["titulo"],
                        size=16,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        extras = [
            {"icon": ft.Icons.WIFI, "label": "Wi-Fi"},
            {"icon": ft.Icons.FREE_BREAKFAST, "label": "Desayuno"},
            {"icon": ft.Icons.POOL, "label": "Piscina"},
            {"icon": ft.Icons.RESTAURANT, "label": "Comidas"},
            {"icon": ft.Icons.LOCAL_PARKING, "label": "Estacionamiento"},
            {"icon": ft.Icons.PETS, "label": "Pet Friendly"}
        ]

        return ft.Column([
            ft.Container(
                bgcolor="#FAFAFA",
                border_radius=30,
                padding=30,
                content=ft.Row(
                    [servicio_card(s) for s in servicios_data],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    spacing=30,
                    wrap=True,
                )
            ),
            ft.Container(
                bgcolor="#E9DED1",
                padding=20,
                border_radius=20,
                content=ft.Row([
                    ft.Column([
                        ft.Icon(e["icon"], size=40),
                        ft.Text(e["label"], size=14),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    for e in extras
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            )
        ])

    def contactos():
        return ft.Container(
            expand=True,
            content=ft.Stack([
                ft.Image(
                    src="https://i0.wp.com/foodandpleasure.com/wp-content/uploads/2020/10/65345792-h1-facb_angular_pool_view_300dpi.jpg?fit=2800%2C1867&ssl=1",
                    width=page.width,
                    height=page.height,
                    fit=ft.ImageFit.COVER
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Container(
                        padding=30,
                        bgcolor=ft.Colors.with_opacity(0.7, "white"),
                        border_radius=20,
                        content=ft.Column([
                            ft.Image(src="logo_sheldon.png", width=120),
                            ft.Text("Correo: HotelSheldon@gmail.com", size=20),
                            ft.Text("Teléfono: +54 X XXX XXX-XXXX", size=20),
                            ft.Text("           Dirección: Alcides Casatti, Unquillo, Córdoba", size=20),
                            ft.Text("Instagram: @Hotel.sheldon.oficial", size=20),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10)
                    )
                )
            ], alignment=ft.alignment.center))

    def reserva():
        check_in_picker = ft.DatePicker(
            first_date=datetime(year=2025, month=12, day=1),
            last_date=datetime(year=2027, month=12, day=1)
        )
        check_out_picker = ft.DatePicker(
            first_date=datetime(year=2025, month=12, day=1),
            last_date=datetime(year=2027, month=12, day=1)
        )
        check_in_field = ft.TextField(label="Fecha de ingreso (DD/MM/AAAA)", read_only=True, width=200)
        check_out_field = ft.TextField(label="Fecha de salida (DD/MM/AAAA)", read_only=True, width=200)
        check_in_button = ft.ElevatedButton(
            'Seleccionar fecha de ingreso',
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda _: page.open(check_in_picker)
        )
        check_out_button = ft.ElevatedButton(
            'Seleccionar fecha de salida',
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda _: page.open(check_out_picker)
        )

        def handle_check_in_change(e):
            fecha = e.control.value
            check_in_field.value = fecha.strftime("%d/%m/%Y")
            actualizar_resumen()
            page.update()

        def handle_check_out_change(e):
            fecha = e.control.value
            check_out_field.value = fecha.strftime("%d/%m/%Y")
            actualizar_resumen()
            page.update()

        check_in_picker.on_change = handle_check_in_change
        check_out_picker.on_change = handle_check_out_change

        nombre = ft.TextField(label="Nombre completo", width=400)
        telefono = ft.TextField(label="Teléfono", width=400)
        email = ft.TextField(label="Email", width=400)

        preferencias_opcionales = {
            "Fumadores": {"switch": ft.Switch(label="Fumadores",animate_size=20, label_position=ft.LabelPosition.LEFT, value=False, scale=0.8), "valor": "No"},
            "Cama extra": {"switch": ft.Switch(label="Cama extra",animate_size=20, label_position=ft.LabelPosition.LEFT, value=False, scale=0.8), "valor": "No"},
            "Piso alto": {"switch": ft.Switch(label="Piso alto",animate_size=20, label_position=ft.LabelPosition.LEFT, value=False, scale=0.8), "valor": "No"}
        }

        def toggle_preferencia(preferencia):
            def _toggle_preferencia(e):
                preferencias_opcionales[preferencia]["valor"] = "Sí" if preferencias_opcionales[preferencia]["valor"] == "No" else "No"
                preferencias_opcionales[preferencia]["switch"].value = preferencias_opcionales[preferencia]["valor"] == "Sí"
                actualizar_resumen()
                page.update()
            return _toggle_preferencia

        def limpiar_preferencia(preferencia):
            def _limpiar_preferencia(e):
                preferencias_opcionales[preferencia]["valor"] = "No"
                preferencias_opcionales[preferencia]["switch"].value = False
                actualizar_resumen()
                page.update()
            return _limpiar_preferencia

        preferencias_controls = []
        for preferencia, data in preferencias_opcionales.items():
            data["switch"].on_change = toggle_preferencia(preferencia)
            row = ft.Row(
                [
                    data["switch"],
                ],
                alignment=ft.MainAxisAlignment.START,
                width=450
            )
            preferencias_controls.append(row)

        preferencias_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Preferencias Opcionales", size=20, weight="bold"),
                    *preferencias_controls
                ],
                spacing=20,
                width=500
            ),
            padding=20,
            bgcolor=ft.Colors.GREY_200,
            border_radius=15,
            alignment=ft.alignment.top_left,
        )

        resumen_container = ft.Column([], spacing=9)
        total_reserva = ft.Text("Total: $0 ARS", size=20, weight="bold")

        tipos_habitaciones = {
            " Servicio Familiar      ": ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=50),
            " Servicio Spa           ": ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=50),
            " Servicio Suite de lujo ": ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=50),
            " Servicio Estandar      ": ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=50)
        }

        def minus_click(habitacion):
            def _minus_click(e):
                current_value = int(tipos_habitaciones[habitacion].value)
                if current_value > 0:
                    tipos_habitaciones[habitacion].value = str(current_value - 1)
                    actualizar_resumen()
                    page.update()
            return _minus_click

        def plus_click(habitacion):
            def _plus_click(e):
                current_value = int(tipos_habitaciones[habitacion].value)
                tipos_habitaciones[habitacion].value = str(current_value + 1)
                actualizar_resumen()
                page.update()
            return _plus_click

        habitacion_controls = []
        for habitacion in tipos_habitaciones:
            row = ft.Row(
                [
                    ft.Text(habitacion, size=16),
                    ft.IconButton(ft.Icons.REMOVE, on_click=minus_click(habitacion)),
                    tipos_habitaciones[habitacion],
                    ft.IconButton(ft.Icons.ADD, on_click=plus_click(habitacion)),
                    ft.Text(f"${PRECIOS_HABITACIONES[habitacion]} ARS/noche", size=14, color=ft.Colors.GREY_600)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                width=450
            )
            habitacion_controls.append(row)

        def calcular_total():
            total = 0
            for habitacion, cantidad in tipos_habitaciones.items():
                total += int(cantidad.value) * PRECIOS_HABITACIONES[habitacion]
            return total

        def actualizar_resumen():
            resumen_container.controls.clear()
            total = calcular_total()
            if check_in_field.value and check_out_field.value:
                try:
                    ingreso = datetime.strptime(check_in_field.value, "%d/%m/%Y")
                    salida = datetime.strptime(check_out_field.value, "%d/%m/%Y")
                    noches = (salida - ingreso).days
                    total *= noches
                except:
                    noches = 1
            if check_in_field.value:
                resumen_container.controls.append(
                    ft.Row([
                        ft.Text(f"Fecha de ingreso: {check_in_field.value}"),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e: limpiar_campo(check_in_field, check_in_picker)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            if check_out_field.value:
                resumen_container.controls.append(
                    ft.Row([
                        ft.Text(f"Fecha de salida: {check_out_field.value}"),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e: limpiar_campo(check_out_field, check_out_picker)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            for habitacion, cantidad in tipos_habitaciones.items():
                if int(cantidad.value) > 0:
                    resumen_container.controls.append(
                        ft.Row([
                            ft.Text(f"{habitacion}: {cantidad.value}"),
                            ft.IconButton(ft.Icons.DELETE, on_click=lambda e, h=habitacion: limpiar_habitacion(h)),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
            for preferencia, data in preferencias_opcionales.items():
                if data["valor"] == "Sí":
                    resumen_container.controls.append(
                        ft.Row([
                            ft.Text(f"{preferencia}: {data['valor']}"),
                            ft.IconButton(ft.Icons.DELETE, on_click=limpiar_preferencia(preferencia)),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
            if nombre.value:
                resumen_container.controls.append(
                    ft.Row([
                        ft.Text(f"Nombre: {nombre.value}"),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e: limpiar_campo(nombre)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            if telefono.value:
                resumen_container.controls.append(
                    ft.Row([
                        ft.Text(f"Teléfono: {telefono.value}"),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e: limpiar_campo(telefono)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            if email.value:
                resumen_container.controls.append(
                    ft.Row([
                        ft.Text(f"Email: {email.value}"),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e: limpiar_campo(email)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            total_reserva.value = f"Total: ${total} ARS"
            page.update()

        def limpiar_campo(campo, picker=None):
            campo.value = ""
            if picker:
                picker.value = None
            actualizar_resumen()
            page.update()

        def limpiar_habitacion(habitacion):
            tipos_habitaciones[habitacion].value = "0"
            actualizar_resumen()
            page.update()

        def enviar_reserva(e):
            if not all([check_in_field.value, check_out_field.value, nombre.value, telefono.value, email.value]):
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, completá todos los campos obligatorios."), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            try:
                ingreso = datetime.strptime(check_in_field.value, "%d/%m/%Y")
                salida = datetime.strptime(check_out_field.value, "%d/%m/%Y")
                if salida <= ingreso:
                    page.snack_bar = ft.SnackBar(ft.Text("La fecha de salida debe ser posterior a la de ingreso."), bgcolor="red")
                    page.snack_bar.open = True
                    page.update()
                    return
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Formato de fecha incorrecto. Usá DD/MM/AAAA."), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            habitaciones_reservadas = {}
            for habitacion, cantidad in tipos_habitaciones.items():
                if int(cantidad.value) > 0:
                    habitaciones_reservadas[habitacion] = cantidad.value
            if not habitaciones_reservadas:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, seleccioná al menos un tipo de habitación."), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            noches = (salida - ingreso).days
            total = 0
            for habitacion, cantidad in habitaciones_reservadas.items():
                total += int(cantidad) * PRECIOS_HABITACIONES[habitacion] * noches
                guardar_reserva_en_db(
                    check_in_field.value,
                    check_out_field.value,
                    nombre.value,
                    telefono.value,
                    email.value,
                    ", ".join([f"{p}: {preferencias_opcionales[p]['valor']}" for p in preferencias_opcionales]),
                    cantidad,
                    habitacion,
                    total
                )
            enviar_confirmacion_email(
                email.value,
                nombre.value,
                check_in_field.value,
                check_out_field.value,
                habitaciones_reservadas,
                total,
                preferencias_opcionales
            )
            page.snack_bar = ft.SnackBar(ft.Text("Reserva guardada con éxito."), bgcolor="green")
            page.snack_bar.open = True
            page.update()

        fecha_ingreso_row = ft.Row(
            controls=[
                check_in_field,
                check_in_button
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )
        fecha_salida_row = ft.Row(
            controls=[
                check_out_field,
                check_out_button
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )
        tipos_habitaciones_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Tipo de habitaciones", size=20, weight="bold"),
                    *habitacion_controls
                ],
                spacing=10,
                width=500
            ),
            padding=20,
            bgcolor=ft.Colors.GREY_200,
            border_radius=15,
            alignment=ft.alignment.top_left,
        )

        main_row = ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Formulario de Reserva", size=28, italic=True, weight="bold"),
                            fecha_ingreso_row,
                            fecha_salida_row,
                            nombre,
                            telefono,
                            email,
                            tipos_habitaciones_container,
                            preferencias_container,
                            ft.ElevatedButton("Confirmar Reserva", bgcolor="#D9BBA9", color="black", on_click=enviar_reserva)
                        ],
                        spacing=10,
                        width=500
                    ),
                    padding=8,
                    alignment=ft.alignment.top_left,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Resumen de la Reserva", size=28, italic=True, weight="bold"),
                            resumen_container,
                            total_reserva
                        ],
                        spacing=20,
                        width=740
                    ),
                    padding=ft.padding.only(top=9, left=30, right=30, bottom=30),
                    bgcolor=ft.Colors.GREY_200,
                    border_radius=10,
                    alignment=ft.alignment.top_center,
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        nombre.on_change = lambda e: actualizar_resumen()
        telefono.on_change = lambda e: actualizar_resumen()
        email.on_change = lambda e: actualizar_resumen()

        return main_row

    selected_section.current = ft.Text("Inicio")
    go_to("inicio")
    page.add(
        ft.Container(content=nav_container, alignment=ft.alignment.top_center),
        ft.Container(content=main_content, expand=True, alignment=ft.alignment.top_center)
    )

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "tucorreo@gmail.com"
EMAIL_PASS = "tu_contraseña"

def enviar_confirmacion_email(destinatario, nombre, ingreso, salida, habitaciones, total, preferencias):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirmación de reserva - Hotel Sheldon"
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario
    texto = f"""
Hola {nombre},
Tu reserva en Hotel Sheldon ha sido confirmada.
Fecha de ingreso: {ingreso}
Fecha de salida: {salida}
Detalle de habitaciones:
"""
    for habitacion, cantidad in habitaciones.items():
        texto += f"- {habitacion}: {cantidad} (${PRECIOS_HABITACIONES[habitacion]} ARS/noche)\n"
    texto += "\nPreferencias:\n"
    for preferencia, data in preferencias.items():
        texto += f"- {preferencia}: {data['valor']}\n"
    texto += f"\nTotal de la reserva: ${total} ARS\n\n¡Te esperamos!\n\nHotel Sheldon"
    parte_texto = MIMEText(texto, "plain")
    msg.attach(parte_texto)
    try:
        servidor = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        servidor.starttls()
        servidor.login(EMAIL_USER, EMAIL_PASS)
        servidor.sendmail(EMAIL_USER, destinatario, msg.as_string())
        servidor.quit()
        print("Correo de confirmación enviado.")
    except Exception as e:
        print("Error al enviar el correo:", e)

ft.app(target=main)
