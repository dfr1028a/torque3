import math
import physics_init
import importlib

# The underlying data array mapping Style IDs to specific Coordinate Keys
cg_benchmarks = {
    "Blade": {"y": 0.40, "z": 0.55},
    "Wide Blade":        {"y": 0.60, "z": 0.45},
    "Mid Mallet":        {"y": 0.80, "z": 0.40},
    "MOI Mallet":       {"y": 1.20, "z": 0.35},
}

# Line 5: Select the profile and pull the corresponding benchmarks
style_id = "Blade"
current_benchmark_y = cg_benchmarks[style_id]["y"]
current_benchmark_z = cg_benchmarks[style_id]["z"]

# Line 1: Mass of the putter head in grams. (Range: 315.0 - 400.0)
head_mass = 350.0
head_mass = max(315.0, min(head_mass, 400.0))

# Line 4: CG lateral position (Fixed at 0.0 for Center of Face).
cg_x = 0.0

# Line 19: Vertical displacement from Center of Face (0.0) to Shaft Axis.
# Axis: X (Vertical). Range: 0.0 to 2.0. Default: 0.0.
shaft_x_offset = 0.0
shaft_x_offset = max(0.0, min(shaft_x_offset, 2.0))

# Line 2: Displacement from Face Plane (0.0) to Shaft Axis.
# Axis: Y (Depth). Range: Dynamic (-current_benchmark_y to 0.74).
shaft_displacement = 0.25
shaft_displacement = max(-current_benchmark_y, min(shaft_displacement, 0.74))
total_y_gap = shaft_displacement + current_benchmark_y

# Line 3: Static gravity-induced rotation (Static Horizontal Shaft Balance).
# Range: 0 (Face Balanced) to 90 (Full Toe Hang).
toe_hang = 0.0
toe_hang = max(0.0, min(toe_hang, 90.0))

# Line 10: Z height distance from the ground (Z 0.0) to the start of the shaft position in inches. 
# Range: 0.3 (Bored Hole), 1.15 (Post), 1.9 (Flow/Slant), 2.7 (Standard Plumber), 3.9 (Long Neck). Default: 1.15.
neck_height = 1.15
neck_height = max(0.3, min(neck_height, 3.9))

# Line 6: The angle in the ZX plane (toward and away from the player at address) relative to vertical.
# Range: 63.0 (Flat) to 79.0 (Upright). Default: 70.0.
lie_angle = 70.0
lie_angle = max(63.0, min(lie_angle, 79.0))

# Line 7: The angle in the ZY plane (side to side tilt) relative to vertical.
# Range: -2.0 (Backward Lean) to 2.0 (Forward Press). Default: 0.0.
shaft_lean = 0.0
shaft_lean = max(-2.0, min(shaft_lean, 2.0))

# Line 8: Total length from the sole to the end of the grip.
# Range: 30.0 (Short) to 40.0 (Long). Default: 34.0.
assembled_length = 34.0
assembled_length = max(30.0, min(assembled_length, 40.0))

# Raw shaft starting length constant for density calculations
RAW_SHAFT_LENGTH = 38.0

# Line 9: Weight of the uncut 38.0" shaft in grams before assembly (used for density).
# Range: 90.0 (Light) to 150.0 (Heavy). Default: 120.0.
raw_shaft_mass = 120.0
raw_shaft_mass = max(90.0, min(raw_shaft_mass, 150.0))

# Line 11: Mass of the grip in grams (used for total assembly mass and counter-balance calculations).
# Range: 50.0 (Light) to 150.0 (Counter-Core). Default: 60.0.
grip_mass = 60.0
grip_mass = max(50.0, min(grip_mass, 150.0))

# Line 12: Thickness (diameter) of the grip in inches.
# Range: 0.9 (Standard) to 1.7 (Thick). Default: 0.9.
grip_diameter = 0.9
grip_diameter = max(0.9, min(grip_diameter, 1.7))

# Line 13: Surface friction coefficient (mu) of the grip material.
# Range: 0.85 (Rubber), 1.25 (Polyurethane). Default: 0.85.
grip_friction = 0.85
grip_friction = max(0.85, min(grip_friction, 1.25))

