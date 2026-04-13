# --- SUB-RESULT 3.5: SYSTEM ANGULAR VELOCITY ---

def calculate_system_angular_velocity(v_head, r_pivot_m):
    """
    Calculates the rotational speed of the entire assembly.
    
    Inputs:
    - v_head: Linear velocity of the putter head (m/s).
    - r_pivot_m: The radius from the pivot (grip) to the head CG (meters).
    """
    # Safety: Guard against zero length to prevent division by zero
    if r_pivot_m <= 0:
        raise ValueError("Pivot radius (r_pivot_m) must be greater than zero.")

    # Omega (rad/s) = Linear Velocity / Radius (instantaneous at impact)
    system_omega = v_head / r_pivot_m
    
    return system_omega


# --- 1. Compute head_cg_radius from RESULT 3.1 CG offsets ---
r_3d_head_in = math.sqrt(
    rel_x**2 + rel_y**2 + rel_z**2
)
head_cg_radius = r_3d_head_in * 25.4   # radius in mm


# --- 2. Convert stroke_velocity (fps) → m/s ---
ft_per_s_to_m_per_s = 0.3048
head_speed_m_s = stroke_velocity * ft_per_s_to_m_per_s   # 4.4 fps → ~1.34 m/s


# --- 3. Use the computed head_cg_radius and head_speed_m_s ---
omega_instant = calculate_system_angular_velocity(
    head_speed_m_s, 
    head_cg_radius / 1000.0   # convert mm → meters
)


# --- 4. 2:1 stroke ratio smoothing (2 units back, 1 unit through) ---
total_stroke_time_s = 2.0

# Smoothed angular velocity: average over a 2:1 ramp‑up profile
omega_smoothed = 0.5 * omega_instant   # 0 → omega_instant over stroke time


# --- 5. Print the smoothed, “2:1‑stroke” value ---
print(f"Result 3.5 System Angular Velocity: {omega_smoothed:.2f} rad/s")
