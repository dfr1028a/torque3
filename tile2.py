import flet.canvas as cv
import flet as ft
import math


class Tile2(ft.Container):
    def __init__(self, benchmark_y=0.40, **kwargs):
        super().__init__(**kwargs)
        self.benchmark_y = benchmark_y  # This stores the 0.40 from your engine
        self.on_change = None  # This holds the connection to main2.py
        self.INCH_TO_PX = 24.25 / 0.42  # ~65.54 pixels per inch
       
        self.width = 400
        self.height = 445
        self.bgcolor = "white"
        self.border = ft.border.all(1, "#ffffff")
        self.padding = 10
        self.border_radius = 8


        self.head_images = {
    "Blade": "assets/blade.png",
    "Wide Blade": "assets/wide_blade.png",
    "Mid Mallet": "assets/mid_mallet.png",
    "MOI Mallet": "assets/moi_mallet.png"
}
       
       
# CG Offsets: Distance (in inches) to shift image to keep Red Dot at origin
        self.cg_offsets = {
            "Blade":      {"left": 0.15, "top": 0.10},
            "Wide Blade": {"left": 0.35, "top": 0.10},
            "Mid Mallet": {"left": 0.55, "top": 0.10},
            "MOI Mallet": {"left": 0.95, "top": 0.10}  
        }


        # Visual adjustment (in pixels) for the Charcoal Circle based on neck height
        self.neck_visual_tweaks = {
            0.3: 0,    # Hole
            1.15: 7,   # Post
            1.9: 12,   # Flow/Slant
            2.7: 27,   # Plumber
            3.9: 46    # Long
        }


        self.glass_gradient = ft.LinearGradient(
            begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1),
            colors=["#0078d4", "#005a9e"],
        )
       
        self.inactive_gradient = ft.LinearGradient(
            begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1),
            colors=["white", "white"],
        )


        # Origin in Pixels (Canvas center / Red Dot location)
        self.origin_x = 187.5
        self.origin_y = 150.0
       
        # USER DATA IN INCHES
        self.off_x = 0.00  
        self.off_y = -0.25  
        self.neck_height = 1.15
        self.head_type = "Blade"


        # Calculate initial pixel offsets so the image doesn't start at 0,0
        init_offsets = self.cg_offsets[self.head_type]
        init_left = -(init_offsets["left"] * self.INCH_TO_PX)
        init_top = -(init_offsets["top"] * self.INCH_TO_PX)

        self.toe_hang_text = ft.Text("TOE HANG: 0.0°", size=14, weight="bold", color="red", left=10, top=28)
        self.neck_height_text = ft.Text("Neck Height: 1.15\"", size=14, weight="bold", color="black", left=10, top=8)
        self.head_image = ft.Image(
            src=self.head_images[self.head_type], 
            width=375, 
            height=300, 
            fit="contain", 
            left=init_left, 
            top=init_top
        )
       
        self.offset_def = ft.Text("Offset (X): Horizontal CG distance", size=12, italic=True, color="gray")
        self.depth_def = ft.Text("Depth (Y): Vertical CG distance", size=12, italic=True, color="gray")


        # Red CG Dot
        self.target_dot = ft.Container(width=10, height=10, bgcolor="red", border_radius=5, left=self.origin_x - 5, top=self.origin_y - 5)
       


       
       
        self.shadow_circle = ft.Container(
            width=24, height=24, bgcolor="#f3b200", border_radius=12, opacity=0.3, left=0, top=0
        )
       
        self.charcoal_circle = ft.Container(
            width=24.25, height=24.25,
            bgcolor="#343a40",
            border_radius=12.125,
            border=ft.border.all(1, "white"),
            left=0, top=0,
            opacity=0.7
        )
       