# Line 14: Total clamping force of the player's hands in Pounds-force (lbf).
# Range: 1.2 (Feather Light) to 12.0 (Firm). Default: 5.0.
grip_force = 5.0
grip_force = max(1.2, min(grip_force, 12.0))

# Line 15: The vertical length of the grip occupied by the player's hands in inches.
# Presets: 9.0 (10-Finger/Split), 7.5 (Standard Overlap), 5.5 (Close/Interlock).
# Range: 5.5 to 9.0. Default: 7.5.
hand_span = 7.5
hand_span = max(5.5, min(hand_span, 9.0))

# Line 16: The distance from the top of the grip to the top of the player's Hand Span in inches.
# Range: 0.0 (Flush with top) to 5.0 (Choked down significantly). Default: 0.1.
grip_position_offset = 0.1
grip_position_offset = max(0.0, min(grip_position_offset, 5.0))

# Line 17: Speed of the putter head in feet per second (fps).
# Range: 1.0 (Slow) to 10.0 (Fast). Default: 4.4.
stroke_velocity = 4.4
stroke_velocity = max(1.0, min(stroke_velocity, 10.0))

# Line 18: Grip length in inches.
# Options: 10.0 (Standard), 16.0 (Counter-balance). Default: 10.0.
grip_length = 10.0
grip_length = max(10.0, min(grip_length, 16.0))




# Create source_engine object and assign all your variables
source_engine = type('SourceEngine', (object,), {})()
source_engine.cg_x = cg_x
source_engine.shaft_x_offset = shaft_x_offset
source_engine.current_benchmark_y = current_benchmark_y
source_engine.cg_benchmarks = cg_benchmarks
source_engine.shaft_displacement = shaft_displacement
source_engine.toe_hang_deg = toe_hang
source_engine.current_benchmark_z = current_benchmark_z
source_engine.head_mass = head_mass
source_engine.raw_shaft_mass = raw_shaft_mass
source_engine.assembled_length = assembled_length
source_engine.grip_mass = grip_mass
source_engine.grip_length = grip_length
source_engine.neck_height = neck_height
source_engine.stroke_velocity = stroke_velocity
source_engine.grip_force = grip_force
source_engine.lie_angle = lie_angle
source_engine.shaft_lean = shaft_lean
source_engine.grip_diameter = grip_diameter
source_engine.grip_friction = grip_friction
source_engine.hand_span = hand_span
source_engine.grip_position_offset = grip_position_offset
source_engine.style_id = style_id


# --- THE TRIGGER FUNCTION ---

def calculate():
    
    benchmarks = cg_benchmarks.get(source_engine.style_id, {"y": 0.40, "z": 0.55})
    source_engine.current_benchmark_y = benchmarks["y"]
    source_engine.current_benchmark_z = benchmarks["z"]
    source_engine.physics_results = physics_init.initialize_physics(vars(source_engine))
    

    current_snapshot = vars(source_engine)
    
    import result_3_1
    math_output = result_3_1.run_result_3_1(current_snapshot)
    
    source_engine.cg_offsets = {
        "x": math_output["offsets"][0], 
        "y": math_output["offsets"][1], 
        "z": math_output["offsets"][2]
    }
    
    source_engine.toe_hang_deg = math_output["toe_hang"]
    source_engine.physics_vars = source_engine.physics_results
    source_engine.shaft_moi = source_engine.physics_results.get("shaft_moi", 0.0)

    import result_3_7
    torque_results = result_3_7.run_result_3_7(current_snapshot, source_engine.physics_results)

    # Pull the values from result_3_7 into the engine
    source_engine.total_dynamic_torque_nm = torque_results["total_dynamic_torque_nm"]
    source_engine.alpha_display = torque_results["alpha_display"]

# 2. ATTACH the function to the object (Do this BEFORE calling it)
source_engine.calculate = calculate

# 3. FINAL STARTUP EXECUTION
# Initialize physics first so calculate() has data to work with
initial_vars = vars(source_engine)
source_engine.physics_results = physics_init.initialize_physics(initial_vars)

# Now call the function - it will exist now
source_engine.calculate()

