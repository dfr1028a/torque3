import math

def run_result_3_7(snapshot, physics_vars):
    # --- [ORIGINAL LOGIC: MASSES & OFFSETS] ---
    head_mass_kg = float(snapshot.get("head_mass", 0)) / 1000.0
    shaft_mass_kg = float(snapshot.get("raw_shaft_mass", 0)) / 1000.0
    grip_mass_kg = float(snapshot.get("grip_mass", 0)) / 1000.0

    head_cg_x_offset_inches = float(snapshot.get("cg_offsets", {}).get("x", 0))
    head_cg_y_offset_inches = float(snapshot.get("cg_offsets", {}).get("y", 0))
    head_cg_z_offset_inches = float(snapshot.get("cg_offsets", {}).get("z", 0))

    shaft_moi = float(snapshot.get("shaft_moi", 0.0001))

    r_3d_shaft_head_inches = math.sqrt(
        head_cg_x_offset_inches**2 +
        head_cg_y_offset_inches**2 +
        head_cg_z_offset_inches**2
    )
    r_3d_shaft_head_m = r_3d_shaft_head_inches * 0.0254

    # Original Shaft and grip CG radii
    shaft_r_3d = 0.0
    grip_r_3d = 0.0
    r_3d_shaft_shaft_m = shaft_r_3d
    r_3d_shaft_grip_m = grip_r_3d

    g = 9.81
    lie_val = float(snapshot.get("lie_angle", 70))

    # --- [ORIGINAL LOGIC: VELOCITY & OMEGA] ---
    effective_stroke_radius_m = 0.7   
    omega_rads = physics_vars.get("user_v_m_s", 0) / effective_stroke_radius_m

    # --- [ORIGINAL LOGIC: 1. GRAVITY TORQUE] ---
    torque_gravity_total_nm = (
        head_mass_kg * g * abs(math.cos(math.radians(lie_val))) * r_3d_shaft_head_m +
        shaft_mass_kg * g * abs(math.cos(math.radians(lie_val))) * r_3d_shaft_shaft_m +
        grip_mass_kg * g * abs(math.cos(math.radians(lie_val))) * r_3d_shaft_grip_m
    )

    # --- [ORIGINAL LOGIC: 2. CENTRIFUGAL TORQUE] ---
    r_twist_m = math.sqrt(head_cg_x_offset_inches**2 + head_cg_y_offset_inches**2) * 0.0254 
    torque_centrifugal_total_nm = head_mass_kg * (omega_rads**2) * r_twist_m * r_twist_m

    # --- [NEW ADDITION: 3. INERTIAL PEAK TORQUE] ---
    # This addresses the JND gap. We use your 2:1 ratio (0.67s forward stroke) 
    # to find the peak acceleration at the start of the move.
    v_max_m_s = physics_vars.get("user_v_m_s", 0)
    forward_stroke_time_s = 0.67
    # Using Harmonic Peak Acceleration (pi/2 multiplier for pendulum motion)
    peak_accel_m_s2 = v_max_m_s * (math.pi / (2 * forward_stroke_time_s))
    torque_inertial_peak_nm = (head_mass_kg * peak_accel_m_s2) * r_twist_m

    # --- [FINAL CALCULATION: TOTAL PEAK DYNAMIC TORQUE] ---
    # We add the Inertial Spike to your existing Dynamic Torque
    total_dynamic_torque_nm = torque_gravity_total_nm + torque_centrifugal_total_nm + torque_inertial_peak_nm

    # --- [ORIGINAL LOGIC: ALPHA & SMOOTHING] ---
    # (Restored exactly as you had it for the display outputs)
    vel_val = float(snapshot.get("stroke_velocity", 0))
    head_speed_m_s = vel_val * 0.3048 
    omega_max = head_speed_m_s / 0.75 
    alpha_realistic = omega_max / forward_stroke_time_s
    alpha_display = min(20.0, alpha_realistic)

    return {
        "total_dynamic_torque_nm": total_dynamic_torque_nm,
        "alpha_display": alpha_display,
        "peak_inertial_component": torque_inertial_peak_nm # Added for your reference
    }