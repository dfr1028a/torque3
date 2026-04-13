# result_1_1.py
def calculate_result_1_1(physics_vars, source_vars):
    """SUB-RESULT 1.1: Fulcrum from SOLE PLATE = 0" (head-local reference frame)"""
    
    # From source_engine
    benchmark_head_vcg = source_vars["current_benchmark_z"]
    grip_length = source_vars["grip_length"]
    assembled_length = source_vars["assembled_length"]
    
    # From physics_init  
    shaft_mass = physics_vars["shaft_mass_g"]
    total_system_mass = physics_vars["total_system_mass_kg"] * 1000.0  # Convert back to g
    neck_height = physics_vars["neck_height_mm"] / 25.4  # inches
    
    # From Result 1 (need to pass or calculate here)
    effective_shaft_length = assembled_length - neck_height
    
    # ALL distances measured from SOLE PLATE = 0"
    d_h = benchmark_head_vcg  # Head CG from sole (unchanged, perfect)
    d_s = neck_height + (effective_shaft_length / 2)  # Shaft CG from sole
    d_g = assembled_length - (grip_length / 2)  # Grip CG from sole
    
    x_fulcrum = ((source_vars["head_mass"] * d_h) + (shaft_mass * d_s) + (source_vars["grip_mass"] * d_g)) / total_system_mass
    

    
    return {
        "result_1_1_x_fulcrum": x_fulcrum,
        "result_1_1_d_h": d_h,
        "result_1_1_d_s": d_s,
        "result_1_1_d_g": d_g

        
    }
