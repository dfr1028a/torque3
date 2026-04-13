# --- RESULT 2: SWING WEIGHT ---

def calculate_swing_weight(total_system_mass_oz, x_fulcrum, assembled_length):
    # Convert sole-plate fulcrum → grip-end reference for swingweight
    x_fulcrum_grip_ref = assembled_length - x_fulcrum
    
    # 14" pivot from GRIP END (industry standard)
    pivot_distance = 14.0
    lever_arm = abs(x_fulcrum_grip_ref - pivot_distance)

    # 2. Calculate Torque in ounce-inches
    torque_oz_in = total_system_mass_oz * lever_arm

    # 3. Convert to Swing Weight Points (Standard Lorythmic Scale)
    sw_points = (torque_oz_in - -31.0) / 7.0

    # 4. Alphanumeric Translation Logic
    sw_letters = ["A", "B", "C", "D", "E", "F", "G"]
    letter_index = max(0, min(6, int((sw_points // 10))))
    sw_letter = sw_letters[letter_index]
    sw_number = round(max(0, sw_points % 10), 1)

    # Final Result Output
    final_swing_weight = f"{sw_letter}-{sw_number}"
    print(f"Swing Weight: {final_swing_weight}")
    return final_swing_weight
