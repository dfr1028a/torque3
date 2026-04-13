import flet as ft

def main(page: ft.Page):
    page.title = "Lab UI - 5px Tight Grid"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000" 
    page.padding = 0
    
    page.window_width = 1600
    page.window_height = 950

    def create_tile(number, w, h, x, y, color="#1c1f26"):
        return ft.Container(
            content=ft.Text(str(number), color="white", size=30, weight="bold"),
            width=w, height=h, left=x, top=y,
            bgcolor=color, border_radius=8, # Slightly smaller radius for tighter gaps
            alignment=ft.Alignment(0, 0), 
        )

    # --- THE SYMMETRICAL CANVAS (5px Gutters) ---
    layout_stack = ft.Container(
        content=ft.Stack(
            controls=[
                # Tile 1: Sidebar
                create_tile(1, 300, 850, 0, 0, color="#11131a"),
                
                # Tile 2: Top Left (Chart)
                # x = Sidebar(300) + Gutter(5) = 305
                create_tile(2, 400, 420, 305, 0),
                
                # Tiles 3-6: The 2x2 Grid
                # x = Chart(305+400) + Gutter(5) = 710
                create_tile(3, 140, 207, 710, 0),
                create_tile(4, 140, 207, 855, 0), # 710 + 140 + 5
                create_tile(5, 140, 207, 710, 212), # 0 + 207 + 5
                create_tile(6, 140, 207, 855, 212),
                
                # Tile 7: Far Right (Profile)
                # x = Grid(855+140) + Gutter(5) = 1000
                create_tile(7, 250, 420, 1000, 0, color="#252833"),

                # Tile 8: Mega Bottom Tile
                # x = 305 (Aligns with Chart), y = 425 (Chart 420 + 5)
                # Width = 400 + 5 + 140 + 5 + 140 + 5 + 250 = 945
                # Height = 850 - 425 = 425
                create_tile(8, 945, 425, 305, 425),
            ],
            width=1250, # Recalculated total content width
            height=850, # Total content height
        ),
        bgcolor="#2a2d36", 
        padding=5,         # Uniform 5px frame
        border_radius=8,
    )

    page.add(
        ft.Container(
            content=layout_stack,
            alignment=ft.Alignment(0, 0),
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)