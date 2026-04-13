import math
import result_3_1
import result_11


def calculate_result_1(physics_vars):
    """RESULT 1: Total system mass using physics_init outputs"""
    shaft_mass_g = physics_vars["shaft_mass_g"]
    total_system_mass_g = physics_vars["total_system_mass_kg"] * 1000.0
    total_system_mass_oz = total_system_mass_g / 28.34952
    
    return {
        "result_1_total_system_mass_g": total_system_mass_g,
        "result_1_total_system_mass_oz": total_system_mass_oz
    }


def calculate_result_1_1(physics_vars, source_vars):
    """SUB-RESULT 1.1: Fulcrum from SOLE PLATE = 0" (head-local reference frame)"""
    benchmark_head_vcg = source_vars["current_benchmark_z"]
    grip_length = source_vars["grip_length"]
    assembled_length = source_vars["assembled_length"]
    
    shaft_mass = physics_vars["shaft_mass_g"]
    total_system_mass = physics_vars["total_system_mass_kg"] * 1000.0
    neck_height = physics_vars["neck_height_mm"] / 25.4 
    
    effective_shaft_length = assembled_length - neck_height
    
    d_h = benchmark_head_vcg
    d_s = neck_height + (effective_shaft_length / 2)
    d_g = assembled_length - (grip_length / 2)
    
    x_fulcrum = ((source_vars["head_mass"] * d_h) + (shaft_mass * d_s) + (source_vars["grip_mass"] * d_g)) / total_system_mass
    
    return {
        "result_1_1_x_fulcrum": x_fulcrum,
        "result_1_1_d_h": d_h,
        "result_1_1_d_s": d_s,
        "result_1_1_d_g": d_g
    }


def calculate_result_3_1(cg_x, benchmark_y, benchmark_z, shaft_displacement, toe_hang_deg):
    theta = math.radians(toe_hang_deg)
    y_static = benchmark_y + shaft_displacement
    rel_x = cg_x * math.cos(theta) - y_static * math.sin(theta)
    rel_y = cg_x * math.sin(theta) + y_static * math.cos(theta)
    rel_z = benchmark_z
    return rel_x, rel_y, rel_z


def calculate_result_3_6(head_mass_g, shaft_mass_g, grip_mass_g, 
                             rel_x, rel_y, rel_z, shaft_radius=0.015):
    m_h = head_mass_g / 1000.0
    m_s = shaft_mass_g / 1000.0  
    m_g = grip_mass_g / 1000.0
    
    r_head_sq = (rel_x * 0.0254)**2 + (rel_y * 0.0254)**2 + (rel_z * 0.0254)**2
    i_head_shaft = m_h * r_head_sq
    
    i_shaft_own = 0.5 * m_s * (shaft_radius**2) 
    i_grip_shaft = 0.5 * m_g * (0.02)**2        
    
    return i_head_shaft + i_shaft_own + i_grip_shaft


def calculate_result_3_5(v_head_m_s, r_pivot_mm):
    """RESULT 3.5: System Angular Velocity"""
    if r_pivot_mm <= 0:
        return {"result_3_5_omega_instant": 0.0, "result_3_5_omega_smoothed": 0.0}
    
    # Radius convert mm -> meters
    r_pivot_m = r_pivot_mm / 1000.0
        
    # Omega (rad/s) = Linear Velocity / Radius
    omega_instant = v_head_m_s / r_pivot_m
    
    # 2:1 stroke ratio smoothing (0.5 multiplier)
    omega_smoothed = 0.5 * omega_instant
    
    return {
        "result_3_5_omega_instant": omega_instant,
        "result_3_5_omega_smoothed": omega_smoothed
    }


def calculate_result_3_3(head_mass_g, shaft_mass_g, grip_mass_g, rel_x, rel_y, fulcrum_z):
    # Use raw grams to determine the system CG ratio (cleaner)
    total_mass_g = head_mass_g + shaft_mass_g + grip_mass_g
    
    # System CG (weighted average)
    sys_x = (head_mass_g * rel_x) / total_mass_g
    sys_y = (head_mass_g * rel_y) / total_mass_g
    
    # Return coordinates + the total mass in ounces for Result 1 compatibility
    total_mass_oz = total_mass_g / 28.34952
    return sys_x, sys_y, fulcrum_z, total_mass_oz


