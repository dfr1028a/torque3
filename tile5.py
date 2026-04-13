import flet as ft

class Tile5(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # --- 1. DEFINE REFERENCES (Top Level) ---
        self.sti_circle_text = ft.Text("23", size=24, weight="bold", color="white")
        self.torque_val_text = ft.Text("0.073", size=28, weight="bold", color="black")
        self.torque_progress = ft.ProgressBar(value=0.30, color="#004e92", bgcolor="#A0A0A0", height=6)

        self.pti_circle_text = ft.Text("23", size=24, weight="bold", color="white")
        self.pti_player_label = ft.Text("87.7%", size=12, weight="bold", color="#000000")
        self.pti_putter_label = ft.Text("12.3%", size=12, weight="bold", color="#000000")
        
        self.pti_player_bar = ft.Container(
            bgcolor="#28a745", height=22, 
            border_radius=ft.border_radius.only(top_left=4, bottom_left=4)
        )
        self.pti_putter_bar = ft.Container(
            bgcolor="#004e92", height=22, 
            border_radius=ft.border_radius.only(top_right=4, bottom_right=4)
        )

        # Separate the Putter Label Container to avoid inline assignment errors
        self.pti_putter_label_container = ft.Container(content=self.pti_putter_label)

        # Layout Settings
        self.width = 640 
        self.height = 220 
        self.bgcolor = "white"
        self.border = ft.border.all(1, "#ffffff")
        self.border_radius = 8
        vertical_offset = 20   
        bar_width = 140        

        # --- Helpers ---
        def data_circle(val_ref, bg_color):
            return ft.Container(
                content=val_ref if isinstance(val_ref, ft.Control) else ft.Text(val_ref, size=24, weight="bold", color="white"),
                alignment=ft.Alignment(0, 0),
                width=70, height=70,
                bgcolor=bg_color,
                border=ft.border.all(2, "white"),
                border_radius=35,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=0, color="black") 
            )

        def vertical_bar(label_top, val_text, fill_percentage):
            bar_max_height = 100
            fill_height = bar_max_height * fill_percentage
            return ft.Column([
                ft.Text(label_top, size=10, weight="bold", color="black", text_align=ft.TextAlign.CENTER, width=60),
                ft.Text(val_text, size=12, weight="bold", color="black", text_align=ft.TextAlign.CENTER, width=60),
                ft.Container(
                    width=20, height=bar_max_height, bgcolor="#eeeeee", border_radius=3,
                    alignment=ft.Alignment(0, 1), 
                    content=ft.Container(width=20, height=fill_height, bgcolor="black", border_radius=3)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)

        self.connection_widget = ft.Column([
            ft.Text("PLAYER CONNECTION", size=14, weight="bold", color="black"),
            ft.Row([
                vertical_bar("TORQUE\nLOAD", "1.3 lbs", 0.15),
                vertical_bar("GRIP\nFORCE", "9.5 lbs", 0.65),
                vertical_bar("STABILITY\nRES.", "8.2 lbs", 0.55),
                vertical_bar("FORCE\nUSAGE", "13%", 0.25),
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

        # --- The Absolute Layout (Clean References Only) ---
        self.content = ft.Stack([
            # STI
            ft.Container(bgcolor="#004e92", width=100, height=45, left=20, top=25 + vertical_offset, border_radius=4),
            ft.Text("STI", size=28, weight="bold", color="white", left=35, top=25 + vertical_offset),
            ft.Container(content=data_circle(self.sti_circle_text, "#004e92"), left=90, top=9 + vertical_offset),
            ft.Text("DYNAMIC TORQUE", size=12, weight="bold", color="#000000", left=196, top=15 + vertical_offset),
            ft.Container(content=self.torque_val_text, left=196, top=30 + vertical_offset),
            ft.Text("Nm", size=12, weight="bold", color="black", left=278, top=42 + vertical_offset),
            ft.Container(content=self.torque_progress, width=bar_width, left=180, top=70 + vertical_offset),

            # PTI
            ft.Container(bgcolor="#28a745", width=100, height=45, left=20, top=114 + vertical_offset, border_radius=4),
            ft.Text("PTI", size=28, weight="bold", color="white", left=35, top=117 + vertical_offset),
            ft.Container(content=data_circle(self.pti_circle_text, "#28a745"), left=90, top=101 + vertical_offset),
            ft.Text("PLAYER vs PUTTER", size=12, weight="bold", color="black", left=196, top=99 + vertical_offset),
            
            self.pti_player_bar,
            self.pti_putter_bar,
            ft.Container(content=self.pti_player_label, left=180, top=152 + vertical_offset),
            self.pti_putter_label_container, # Clean reference

            # Right Side
            ft.Container(content=self.connection_widget, right=20, top=10, width=280, height=200)
        ], width=640, height=220)

        # Position Setup
        self.pti_player_bar.left = 180
        self.pti_player_bar.top = 125 + vertical_offset
        self.pti_player_bar.width = int(bar_width * 0.877)

        self.pti_putter_bar.left = 180 + int(bar_width * 0.877)
        self.pti_putter_bar.top = 125 + vertical_offset
        self.pti_putter_bar.width = bar_width - int(bar_width * 0.877)
        
        self.pti_putter_label_container.left = 180 + bar_width - 35
        self.pti_putter_label_container.top = 152 + vertical_offset

    def update_sti_visuals(self, torque_nm, isolation_max, pti_linear):
        # Update STI
        self.torque_val_text.value = f"{torque_nm:.3f}"
        self.torque_progress.value = min(1.0, torque_nm / 0.250)
        if isolation_max > 0:
            sti_display = (torque_nm / isolation_max) * 10
            self.sti_circle_text.value = str(int(sti_display))
        
        # Update PTI
        self.pti_circle_text.value = str(int(pti_linear))
        
        bar_w_total = 140
        p_w = int(bar_w_total * (pti_linear / 100))
        putt_w = bar_w_total - p_w
        
        self.pti_player_bar.width = p_w
        self.pti_putter_bar.width = putt_w
        self.pti_putter_bar.left = 180 + p_w
        
        self.pti_player_label.value = f"{pti_linear:.1f}%"
        self.pti_putter_label.value = f"{(100 - pti_linear):.1f}%"
        
        self.update()