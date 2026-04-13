import flet as ft
import flet.canvas as cv

class Tile3(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.width = 640 
        self.height = 445
        self.bgcolor = "white"
        self.border = ft.border.all(1, "#ffffff")
        self.border_radius = 8
        self.padding = 0 

        # --- 1. Background Zones (Canvas Rectangles) ---
        # We define them here; their actual size/position is handled in update_data
        self.rect_red = cv.Rect(x=0, y=0, width=360, height=360, paint=ft.Paint(color="#c20010"))
        self.rect_orange = cv.Rect(x=0, y=0, width=360, height=0, paint=ft.Paint(color="#fc8f00"))
        self.rect_yellow = cv.Rect(x=0, y=0, width=360, height=0, paint=ft.Paint(color="#fbff00"))
        self.rect_white = cv.Rect(x=0, y=0, width=360, height=0, paint=ft.Paint(color="#ffffff"))

        # --- 2. The Vector Line (Consolidated into the same Canvas) ---
        self.line_shape = cv.Line(
            x1=0, y1=360,
            x2=0, y2=360,  # Initialize at the same point as x1/y1
            paint=ft.Paint(color="red", stroke_width=4)
        )

        # ONE Canvas to rule them all (Red is first/bottom, Line is last/top)
        self.main_canvas = cv.Canvas(
            shapes=[
                self.rect_red,
                self.rect_orange,
                self.rect_yellow,
                self.rect_white,
                self.line_shape
            ],
            width=360,
            height=360
        )

        # --- 2. The Plotted Dot ---
        self.dot = ft.Container(
            width=14, height=14,
            bgcolor="black",
            border_radius=7,
            border=ft.border.all(2, "white"),
            left=150, top=250,
        )

        # --- 3. Assemble the Chart Frame ---
        self.chart_frame = ft.Stack([
            # 1. The Single Canvas (Background + Line)
            self.main_canvas,

            # 2. Grid Lines (Horizontal) - Positioned ABOVE the canvas
            ft.Container(
                content=ft.Column([
                    ft.Container(width=360, height=1, bgcolor="black", opacity=0.1) 
                    for _ in range(11)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                width=360, height=360,
            ),

            # 3. Grid Lines (Vertical)
            ft.Container(
                content=ft.Row([
                    ft.Container(width=1, height=360, bgcolor="black", opacity=0.1) 
                    for _ in range(8)
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=0),
                width=360, height=360,
            ),

            # 4. The Dot
            self.dot,
        ], width=360, height=360)

        # --- 4. Sidebar --- (UNTOUCHED)
        self.definition_title = ft.Text("PASSIVE TRACKING", size=13, weight="bold", color="#ffffff")
        self.definition_header = ft.Container(
            content=self.definition_title,
            bgcolor="black",
            padding=ft.padding.symmetric(vertical=8),
            alignment=ft.Alignment(0, 0), 
            width=180,
            border_radius=ft.border_radius.only(top_left=8, top_right=8)
        )
        self.definition_body = ft.Text(
            "Torque is at the Just Noticeable Difference (JND) threshold. The stimulus is physically present but remains stable via passive friction, avoiding the need for conscious corrective interference.",
            size=11, color="black", weight="bold", width=160 
        )

        self.torque_widget = ft.Column(
            controls=[
                ft.Text("SENSORY ZONE", size=18, weight="bold", color="black"),
                ft.Row([ft.Text("56%", size=24, weight="bold", color="black")], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(content=ft.ProgressBar(value=0.30, color="black", bgcolor="#c5c5c5", height=8), width=160, margin=ft.margin.only(bottom=16)),
                ft.Container(
                    content=ft.Column([self.definition_header, ft.Container(content=self.definition_body, padding=10)], spacing=0),
                    border=ft.border.all(1, "#eeeeee"), border_radius=8, bgcolor="#f9f9f9", width=180
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=180,
        )

        # --- 6. Final Layout --- (UNTOUCHED)
        self.content = ft.Stack([
            ft.Container(content=ft.Text("Dynamic Torque (Nm)", weight="bold", color="black", size=14, no_wrap=True), rotate=ft.Rotate(angle=-1.5708), left=-125, top=185, width=300, alignment=ft.Alignment(0, 0)),
            ft.Container(
                content=ft.Column([
                    ft.Container(content=ft.Text(t, size=12, color="black", weight="bold"), height=36, alignment=ft.Alignment(1, 0))
                    for t in [".25", ".22", ".20", ".17", ".15", ".12", ".10", ".07", ".05", ".02", ".00"]
                ], spacing=0), 
                left=10, top=2, width=50, height=400),
            
            ft.Container(content=self.chart_frame, left=70, top=20, border=ft.border.all(1, "#444444")),
            ft.Container(content=ft.Row([ft.Container(content=ft.Text(str(i), size=12, color="black", weight="bold"), width=40, alignment=ft.Alignment(0, 0)) for i in range(2, 10)], spacing=0, alignment=ft.MainAxisAlignment.START), left=90, top=385, width=320),
            ft.Container(content=ft.Text("Stroke Velocity (Fps)", weight="bold", color="black", size=14), left=190, top=410),
            ft.Container(content=self.torque_widget, top=60, left=445, width=180, height=380)
        ], width=640, height=445)


        self.zone_definitions = {
            "white": {
                "title": "ISOLATION",
                "color": "#ffffff",
                "body": "Any torque present is below the sensory threshold. Because there is insufficient data recognized, the nervous system lacks the feedback necessary to initiate a motor response, leading to a state of neurological isolation where the stroke remains undisturbed by rotational forces."
            },
            "yellow": {
                "title": "JND",
                "color": "#fffb18",
                "body": "Torque has reached the JND (just noticeable difference) threshold. It is detectable to the nervous system, but remains within the limits of passive control. The stroke is still governed by natural stabilization rather than active corrective response."
            },
            "orange": {
                "title": "AWARE",
                "color": "#fc8f00",
                "body": "Torque has reached a level where the nervous system clearly recognizes the rotational stimulus as distinct from baseline, but the influence on stroke pattern remains subtle. Minor conscious correction may become available while passive control is still partially effective."
            },
            "red": {
                "title": "INFLUENTIAL",
                "color": "#c20010",
                "body": "Torque has reached a level where the nervous system registers it as a significant influence on stroke dynamics, consistently directing rotational tendencies. The stimulus now meaningfully governs face alignment."
            }
        }

    def update_data(self, r_h, g_h, b_h, y_h, d_x, d_y):
        print(f"ZONE DATA -> White: {y_h:.4f} | Yellow: {b_h:.4f} | Orange: {g_h:.4f}")
        # 1. SCALE: Map 0.25 Nm to the full 360px height (360 / 0.25 = 1440)
        # Ensure this block is indented exactly like this.
        scale = 1440 
        
        # Convert pixel position back to Nm (0.25 is the top of the chart)
        current_torque = 0.25 - (d_y / scale)

        # Determine zone by checking if we have CLEARED the floor of each tier
        # This prevents the label from 'jumping the gun' when sitting on the line
        if current_torque > g_h:
            zone = "red"
        elif current_torque > b_h:
            zone = "orange"
        elif current_torque > y_h:
            zone = "yellow"
        else:
            zone = "white"


        # 1. Update the sidebar text using the dictionary
        data = self.zone_definitions[zone]
        self.definition_title.value = data["title"]
        self.definition_title.color = data["color"]
        self.definition_body.value = data["body"]
        
        # 2. Calculate local percentage within the current zone
        # We align the floor of one zone with the ceiling of the previous one
        floors = {
            "white": 0, 
            "yellow": y_h, 
            "orange": b_h, 
            "red": g_h
        }
        ceilings = {
            "white": y_h, 
            "yellow": b_h, 
            "orange": g_h, 
            "red": 0.25
        }
        
        floor = floors[zone]
        ceiling = ceilings[zone]
        zone_span = ceiling - floor
        
        # Calculate depth into the zone: (Current - Bottom) / Total Zone Height
        if zone_span > 0:
            local_pct = (current_torque - floor) / zone_span
        else:
            local_pct = 0
            
        local_pct = max(0, min(1, local_pct)) # Clamp to 0-100% range

        # 3. Update the Percentage Text and Progress Bar
        self.torque_widget.controls[1].controls[0].value = f"{int(local_pct * 100)}%"
        self.torque_widget.controls[2].content.value = local_pct

        # 2. CALCULATE ABSOLUTE CEILINGS (Distance from the bottom)
        # We multiply the Nm value by the scale to get pixel height.
        w_top = y_h * scale  
        y_top = b_h * scale  
        o_top = g_h * scale  

        # 3. REBUILD SHAPES
        # We start drawing from the 'top' (360 - height) down to the bottom.
        # This forces the zones to "grow up" the screen as values increase.
        self.main_canvas.shapes = [
            # RED: Background (The whole box)
            cv.Rect(x=0, y=0, width=360, height=360, 
                    paint=ft.Paint(color="#c20010")),
            
            # ORANGE: From its top down to the bottom
            cv.Rect(x=0, y=max(0, 360 - o_top), width=360, 
                    height=o_top, paint=ft.Paint(color="#fc8f00")),
            
            # YELLOW: From its top down to the bottom
            cv.Rect(x=0, y=max(0, 360 - y_top), width=360, 
                    height=y_top, paint=ft.Paint(color="#fbff00")),
            
            # WHITE: From its top down to the bottom
            cv.Rect(x=0, y=max(0, 360 - w_top), width=360, 
                    height=w_top, paint=ft.Paint(color="#ffffff")),
            
            
        ]

        # Update the dot position
        self.dot.left = d_x
        self.dot.top = d_y
        self.update()