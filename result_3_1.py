import math


# --- SUB-RESULT 3.1: RELATIVE CG COORDINATES ---

def calculate_local_cg_offsets(cg_x, benchmark_y, benchmark_z, shaft_disp, toe_hang_deg):
    """
    Locates the Center of Gravity relative to the shaft axis center (0,0,0).
    
    Units/Conventions:
    - All distances (cg_x, benchmark_y/z, shaft_disp) - All distances (cg_x, benchmark_y/z, shaft_disp) are ALWAYS IN INCHES.
    - toe_hang_deg: Putter's natural hang angle in DEGREES (0 = Face Balanced).
    - Local Frame: +X is Toe, +Y is Back (Depth), +Z is Down Shaft.
    """
    
    # 1. Convert hang angle to radians for math.sin/cos
    theta = math.radians(toe_hang_deg)

    # 2. Establish the total static lever arm (Depth)
    # Distance from shaft center to CG depth before rotation
    y_static = shaft_disp

    # 3. Apply 2D Rotation around the Shaft (Z-Axis)
    # This transforms the face-centered benchmarks into shaft-centered relative coordinates
    rel_x = cg_x * math.cos(theta) - y_static * math.sin(theta)
    rel_y = cg_x * math.sin(theta) + y_static * math.cos(theta)
    rel_z = benchmark_z

    return rel_x, rel_y, rel_z

def run_result_3_1(source_vars):
    # --- SANITIZE INPUTS FIRST (The Firewall) ---
    shaft_x  = float(source_vars["shaft_x_offset"])
    cg_x_val = float(source_vars["cg_x"])
    bench_y  = float(source_vars["current_benchmark_y"])
    bench_z  = float(source_vars["current_benchmark_z"])
    shaft_d  = float(source_vars["shaft_displacement"])

    # 1. FIX POLARITY: Use sanitized floats
    total_x_dist = shaft_x - cg_x_val

    # 2. Get the coordinates using sanitized floats
    rel_x, rel_y, rel_z = calculate_local_cg_offsets(
        total_x_dist,
        bench_y, 
        bench_z,
        shaft_d,
        0.0 
    )

    

    # 3. Apply the 70-degree Lie Angle Projection
    LIE_ANGLE = float(source_vars["lie_angle"])
    vertical_comp = rel_x * math.sin(math.radians(LIE_ANGLE))

    # 4. Calculate the Toe Hang angle
    # We use abs(rel_y) here if you want the angle calculation to treat 'Down' as positive
    toe_hang = math.degrees(math.atan2(vertical_comp, abs(rel_y)))

    return {
        "offsets": (rel_x, rel_y, rel_z),
        "toe_hang": toe_hang,
        "lever_arm": math.sqrt(rel_x**2 + rel_y**2)
    }
