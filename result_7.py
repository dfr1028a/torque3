# --- RESULT 7: GRIP FORCE ---

def calculate_result_7(user_grip_force_lbf):
    """
    Reflects the user's input Grip Force and categorizes the tension level.
    Input Range (Line 14): 1.2 to 12.0 lbf.
    """
    # 1. Direct Reflection of Input
    force_val = round(user_grip_force_lbf, 1)
    
    # 2. Tension Categorization
    if force_val < 3.0:
        tension_label = "Feather Light"
        description = "Minimum active tension; high feel, low stability."
    elif force_val < 6.0:
        tension_label = "Standard / Relaxed"
        description = "Neutral pressure; balanced control."
    elif force_val < 9.0:
        tension_label = "Firm / Active"
        description = "Intentional squeeze; high stability for high-torque heads."
    else:
        tension_label = "Vise / Max Tension"
        description = "Heavy muscular engagement; stabilizes max-MOI builds."

    return {
        "grip_force_display": f"{force_val} lbf",
        "tension_category": tension_label,
        "ui_description": description
    }

# Execution
result_7 = calculate_result_7(grip_force)

