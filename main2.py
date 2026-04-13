import flet as ft
import flet.canvas as cv
from tile1 import Tile1
from tile2 import Tile2
from tile3 import Tile3
from tile4 import Tile4 
from tile5 import Tile5
import source_engine

def main(page: ft.Page):
    page.title = "Putter Engine v2 - Orchestrator"
    page.bgcolor = "#1a1a1a"
    
    # Initialize the brain logic
    engine = source_engine.source_engine

    # 1. Create UI Instances
    t1 = Tile1(left=0, top=0)
    t2 = Tile2(left=305, top=0)
    t3 = Tile3(left=710, top=0)
    # 1. Create the path object
    curve_path = cv.Path(
        [cv.Path.MoveTo(0, 360)], 
        paint=ft.Paint(color="#ff0000", stroke_width=2, style=ft.PaintingStyle.STROKE)
    )
    # 2. Insert it into Tile 3's chart (Index 3 keeps it behind the dot)
    t3.chart_frame.controls.insert(3, cv.Canvas([curve_path], width=360, height=360))
    t4 = Tile4(left=305, top=450, height=220)
    t5 = Tile5(left=710, top=450)

    # 2. INITIAL HANDSHAKE (Engine -> UI)
    t1.ui_refs["head_w"].value = str(int(engine.head_mass))
    t1.ui_refs["lie_angle"].value = str(int(engine.lie_angle))
    t1.ui_refs["len"].value = f"{engine.assembled_length:.2f}"
    t1.ui_refs["g_w"].value = str(int(engine.grip_mass))
    
    def on_ui_change(e):
        try:
            
            
            
            # --- PUSH UI INPUTS TO ENGINE ---
            engine.head_mass = float(t1.ui_refs["head_w"].value or 350)
            engine.lie_angle = float(t1.ui_refs["lie_angle"].value or 70)
            engine.shaft_lean = float(t1.ui_refs["lean"].value or 0.0)
            engine.assembled_length = float(t1.ui_refs["len"].value or 34)
            engine.raw_shaft_mass = float(t1.ui_refs["u_shaft_w"].value or 120)
            engine.grip_mass = float(t1.ui_refs["g_w"].value or 60)
            engine.grip_diameter = float(t1.ui_refs["g_dia"].value or 0.9)
            engine.grip_length = float(t1.ui_refs["g_len"].value or 10.0)
            engine.grip_friction = float(t1.ui_refs["g_mat"].value or 0.85)
            engine.grip_force = float(t1.ui_refs["g_force"].value or 5.0)
            engine.hand_span = float(t1.ui_refs["g_span"].value or 7.5)
            engine.grip_position_offset = float(t1.ui_refs["g_choke"].value or 0.1)
            engine.stroke_velocity = float(t1.ui_refs["v"].value or 4.4)

            
            
            # --- TILE 2 (Canvas) DATA ---
            engine.neck_height = t2.neck_height
            engine.shaft_x_offset = round(t2.off_x, 4)
            engine.shaft_displacement = abs(round(t2.off_y, 4))
            engine.style_id = str(t2.head_type)

            # --- THE TRIGGER ---
            engine.calculate()
            res = engine.physics_results  # This is the dictionary from physics_init



            # 3. UNIFIED VERIFICATION DUMP (The Only Allowed Print)
            print("\n" + "═"*60)
            print(f" SYSTEM SYNC | Style: {engine.style_id.upper()}")
            print("─"*60)
            print(f" MASS    | Total: {res.get('result_1_total_system_mass_g', 0):.1f}g ({res.get('result_1_total_system_mass_oz', 0):.2f}oz)")
            print(f" OFFSETS | X: {res.get('rel_x', 0):.3f} | Y: {res.get('rel_y', 0):.3f} | Z: {res.get('rel_z', 0):.3f}")
            print(f" BALANCE | SW: {res.get('result_2_swing_weight', 'N/A')} | Fulcrum: {res.get('result_1_1_x_fulcrum', 0):.2f}\"")
            print(f" DYNAMIC | Torque: {res.get('result_3_7_total_dynamic_torque_nm', 0):.4f} Nm | PTI: {res.get('result_10_pti_linear', 0)}%")
            print(f" PLAYER  | Grip Usage: {res.get('result_8_usage_pct', 0)}% | Reserve: {res.get('result_9_grip_reserve_lbf', 0)} lbs")
            print("═"*60)

            # Update Tile 2 Labels
            t2.in_x.value = f"{engine.shaft_x_offset:.2f}"
            t2.in_y.value = f"{(engine.shaft_displacement - engine.current_benchmark_y):.2f}"

            # Update Tile 4 (CG Visualization)
            t4.update_from_physics(
                rel_x=engine.cg_offsets.get('x', 0.0),
                rel_y=engine.cg_offsets.get('y', 0.0),
                toe_hang=engine.toe_hang_deg
            )

            

            # --- SYNC DOT AND ZONES TO TILE 3 ---
            # 1. Calculate Dot Position (must match the curve scaling)
            v_input = engine.stroke_velocity
            t_input = engine.physics_results.get("result_3_7_total_dynamic_torque_nm", 0.0)

            # Map to the 360px grid (Velocity starts at 1.0)
            f_x = ((v_input - 1.0) * 40) - 7
            f_y = (360 - (t_input * 1440)) - 7




            # 2. Push all data to Tile3 (including the color zones from physics)
            t3.update_data(
    r_h=engine.physics_results.get("result_11_unstable_load_min", 0.25),    
    g_h=engine.physics_results.get("result_11_active_recruitment_min", 0.12),  
    b_h=engine.physics_results.get("result_11_passive_tracking_max", 0.06),      
    y_h=engine.physics_results.get("result_11_isolation_max", 0.025),         
    d_x=f_x, 
    d_y=f_y
)
            
            
            
            # --- SYNC TILE 5 (STI & PTI) ---
            t5.update_sti_visuals(
    torque_nm=res.get("result_3_7_total_dynamic_torque_nm", 0.0),
    isolation_max=res.get("result_11_isolation_max", 0.025),
    pti_linear=res.get("result_10_pti_linear", 0.0)
)

        except Exception:
            import traceback
            traceback.print_exc()
        
        page.update()

    # 4. Connect Event Listeners
    for key, control in t1.ui_refs.items():
        # This ensures we catch TextFields, Dropdowns, and Sliders
        if isinstance(control, (ft.TextField, ft.Dropdown, ft.Slider, ft.Text)):
            control.on_change = on_ui_change

    t2.on_change = on_ui_change

    # 5. Layout and Startup
    main_container = ft.Container(
        content=ft.Stack(controls=[t1, t2, t3, t4, t5], width=1350, height=850),
        bgcolor="#2a2d36", padding=5, border_radius=8, expand=True
    )

    # Boot the engine once to fill initial state
    engine.calculate()
    page.add(main_container)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)