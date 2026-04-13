import flet as ft

class Tile1(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = 300
        # REMOVED: self.height = 700 
        # This allows the container to shrink-wrap the content
        self.border_radius = 8
        self.padding = ft.padding.only(top=8, left=12, right=12, bottom=8)
        self.border = ft.border.all(1, "#ffffff")
        
        self.bgcolor = "#ffffff"

        self.blue_hex = "#0077b6"
        self.blue_glass = ft.LinearGradient(colors=[self.blue_hex, "#004e92"])
        self.red_glass = ft.LinearGradient(colors=["#e63946", "#b91c1c"])
        self.green_glass = ft.LinearGradient(colors=["#28a745", "#1e7e34"])

        self.ui_refs = {} 
        content_controls = []

        def create_section_header(text, color_hex):
            return ft.Container(
                content=ft.Text(text, size=13, weight="bold", color=color_hex),
                alignment=ft.Alignment(0, 0), 
                border=ft.border.only(bottom=ft.BorderSide(1.5, color_hex)),
                padding=ft.padding.only(bottom=1), 
                margin=ft.margin.only(bottom=4, top=4)
            )

        def create_popup_menu(key, label, default_display, options_tuples):
            
            display_text = ft.Text(default_display, size=11, color="#343a40", weight="bold")
            self.ui_refs[key] = display_text
            
            
            def on_select(e):
        
                display_text.value = e.control.data 
                display_text.content_text = e.control.content.value 
        
                if hasattr(display_text, "on_change") and display_text.on_change:
                    display_text.on_change(None)
                display_text.update()

            
            menu = ft.PopupMenuButton(
            content=ft.Row([display_text, ft.Icon(ft.Icons.ARROW_DROP_DOWN, color="#343a40", size=16)], 
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
            items=[ft.PopupMenuItem(content=ft.Text(opt[1], size=11), data=str(opt[0]), on_click=on_select) for opt in options_tuples],
            )
            return ft.Column([
                ft.Text(label, size=11, weight="bold", color="#343a40"),
                ft.Container(content=menu, height=26, width=270, bgcolor="#ffffff", border=ft.border.all(1, "#adb5bd"), 
                     border_radius=3, padding=ft.padding.only(left=8, right=4), alignment=ft.Alignment(-1, 0)) 
            ], spacing=0)

        def create_digital_input(key, label, val, step, min_v, max_v, glass_gradient):
            readout = ft.TextField(value=val, width=210, height=26, text_size=11, color="#ffffff", bgcolor="#343a40", 
                                   border_radius=3, text_align="center", content_padding=0, border_width=0, 
                                   on_submit=lambda e: self.validate_and_snap(e.control, min_v, max_v, step), 
                                   on_blur=lambda e: self.validate_and_snap(e.control, min_v, max_v, step))
            self.ui_refs[key] = readout
            return ft.Column([
                ft.Text(label, size=11, weight="bold", color="#343a40"),
                ft.Row([
                    ft.Container(content=ft.Text("-", size=12, color="white", weight="bold"), gradient=glass_gradient, width=26, height=26, border_radius=3, alignment=ft.Alignment(0, 0), on_click=lambda _: self.step_val(readout, -step, min_v, max_v)), 
                    readout, 
                    ft.Container(content=ft.Text("+", size=12, color="white", weight="bold"), gradient=glass_gradient, width=26, height=26, border_radius=3, alignment=ft.Alignment(0, 0), on_click=lambda _: self.step_val(readout, step, min_v, max_v))
                ], spacing=2)
            ], spacing=0)

        # Build Sections
        content_controls.append(create_section_header("Putter Head Specs", self.blue_hex))
        content_controls.append(create_digital_input("head_w", "Head Weight (G)", "350", 1, 310, 400, self.blue_glass))
        content_controls.append(create_digital_input("lie_angle", "Lie Angle (Deg)", "70", 1, 64, 76, self.blue_glass))
        content_controls.append(create_digital_input("lean", "Shaft Lean (Deg)", "0", 1, -3, 3, self.blue_glass))

        content_controls.append(create_section_header("Assembly Specs", "#e63946"))
        content_controls.append(create_digital_input("len", "Assembled Length (In)", "35.00", 0.25, 30.0, 38.0, self.red_glass))
        content_controls.append(create_digital_input("u_shaft_w", "Uncut Shaft Weight (G)", "120", 5, 100, 150, self.red_glass))
        content_controls.append(create_popup_menu("g_len", "Grip Length", "10.0", [
    (10.0, "Standard (~10\")"), 
    (16.0, "Long (~16\")")
]))

        content_controls.append(create_digital_input("g_dia", "Grip Diameter (In)", "0.90", 0.1, 0.8, 1.7, self.red_glass))
        content_controls.append(create_popup_menu("g_mat", "Grip Material", "0.85", [
            (0.85, '0.85, (Rubber)'), 
            (0.90, '0.90, (Polyurethane)')
        ]))
        content_controls.append(create_digital_input("g_w", "Grip Weight (G)", "60", 2, 50, 150, self.red_glass))

        content_controls.append(create_section_header("Player Control", "#28a745"))
        content_controls.append(create_digital_input("g_force", "Grip Force (Lbf)", "5.00", 0.5, 1.5, 12.0, self.green_glass))
        content_controls.append(create_popup_menu("g_span", "Grip Span", "7.5", [
    (9.0, '9.0" (10-Finger/Split)'), 
    (7.5, '7.5" (Standard Overlap)'), 
    (5.5, '5.5" (Close/Interlock)')
]))
        content_controls.append(create_digital_input("g_choke", "Grip Choke (In)", "-0.10", 0.1, -5.0, 0.0, self.green_glass))
        content_controls.append(create_digital_input("v", "Stroke Velocity (Fps)", "4.40", 0.2, 1.6, 14.6, self.green_glass))

        # ADDED: A small spacer at the end to match Tile 2's bottom margin
        content_controls.append(ft.Container(height=2))

        self.main_col = ft.Column(controls=content_controls, spacing=1, scroll=None)
        self.content = self.main_col

    def validate_and_snap(self, control, min_v, max_v, step):
        try:
            val = round(float(control.value) / step) * step
            actual_min, actual_max = min(min_v, max_v), max(min_v, max_v)
            val = max(actual_min, min(actual_max, val))
            control.value = str(int(val)) if step >= 1 else f"{val:.2f}"
            control.update()
        except: 
            control.value = f"{min_v:.2f}"
            control.update()

    def step_val(self, readout, delta, min_v, max_v):
        try:
            new_val = float(readout.value) + delta
            actual_min, actual_max = min(min_v, max_v), max(min_v, max_v)
            new_val = max(actual_min, min(actual_max, new_val))
            readout.value = str(int(new_val)) if abs(delta) >= 1 else f"{new_val:.2f}"
            if readout.on_change:
                readout.on_change(None)
            readout.update()
        except: pass