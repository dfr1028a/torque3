    # --- SUB-RESULT 3.6: MOI ---

def calculate_shaft_axis_moi(head_mass_g, shaft_mass_g, grip_mass_g, 
                           rel_x, rel_y, rel_z, shaft_radius=0.015):
    """
    MOI about SHAFT CENTERLINE (Z-axis) for FACE TWIST resistance.
    rel_x, rel_y = CG offsets from shaft axis (inches → meters)
    """
    m_h = head_mass_g / 1000.0
    m_s = shaft_mass_g / 1000.0  
    m_g = grip_mass_g / 1000.0
    
    # HEAD: Point mass at (rel_x, rel_y) distance from shaft axis
    r_head_sq = (rel_x * 0.0254)**2 + (rel_y * 0.0254)**2
    i_head_shaft = m_h * r_head_sq
    
    # SHAFT: Thin cylinder about its own axis (very small)
    i_shaft_own = 0.5 * m_s * (shaft_radius**2)  # ~0.00001 kg·m²
    
    # GRIP: Thin cylinder about shaft axis (very small)  
    i_grip_shaft = 0.5 * m_g * (0.02)**2         # ~0.00002 kg·m²
    
    return i_head_shaft + i_shaft_own + i_grip_shaft

# Replace Result 3.6 with:
shaft_moi = calculate_shaft_axis_moi(
    source_engine.head_mass,
    physics_vars["shaft_mass_g"], 
    source_engine.grip_mass,
    rel_x, rel_y, rel_z  # From Result 3.1
)

