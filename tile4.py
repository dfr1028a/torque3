import math
import flet as ft
import flet.canvas as cv

class Tile4(ft.Container):
    def __init__(self, **kwargs):
        # Pass all arguments (left, top, height=350) to the base Container
        super().__init__(**kwargs)
        
        # We removed self.height = 350 so it takes the height from main.py
        self.width = 400
        self.bgcolor = "white"
        self.border_radius = 8
        self.padding = 20
        # Prevents internal content from stretching the container
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE 

        # UI Elements
        self.title = ft.Text(
            "ROTATION PROFILE", 
            size=14, weight="bold", color="black"
        )

        # --- Graph Paths (Floor set to 100) ---
        self.path = cv.Path(
            [cv.Path.MoveTo(0, 100), cv.Path.LineTo(360, 10)], 
            paint=ft.Paint(stroke_width=3, color="white", style=ft.PaintingStyle.STROKE)
        )
        self.fill_path = cv.Path(
            [cv.Path.MoveTo(0, 100), cv.Path.LineTo(360, 10), cv.Path.LineTo(360, 100), cv.Path.Close()],
            paint=ft.Paint(color="#004e92", style=ft.PaintingStyle.FILL)
        )

        # Vertical indicator bar - sitting ON the line
        self.plotted_point = ft.Container(
            width=5, 
            height=20, 
            bgcolor="white", 
            border_radius=1, 
            left=175, 
            top=25  # Dash bottom ends at 37, matching line bottom
        )

        # Horizontal White Baseline
        self.slider_baseline = ft.Container(
            width=335,
            height=2,
            bgcolor="white",
            left=0,
            top=35, 
        )

        # Assembly
        self.content = ft.Column(
            controls=[
                # Title
                ft.Container(
                    content=self.title, 
                    alignment=ft.Alignment(0, 0),
                    margin=ft.margin.only(top=-10, bottom=10)
                ),
                
                # Grouping graph and track
                ft.Column(
                    controls=[
                        # Graph Canvas
                        ft.Container(
                            content=cv.Canvas([self.fill_path, self.path], width=360, height=100),
                            height=100, 
                            width=360
                        ),
                        
                        # Black track/slider
                        ft.Container(
                            height=50, 
                            width=360, 
                            bgcolor="#000000",
                            border=ft.border.all(1, "#ffffff"), 
                            border_radius=5,
                            padding=ft.padding.only(left=10, right=5),
                            content=ft.Stack([
                                # Layer 1: Text Labels
                                ft.Row(
                                    [
                                        ft.Text("LINEAR", size=10, color="#FFFFFF"),
                                        ft.Text("LATE MOMENTUM", size=10, color="#FFFFFF"),
                                    ], 
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                                    width=335, 
                                    top=2
                                ),
                                # Layer 2: The Horizontal Line
                                self.slider_baseline,
                                # Layer 3: The Vertical Indicator
                                self.plotted_point
                            ])
                        ),
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            alignment=ft.MainAxisAlignment.START # Sticks everything to the top
        )


    def update_from_physics(self, rel_x, rel_y, toe_hang):
    # 1. The X-Offset is our primary "Rotation Driver"
    # If this is 0, momentum_factor will be 0.
        momentum_factor = abs(rel_x) / 1.5
    
    # 2. The Y-Offset acts as a "Stabilizer"
    # It reduces the momentum_factor. The deeper the head (Y), 
    # the harder it is for the X-offset to rotate it.
        stability_reduction = (abs(rel_y) * 0.15) 
    
    # 3. Apply the gate: If X is 0, the whole thing stays 0.
    # We use max(0, ...) to ensure stability doesn't create "negative" momentum.
        rotation_tendency = max(0, momentum_factor - stability_reduction)

    # 4. Add Toe Hang influence, but ONLY if there is an X-offset 
    # (Or keep it very small so it doesn't "jump" a face-balanced putter)
        hang_influence = (abs(toe_hang) / 90.0) * rotation_tendency
    
    # 5. Calculate Final Position
    # 0.0 is the far left (LINEAR)
        sync_factor = rotation_tendency + hang_influence
    
    # 6. Final Clamp
    # Now, if X=0 and Y=0, sync_factor will be 0.0 (Far Left)
        sync_factor = max(0.0, min(1.0, sync_factor))

        self.update_profile(profile_pct=sync_factor, curve_intensity=sync_factor)





    def update_profile(self, profile_pct, curve_intensity):
        # 0.0 = Far Left | 1.0 = Far Right
        self.plotted_point.left = float(profile_pct) * 335
        
        # Adjust curve depth (cp_y)
        cp_y = 55 + (float(curve_intensity) * 40)
        
        self.path.elements = [
            cv.Path.MoveTo(0, 100), 
            cv.Path.QuadraticTo(180, cp_y, 360, 10)
        ]
        self.fill_path.elements = [
            cv.Path.MoveTo(0, 100), 
            cv.Path.QuadraticTo(180, cp_y, 360, 10), 
            cv.Path.LineTo(360, 100), 
            cv.Path.Close()
        ]
        self.update()