# The connection lines - strictly using the 'cv' format
        self.line   = cv.Line(0, 0, 0, 0, paint=ft.Paint(stroke_width=2, color="red"))
        self.line_h = cv.Line(0, 0, 0, 0, paint=ft.Paint(stroke_width=2, color="Blue"))
        self.line_v = cv.Line(0, 0, 0, 0, paint=ft.Paint(stroke_width=2, color="Blue"))
       


        def create_selector_bar(options, current_val, callback):
            items = []
            for i, opt in enumerate(options):
                if i > 0:
                    items.append(ft.Container(width=1, bgcolor="#ced4da", height=24))
                label, val = opt if isinstance(opt, tuple) else (opt, opt)
                is_active = (val == current_val)
                item = ft.Container(
                    content=ft.Text(label, size=11, color="white" if is_active else "black", weight="bold"),
                    alignment=ft.Alignment(0, 0), height=24, expand=True,
                    gradient=self.glass_gradient if is_active else self.inactive_gradient,
                    on_click=lambda e, v=val: callback(v), data=val
                )
                items.append(item)
            return ft.Container(
                content=ft.Row(items, spacing=0), border=ft.border.all(1, "#ced4da"),
                border_radius=4, clip_behavior=ft.ClipBehavior.ANTI_ALIAS, width=360, height=24
            )


        self.head_bar = create_selector_bar(list(self.head_images.keys()), self.head_type, self.set_head)
        self.neck_bar = create_selector_bar([("Hole", 0.3), ("Post", 1.15), ("Flow/Slant", 1.9), ("Plumber", 2.7), ("Long", 3.9)], self.neck_height, self.set_height)


        ft.Column([
                    self.offset_def,
                    self.depth_def
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),


       
        self.green_gradient = ft.LinearGradient(
            begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1),
            colors=["#0078d4", "#005a9e"],
        )


    # --- 1. INITIALIZE ATTRIBUTES FIRST ---
        self.in_x = None
        self.in_y = None

        # --- 2. DEFINE REUSABLE INPUT ROW ---
        def create_input_row(val, icon_minus, icon_plus, btn_gradient, axis):
            txt = ft.TextField(
                value=f"{val:.2f}", width=80, height=28, text_size=14, color="#ffffff",
                bgcolor="#343a40", border_radius=4, border_width=0,
                content_padding=ft.padding.only(top=0, bottom=11),
                text_align=ft.TextAlign.CENTER,
                on_change=lambda e: self.handle_input(e, axis)
            )
            btn_minus = ft.Container(
                content=ft.Icon(icon_minus, color="white", size=18),
                gradient=btn_gradient, width=28, height=28, border_radius=4,
                on_click=lambda _: self.step(axis, -0.05)
            )
            btn_plus = ft.Container(
                content=ft.Icon(icon_plus, color="white", size=18),
                gradient=btn_gradient, width=28, height=28, border_radius=4,
                on_click=lambda _: self.step(axis, 0.05)
            )
            return ft.Row([btn_minus, txt, btn_plus], spacing=3), txt

        # --- 3. ASSIGN THE ROWS (Now safe from AttributeErrors) ---
        # Note: We pass abs(self.off_y) to the UI so the user sees a positive number
        self.row_x, self.in_x = create_input_row(self.off_x, ft.Icons.KEYBOARD_ARROW_UP, ft.Icons.KEYBOARD_ARROW_DOWN, self.green_gradient, "x")
        self.row_y, self.in_y = create_input_row(abs(self.off_y), ft.Icons.KEYBOARD_ARROW_LEFT, ft.Icons.KEYBOARD_ARROW_RIGHT, self.glass_gradient, "y")



       
        self.canvas = ft.GestureDetector(
            on_tap_down=self.on_canvas_click,
            content=ft.Container(
                content=ft.Stack([
                    self.head_image,
                    ft.canvas.Canvas([
                        self.line,  
                        self.line_h,
                        self.line_v  
                    ], width=375, height=300),
                    self.shadow_circle,
                    self.target_dot,
                    self.charcoal_circle,
                    self.toe_hang_text,
                    self.neck_height_text,  
                ]),
                width=375, height=300, bgcolor="white", border=ft.border.all(3, "black"), border_radius=8,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS
            )
        )
       
        self.content = ft.Column([
            ft.Column([self.head_bar, self.neck_bar], spacing=4),
            self.canvas,        
           
            ft.Row([
                ft.Text("CG to Shaft axis (In)", size=10, weight="bold", color="black", width=140, text_align="center"),
                ft.Text("Shaft axis to Face (In)", size=10, weight="bold", color="black", width=140, text_align="center"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
           
            ft.Row([self.row_x, self.row_y], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
       


    def did_mount(self):
        self.sync()
        self.update()


    def set_height(self, val):
        self.neck_height = val
        for item in self.neck_bar.content.controls:
            if isinstance(item, ft.Container) and hasattr(item, "data") and item.data is not None:
                is_active = (item.data == val)
                item.gradient = self.glass_gradient if is_active else self.inactive_gradient
                item.content.color = "white" if is_active else "black"
        self.sync()


    def set_head(self, label):
        self.head_type = label
        self.head_image.src = self.head_images.get(label, "blade.png")
# Shift the image (left and top) to align the new model's CG with the fixed Red Dot
        offsets = self.cg_offsets[label]
        self.benchmark_y = offsets["left"]
        self.head_image.left = -(offsets["left"] * self.INCH_TO_PX)
        self.head_image.top  = -(offsets["top"]  * self.INCH_TO_PX) # New vertical shift
        for item in self.head_bar.content.controls:
            if isinstance(item, ft.Container) and hasattr(item, "data") and item.data is not None:
                is_active = (item.data == label)
                item.gradient = self.glass_gradient if is_active else self.inactive_gradient
                item.content.color = "white" if is_active else "black"
                
        self.sync()


    def on_canvas_click(self, e: ft.TapEvent):
        
        # 2. Calculate raw inches directly from the click relative to origin
        # Note: Vertical mouse movement usually maps to your 'X' (CG Depth/Offset) 
        # and Horizontal maps to your 'Y' (Shaft Axis) based on your existing code.
        raw_x_inch = (e.local_position.y - self.origin_y) / self.INCH_TO_PX
        raw_y_inch = (e.local_position.x - self.origin_x) / self.INCH_TO_PX
        
        self.off_x = raw_x_inch
        
        # Apply your bounds logic
        max_left = self.cg_offsets[self.head_type]["left"] + 0.74
        self.off_y = max(-max_left, min(0, raw_y_inch))
        
        # Update text fields
        self.in_x.value = f"{self.off_x:.2f}"
        face_offset = self.off_y + self.benchmark_y
        self.in_y.value = f"{face_offset:.2f}"
        
        # DEBUG PRINT
        print(f"CLICK POSITION -> X: {self.off_x:.3f} in, Y: {abs(self.off_y):.3f} in")
        
        self.sync()


    def step(self, axis, amount):
        try:
            if axis == "x":
                self.off_x += amount
            elif axis == "y":
                # Changing the logic to move relative to the face
                # This ensures the plus/minus buttons move the shaft intuitively
                self.off_y += amount 
            self.sync()
        except Exception as e:
            print(f"Step Error: {e}")

    def handle_input(self, e, axis):
        if not self.in_x or not self.in_y:
            return
        try:
            if axis == "x":
                self.off_x = float(self.in_x.value)
            elif axis == "y":
                # Calculate the internal Y gap by adding the input to the DNA offset
                # If DNA is 0.40 and input is -0.25, off_y becomes -0.15 (correct for physics)
                user_offset = float(self.in_y.value)
                dna_left = self.cg_offsets[self.head_type]["left"]
                self.off_y = -(dna_left + user_offset)
            self.sync()
        except ValueError:
            pass



       


    def sync(self):
        LIE_ANGLE = 70
        self.neck_height_text.value = f"TIP HEIGHT: {self.neck_height:.2f}\""
        
        tweak = self.neck_visual_tweaks.get(round(self.neck_height, 2), 0)
        
        # 1. Strictly bound the values
        # This keeps the shaft on the "player side" of the CG (X >= 0)
        self.off_x = max(0.0, self.off_x) 
        
        # Keep your existing Y bounds
        max_left = self.cg_offsets[self.head_type]["left"] + 0.74
        self.off_y = max(-max_left, min(0, self.off_y))

        # 2. Update UI text boxes ONLY to show current state
        self.in_x.value = f"{self.off_x:.2f}"
        face_offset = self.off_y + self.benchmark_y
        self.in_y.value = f"{face_offset:.2f}"

        
        # 4. Pixel Mapping
        x_px = self.off_x * self.INCH_TO_PX
        y_px = self.off_y * self.INCH_TO_PX

        # Circles
        self.charcoal_circle.top = (self.origin_y + x_px + tweak) - 12.125
        self.charcoal_circle.left = (self.origin_x + y_px) - 12.125
        self.shadow_circle.top = (self.origin_y + x_px) - 12
        self.shadow_circle.left = (self.origin_x + y_px) - 12

        # Lines and Toe Hang
        vertical_comp = max(0, self.off_x) * math.sin(math.radians(LIE_ANGLE))
        toe_hang_rad = math.atan2(vertical_comp, -self.off_y)
        self.toe_hang_text.value = f"TOE HANG: {math.degrees(toe_hang_rad):.1f}°"
        
        sc_x, sc_y = self.shadow_circle.left + 12, self.shadow_circle.top + 12
        self.line.x1, self.line.y1 = self.origin_x, self.origin_y
        self.line.x2, self.line.y2 = sc_x, sc_y
        self.line_h.x1, self.line_h.y1 = self.origin_x, self.origin_y
        self.line_h.x2, self.line_h.y2 = sc_x, self.origin_y
        self.line_v.x1, self.line_v.y1 = sc_x, self.origin_y
        self.line_v.x2, self.line_v.y2 = sc_x, sc_y

        self.canvas.content.content.controls[1].update()
        if self.page: self.page.update()
        if self.on_change: self.on_change(None)