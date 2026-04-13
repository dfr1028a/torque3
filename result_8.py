# --- RESULT 8: FORCE USAGE (%) ---

def calculate_result_8_usage(
    torque_3_7_nm,         # Result 3.7 (Raw Head Torque)
    grip_dia_in,           # Line 12
    grip_mu,               # Line 13
    grip_f_lbf,            # Line 14
    g_pos_offset_in,       # Line 16 (Offset from top)
    hand_span_in,          # Line 15
    assembled_len_in,      # Line 8
    system_cg_z            # Result 3.3 (Vertical Balance Point)
):
        
    hand_center_z = assembled_len_in - g_pos_offset_in - (hand_span_in / 2)
    leverage_delta = abs(hand_center_z - system_cg_z)
    torque_at_hands = (torque_3_7_nm * 8.85075) * leverage_delta

    r_in = grip_dia_in / 2
    grip_capacity = (grip_f_lbf * grip_mu) * r_in
    
    
    if grip_capacity <= 0:
        usage_pct = 100.0
    else:
        
        usage_pct = (torque_at_hands / grip_capacity) * 100
        
    return {
        "force_usage_pct": round(usage_pct, 1),
        "stability_status": "Stable" if usage_pct < 70 else "At Risk" if usage_pct < 100 else "Slipping",
        "leverage_arm_in": round(leverage_delta, 2) # Added for debugging/transparency
    }

# Execution
res_8 = calculate_result_8_usage(
    source_engine.physics_results["result_3_7_torque"], # Assuming it's in the results dict
    source_engine.grip_diameter,
    source_engine.grip_friction,
    source_engine.grip_force,
    source_engine.grip_position_offset,
    source_engine.hand_span,
    source_engine.assembled_length,
    source_engine.physics_results["result_3_3_sys_z"] 
)