def calculate_result_2(total_system_mass_oz, x_fulcrum, assembled_length):
    # Convert sole-plate fulcrum -> grip-end reference
    x_fulcrum_grip_ref = assembled_length - x_fulcrum
    
    pivot_distance = 14.0
    lever_arm = abs(x_fulcrum_grip_ref - pivot_distance)

    torque_oz_in = total_system_mass_oz * lever_arm

    sw_points = (torque_oz_in - -31.0) / 7.0

    sw_letters = ["A", "B", "C", "D", "E", "F", "G"]
    letter_index = max(0, min(6, int((sw_points // 10))))
    sw_letter = sw_letters[letter_index]
    sw_number = round(max(0, sw_points % 10), 1)

    return f"{sw_letter}-{sw_number}"


import math

def calculate_result_3_7(source_vars, rel_x, rel_y, rel_z, user_v_m_s, shaft_moi):
    # 1. MASS MAPPING (Preserved from your init file)
    head_mass_kg = source_vars["head_mass"] / 1000.0
    # Scaling shaft mass by length relative to 38" standard
    shaft_mass_kg = (source_vars["raw_shaft_mass"] * (source_vars["assembled_length"] / 38.0)) / 1000.0
    grip_mass_kg = source_vars["grip_mass"] / 1000.0

    # 2. RADIUS CONVERSIONS (Preserved)
    r_3d_shaft_head_m = math.sqrt(rel_x**2 + rel_y**2 + rel_z**2) * 0.0254
    r_twist_m = math.sqrt(rel_x**2 + rel_y**2) * 0.0254 
    
    r_3d_shaft_shaft_m = 0.0
    r_3d_shaft_grip_m = 0.0
    g = 9.81

    # 3. STROKE DYNAMICS & ACCELERATION (Updated for Peak Torque)
    effective_stroke_radius_m = 0.75 
    omega_rads = user_v_m_s / effective_stroke_radius_m
    
    # 2:1 Ratio Timing: Forward stroke is 1/3 of the 2s total
    forward_stroke_time_s = 0.67 
    
    # Calculate Peak Harmonic Acceleration (The 'spike' at transition)
    # This represents the sudden change from backstroke to forward stroke
    peak_accel_m_s2 = user_v_m_s * (math.pi / (2 * forward_stroke_time_s))

    # 4. TORQUE CALCULATIONS
    # A. Total gravity torque (Preserved)
    cos_lie = abs(math.cos(math.radians(source_vars["lie_angle"])))
    torque_gravity_total_nm = (
        head_mass_kg * g * cos_lie * r_3d_shaft_head_m +
        shaft_mass_kg * g * cos_lie * r_3d_shaft_shaft_m +
        grip_mass_kg * g * cos_lie * r_3d_shaft_grip_m
    )

    # B. Total centrifugal torque (Preserved)
    torque_centrifugal_total_nm = head_mass_kg * (omega_rads**2) * (r_twist_m**2)

    # C. NEW: Peak Inertial Torque (The Haptic Spike)
    # Force (m*a) acting on the twist lever arm (r_twist)
    torque_inertial_peak_nm = (head_mass_kg * peak_accel_m_s2) * r_twist_m

    # 5. TOTAL DYNAMIC TORQUE (Sum of all three components)
    total_dynamic_torque_nm = (
        torque_gravity_total_nm + 
        torque_centrifugal_total_nm + 
        torque_inertial_peak_nm
    )
    
    # 6. SMOOTHING FOR DISPLAY (Preserved)
    head_speed_m_s = source_vars["stroke_velocity"] * 0.3048
    omega_max = head_speed_m_s / 0.6 
    alpha_display = min(20.0, omega_max / forward_stroke_time_s)

    return total_dynamic_torque_nm, alpha_display


def calculate_result_7(user_grip_force_lbf):
    
    return round(user_grip_force_lbf, 1)



def calculate_result_8_usage(
    torque_3_7_nm,         
    grip_dia_in,           
    grip_mu,               
    grip_f_lbf,            
    grip_position_offset_in,       
    hand_span_in,          
    assembled_len_in,      
    system_cg_z            
):
    hand_center_z = assembled_len_in - grip_position_offset_in - (hand_span_in / 2)
    
    leverage_delta = abs(hand_center_z - system_cg_z)
    torque_at_hands = (torque_3_7_nm * 8.85075) * leverage_delta

    r_in = grip_dia_in / 2
    grip_capacity = (grip_f_lbf * grip_mu) * r_in
    
    if grip_capacity <= 0:
        return 100.0
    
    usage_pct = (torque_at_hands / grip_capacity) * 100
    return round(usage_pct, 1)



def calculate_result_9_reserve(
    torque_3_7_nm,           
    grip_dia_in,             
    grip_mu,                 
    grip_f_lbf,              
    grip_position_offset,    
    hand_span_in,            
    assembled_length,        
    system_cg_z              
):
        
    hand_center_z = assembled_length - grip_position_offset - (hand_span_in / 2)
    leverage_delta = abs(hand_center_z - system_cg_z)
    
    torque_at_hands = (torque_3_7_nm * 8.85075) * leverage_delta
    
    r_in = grip_dia_in / 2
    f_required_lbf = torque_at_hands / (grip_mu * r_in)
    
    reserve_lbf = grip_f_lbf - f_required_lbf
    
    return round(reserve_lbf, 2)


def calculate_result_10_pti(
    res3_7_torque_nm, 
    shaft_moi, 
    user_v_m_s, 
    grip_dia_in, 
    grip_f_lbf, 
    grip_mu, 
    hand_span_in, 
    assembled_len_in, 
    grip_position_offset_in
):
    
    r_m = (grip_dia_in * 0.0254) / 2          
    f_grip_n = grip_f_lbf * 4.44822            

    control_gain = assembled_len_in / (assembled_len_in - grip_position_offset_in)
    player_cap_nm = (f_grip_n * grip_mu * r_m * (hand_span_in / 7.5)) * control_gain

    putter_demand_nm = res3_7_torque_nm + (shaft_moi * user_v_m_s * 0.01)
    
    pti_score_linear = max(0, 100 - (putter_demand_nm / player_cap_nm * 100))
    pti_score_linear = min(100, pti_score_linear)

    pti_ratio = player_cap_nm / putter_demand_nm
    pti_dB = 10 * math.log10(pti_ratio)

    return {
        "result_10_pti_linear": round(pti_score_linear, 1),
        "result_10_pti_db": round(pti_dB, 1),
        "player_cap_nm": round(player_cap_nm, 3),
        "putter_demand_nm": round(putter_demand_nm, 4)
    }


def calculate_result_11_sensory_zones(
    grip_force_lbf, hand_span_in, grip_pos_offset_in,
    grip_dia_in, grip_len_in, grip_mu, grip_mass_g):
    """
    Result 11: Sensory zones using baseline+modifiers model.
    Baseline anchored to hand/wrist torque perception literature.
    All 7 grip variables act as scaling factors around nominal setup.
    """
    
    # 1. BASELINE SENSORY ZONES (at nominal: 4 lbf, 0.9", 7.5" hands, etc.)
    baseline_zones = {
        "isolation_max": 0.025,           # Below reliable detection
        "passive_tracking_max": 0.060,    # Barely noticeable  
        "active_recruitment_min": 0.120,  # Noticeable/requires attention
        "unstable_load_min": 0.250        # Strong/high load
    }
    
    # 2. INDIVIDUAL MODIFIER FACTORS (each ~1.0 at nominal values)
    # Grip force: higher force = stiffer interface (raises thresholds)
    S_force = 1.0 + 0.20 * ((grip_force_lbf - 4.0) / 4.0)
    
    # Grip diameter: larger diameter changes torque handling
    S_diameter = 1.0 + 0.15 * ((grip_dia_in - 0.9) / 0.9)
    
    # Grip friction: higher friction reduces slip sensitivity
    S_friction = 1.0 + 0.10 * grip_mu
    
    # Grip mass: heavier grip adds rotational inertia
    S_mass = 1.0 + 0.05 * (grip_mass_g / 500.0)
    
    # Grip length: longer grip changes leverage (small effect)
    S_length = 1.0 + 0.03 * ((grip_len_in - 10.0) / 10.0)
    
    # Hand span: larger hands = better coupling (lowers thresholds slightly)
    S_hand = 1.0 - 0.10 * ((hand_span_in - 7.5) / 7.5)
    
    # Grip position offset: choking down = shorter lever (lowers thresholds)
    S_offset = 1.0 - 0.08 * grip_pos_offset_in
    
    # 3. COMPOSITE SCALING FACTOR
    S_total = S_force * S_diameter * S_friction * S_mass * S_length * S_hand * S_offset
    
    # 4. SCALED ZONE BOUNDARIES (clamped 0-0.6 Nm for chart)
    zones = {}
    for zone_key, base_value in baseline_zones.items():
        scaled_value = base_value * S_total
        zones[f"result_11_{zone_key}"] = round(max(0.0, min(0.6, scaled_value)), 4)
    
    # 5. WEBER JND MAGNITUDE (~15% Weber fraction at baseline)
    jnd_magnitude = round(0.025 * S_total * 0.15, 4)
    zones["result_11_jnd_magnitude"] = jnd_magnitude
    
    return zones



  
def initialize_physics(source_vars):  
    # Scale raw shaft mass (L9) by the cut length (L8)
    shaft_mass_g = source_vars["raw_shaft_mass"] * (source_vars["assembled_length"] / 38.0) 
    # Single Source of Truth for System Mass (in kg for SI physics)
    total_system_mass_kg = (source_vars["head_mass"] + shaft_mass_g + source_vars["grip_mass"]) / 1000.0
    # Neck Height (L10) to mm/m for pivot calculation
    neck_height_mm = source_vars["neck_height"] * 25.4
    # Stroke Velocity (L17) from FPS to Meters per Second
    user_v_m_s = source_vars["stroke_velocity"] * 0.3048
    # Fulcrum Point (The point where the shaft enters the head)
    fulcrum_point_z = neck_height_mm








    # --- SYSTEM MASS (Result 1) ---
    physics_vars_for_res1 = {
        "shaft_mass_g": shaft_mass_g,
        "total_system_mass_kg": total_system_mass_kg
    }
    res1 = calculate_result_1(physics_vars_for_res1)

    # --- FULCRUM / BALANCE POINT (Result 1.1) ---
    physics_vars_for_res1["neck_height_mm"] = neck_height_mm
    res1_1 = calculate_result_1_1(physics_vars_for_res1, source_vars)

    # --- RELATIVE CG OFFSETS (Result 3.1) ---
    # We need the FRESH toe hang from your external math script
    
    math_output = result_3_1.run_result_3_1(dict(source_vars))
    
    # Extract the fresh values
    fresh_toe_hang = math_output["toe_hang"]
    rel_x = math_output["offsets"][0]
    rel_y = math_output["offsets"][1]
    rel_z = math_output["offsets"][2]
    

    # --- MOI (Result 3.6) ---
    shaft_moi = calculate_result_3_6(
        source_vars["head_mass"],
        shaft_mass_g, 
        source_vars["grip_mass"],
        rel_x, rel_y, rel_z
    )
 
    # --- SYSTEM ANGULAR VELOCITY (Result 3.5) ---
    head_cg_radius_mm = math.sqrt(rel_x**2 + rel_y**2 + rel_z**2) * 25.4
    
    res3_5 = calculate_result_3_5(user_v_m_s, head_cg_radius_mm)


    # --- 5. SYSTEM CG VECTORIZATION (Result 3.3) ---
    sys_x, sys_y, sys_z, total_system_mass_oz = calculate_result_3_3(
        source_vars["head_mass"],
        shaft_mass_g,
        source_vars["grip_mass"],
        rel_x,
        rel_y,
        res1_1["result_1_1_x_fulcrum"]
    )

    # --- 6. SWING WEIGHT (Result 2) ---
    res2_swing_weight = calculate_result_2(
        total_system_mass_oz,
        res1_1["result_1_1_x_fulcrum"],
        source_vars["assembled_length"]
    )

    # --- 7. DYNAMIC TORQUE (Result 3.7) ---
    res3_7_torque_nm, res3_7_alpha = calculate_result_3_7(
        source_vars, 
        rel_x, 
        rel_y, 
        rel_z, 
        user_v_m_s, 
        shaft_moi
    )

    # --- 8. GRIP FORCE (Result 7) ---
    grip_force_processed = calculate_result_7(source_vars["grip_force"])


    # --- 9. FORCE USAGE % (Result 8) ---
    res8_usage_pct = calculate_result_8_usage(
        torque_3_7_nm=res3_7_torque_nm,
        grip_dia_in=source_vars["grip_diameter"],
        grip_mu=source_vars["grip_friction"],
        grip_f_lbf=source_vars["grip_force"],
        grip_position_offset_in=source_vars["grip_position_offset"], 
        hand_span_in=source_vars["hand_span"],            
        assembled_len_in=source_vars["assembled_length"],     
        system_cg_z=sys_z                                
    )


# --- 10. GRIP RESERVE (Result 9) ---
    res9_reserve_lbf = calculate_result_9_reserve(
        torque_3_7_nm=res3_7_torque_nm,
        grip_dia_in=source_vars["grip_diameter"],
        grip_mu=source_vars["grip_friction"],
        grip_f_lbf=source_vars["grip_force"],
        grip_position_offset=source_vars["grip_position_offset"],
        hand_span_in=source_vars["hand_span"],
        assembled_length=source_vars["assembled_length"],
        system_cg_z=sys_z
    )


# --- 11. PLAYER TORQUE INDEX (Result 10) ---
    res10 = calculate_result_10_pti(
        res3_7_torque_nm=res3_7_torque_nm,
        shaft_moi=shaft_moi,
        user_v_m_s=user_v_m_s,
        grip_dia_in=source_vars["grip_diameter"],
        grip_f_lbf=source_vars["grip_force"],
        grip_mu=source_vars["grip_friction"],
        hand_span_in=source_vars["hand_span"],
        assembled_len_in=source_vars["assembled_length"],
        grip_position_offset_in=source_vars["grip_position_offset"]
    )


# --- 12. SENSORY ZONES (Result 11) ---
    result_11 = calculate_result_11_sensory_zones(
    source_vars["grip_force"],
    source_vars["hand_span"],
    source_vars["grip_position_offset"],
    source_vars["grip_diameter"],
    source_vars["grip_length"],
    source_vars["grip_friction"],
    source_vars["grip_mass"]
)


    return {
        "shaft_mass_g": shaft_mass_g,
        "total_system_mass_kg": total_system_mass_kg,
        "total_system_mass_oz": total_system_mass_oz,
        "neck_height_mm": neck_height_mm,
        "user_v_m_s": user_v_m_s,
        "fulcrum_point_z": fulcrum_point_z,
        "result_1_total_system_mass_g": res1["result_1_total_system_mass_g"],
        "result_1_total_system_mass_oz": total_system_mass_oz,
        "result_1_1_x_fulcrum": res1_1["result_1_1_x_fulcrum"],
        "result_3_5_omega_smoothed": res3_5["result_3_5_omega_smoothed"],
        "result_2_swing_weight": res2_swing_weight,
        "result_3_3_sys_x": sys_x,
        "result_3_3_sys_y": sys_y,
        "result_3_3_sys_z": sys_z,
        "rel_x": rel_x,
        "rel_y": rel_y,
        "rel_z": rel_z,
        "shaft_moi": shaft_moi,
        "result_3_7_total_dynamic_torque_nm": res3_7_torque_nm, 
        "result_3_7_alpha_display": res3_7_alpha,
        "result_7_grip_force_value": grip_force_processed,
        "result_8_usage_pct": res8_usage_pct,
        "result_9_grip_reserve_lbf": res9_reserve_lbf,
        "result_10_pti_linear": res10["result_10_pti_linear"],
        "result_10_pti_db": res10["result_10_pti_db"],
        "player_cap_nm": res10["player_cap_nm"],
        "putter_demand_nm": res10["putter_demand_nm"],
        "result_11_isolation_max": result_11["result_11_isolation_max"],
        "result_11_passive_tracking_max": result_11["result_11_passive_tracking_max"],
        "result_11_active_recruitment_min": result_11["result_11_active_recruitment_min"],
        "result_11_unstable_load_min": result_11["result_11_unstable_load_min"],
        "result_11_jnd_magnitude": result_11["result_11_jnd_magnitude"],
        
        

    }