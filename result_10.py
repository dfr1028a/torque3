# --- RESULT 10: PLAYER TORQUE INDEX (PTI) ---


r_m = (source_vars["grip_diameter"] * 0.0254) / 2          
f_grip_n = grip_force_processed * 4.44822             


control_gain = source_vars["assembled_length"] / (source_vars["assembled_length"] - source_vars["grip_position_offset"])
player_cap_nm = (f_grip_n * source_vars["grip_friction"] * r_m * (source_vars["hand_span"] / 7.5)) 


putter_demand_nm = res3_7_torque_nm + (shaft_moi * user_v_m_s * 0.01)


pti_score_linear = max(0, 100 - (putter_demand_nm / player_cap_nm * 100))
pti_score_linear = min(100, pti_score_linear)


pti_ratio = player_cap_nm / putter_demand_nm
pti_dB = 10 * math.log10(pti_ratio)


result_10_pti_linear = round(pti_score_linear, 1)
result_10_pti_db = round(pti_dB, 1)


res10_output = {
    "result_10_pti_linear": result_10_pti_linear,
    "result_10_pti_db": result_10_pti_db,
    "player_cap_nm": round(player_cap_nm, 3),
    "putter_demand_nm": round(putter_demand_nm, 4)
}