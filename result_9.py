# --- RESULT 9: GRIP RESERVE (LBF) ---

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


res_9 = calculate_result_9_reserve(
    torque_3_7_nm=res3_7_torque_nm,
    grip_dia_in=source_vars["grip_diameter"],
    grip_mu=source_vars["grip_friction"],
    grip_f_lbf=grip_force_processed,
    grip_position_offset=source_vars["grip_position_offset"],
    hand_span_in=source_vars["hand_span"],
    assembled_length=source_vars["assembled_length"],
    system_cg_z=sys_z
)

