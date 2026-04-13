# -------------------------------------------------------------------
# 12. RESULT 11: SENSORY ZONES (WEBER'S LAW) ---
# -------------------------------------------------------------------


def calculate_result_11_sensory_zones(
    grip_force,             # From Line 14
    hand_span,              # From Line 15
    grip_position_offset,   # From Line 16
    grip_diameter,          # From Line 12
    grip_length,            # From Line 18
    grip_friction,          # From Line 13
    grip_mass               # From Line 11
):
    """
    RESULT 11: SENSORY ZONES
    Baseline perceptual zones scaled by 7 grip variables.
    Baseline chosen to match hand/wrist torque perception literature.
    """
    
    # 1. BASELINE SENSORY ZONES (at nominal grip: 4 lbf, 0.9", etc.)
    # These are approximate hand/wrist torque perception thresholds
    baseline_zones = {
        "isolation_max": 0.025,           # Below reliable detection
        "passive_tracking_max": 0.060,    # Barely noticeable
        "active_recruitment_min": 0.120,  # Noticeable / requires attention
        "unstable_load_min": 0.250        # Strong / high load
    }
    
    # 2. MODIFIER FACTORS (each ~1.0 for nominal values)
    # Grip force: higher force stiffens interface (raises thresholds)
    S_force = 1.0 + 0.20 * ((grip_force - 4.0) / 4.0)
    
    # Grip diameter: larger diameter changes torque handling (modest effect)
    S_diameter = 1.0 + 0.15 * ((grip_diameter - 0.9) / 0.9)
    
    # Grip friction: higher friction reduces slip sensitivity (raises thresholds)
    S_friction = 1.0 + 0.10 * grip_friction
    
    # Grip mass: heavier grip adds rotational inertia (raises thresholds)
    S_mass = 1.0 + 0.05 * (grip_mass / 500.0)
    
    # Grip length: longer grip changes leverage (small effect)
    S_length = 1.0 + 0.03 * ((grip_length - 10.0) / 10.0)
    
    # Hand span: larger hands may have different coupling (lowers thresholds)
    S_hand = 1.0 - 0.10 * ((hand_span - 7.5) / 7.5)
    
    # Grip position offset: choking down changes lever arm (lowers thresholds)
    S_offset = 1.0 - 0.08 * grip_position_offset
    
    # 3. COMPOSITE SCALING FACTOR
    S_total = S_force * S_diameter * S_friction * S_mass * S_length * S_hand * S_offset



    # 4. CLAMPED ZONE BOUNDARIES (0 to 0.6 Nm chart range)
    zones = {}
    for key, base_value in baseline_zones.items():
        scaled = base_value * S_total
        zones[f"result_11_{key}"] = max(0.0, min(0.6, round(scaled, 4)))
    
    # 5. WEBER'S LAW JND (scaled from baseline origin)
    jnd_magnitude = round(0.025 * S_total * 0.15, 4)  # ~15% Weber fraction
    zones["result_11_jnd_magnitude"] = jnd_magnitude
    



    return zones