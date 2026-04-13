# --- SUB-RESULT 3.3: SYSTEM CG VECTORIZATION ---

def project_head_cg_to_system_cg(head_mass, shaft_mass, grip_mass, rel_x, rel_y, fulcrum_z):
    """
    Calculate total system CG using direct moment balance physics.
    
    Formula: sys_x = (head_mass * head_cg_x + shaft_mass * 0 + grip_mass * 0) / total_mass
    
    Assumptions:
    - Shaft + Grip CG lies on the shaft axis at (0, 0).
    - Longitudinal balance (Z) is already solved via the fulcrum calculation.
    
    Safety:
    - Validates masses to prevent division by zero.
    """
    
    # 1. Edge Case Guard: Division by zero
    total_mass = head_mass + shaft_mass + grip_mass
    if total_mass <= 0:
        raise ValueError("Total mass must be greater than zero.")
    
    # 2. Direct Moment Balance (No Scaling)
    # Shaft/grip contribute 0 to X/Y moments since they're on shaft axis
    sys_x = (head_mass * rel_x + shaft_mass * 0 + grip_mass * 0) / total_mass
    sys_y = (head_mass * rel_y + shaft_mass * 0 + grip_mass * 0) / total_mass
    
    # 3. Final System Vector
    return sys_x, sys_y, fulcrum_z

# Execution for Sub-Result 3.3
shaft_mass_g = source_vars["shaft_mass"]  # From your source_vars
grip_mass_g = source_vars["grip_mass"]    # From your source_vars

# 1. Source data (your exact 4 inputs from source_engine)
current_benchmark_y = source_vars["current_benchmark_y"]  # 0.30 from cg_benchmarks  
shaft_displacement = source_vars["shaft_displacement"]    # Y offset from head CG
toe_hang = source_vars["toe_hang"]                       # 0-90° angle
cg_x = 0.0                                              # Head CG center

print("DEBUG current_benchmark_y:", current_benchmark_y)
print("DEBUG shaft_displacement:", shaft_displacement)
print("DEBUG toe_hang:", toe_hang)

# 2. Total Y gap between shaft axis and CG (YOUR formula)
total_y_gap = shaft_displacement + current_benchmark_y
print("DEBUG total_y_gap:", total_y_gap)


# 3. VALID: Formula A (Rotation Matrix)
theta = math.radians(toe_hang)
rel_x = cg_x * math.cos(theta) - total_y_gap * math.sin(theta)
rel_y = cg_x * math.sin(theta) + total_y_gap * math.cos(theta)

print(f"rel_x: {rel_x:.3f}, rel_y: {rel_y:.3f}")


sys_x, sys_y, sys_z = project_head_cg_to_system_cg(
    source_vars["head_mass"],
    shaft_mass_g,
    source_vars["grip_mass"],
    rel_x,
    rel_y,
    res1_1["result_1_1_x_fulcrum"]
)
print(f"System CG: X={sys_x:.3f}, Y={sys_y:.3f}, Z={sys_z:.3f}")
