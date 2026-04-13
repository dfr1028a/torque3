import flet as ft
import asyncio
import sys
from tile1 import Tile1
from tile2 import Tile2
from tile3 import Tile3
from tile4 import Tile4  
from tile5 import Tile5

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    
    # 1. Initialize all tiles
    t1 = Tile1(left=0, top=0)
    t2 = Tile2(left=305, top=0)
    t3 = Tile3(left=710, top=0)
    
    # ADD THE HEIGHT HERE (e.g., 280 instead of the old 395)
    t4 = Tile4(left=305, top=450, height=220) 
    
    t5 = Tile5(left=710, top=450)

    layout_stack = ft.Container(
        content=ft.Stack(
            controls=[
                t1,
                t2,
                t3,
                t4, 
                t5  
            ],
            width=1350, 
            height=850,
        ),
        bgcolor="#2a2d36",
        padding=5,
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
    import time
    try:
        ft.app(main, view=ft.AppView.WEB_BROWSER, port=8551)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing application...")