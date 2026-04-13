# result_1.py
def calculate_result_1(physics_vars):
    """Total system mass using physics_init outputs"""
    
    # Step 1: Use shaft_mass_g from physics_init (don't recalculate)
    shaft_mass_g = physics_vars["shaft_mass_g"]
    
    # Step 2: Use total_system_mass_kg from physics_init  
    total_system_mass_g = physics_vars["total_system_mass_kg"] * 1000.0
    
    # Step 3: Sub-result for Swing Weight calculation
    total_system_mass_oz = total_system_mass_g / 28.34952
    
    return {
        "result_1_total_system_mass_g": total_system_mass_g,
        "result_1_total_system_mass_oz": total_system_mass_oz
    }
