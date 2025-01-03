from typing import List, Tuple, Dict
import numpy as np

class LEDScreenStructure:
    def __init__(self, panel_size: int = 8, window_size: int = 1000):
        self.panel_size = panel_size
        self.window_size = window_size
        self.base_led_size = 16
        self.display_width = panel_size * 2    # Total width (16)
        self.display_height = panel_size * 3   # Total height (24)
        self.center = window_size // 2
        
        # Initialize the structure
        self.panel_positions = self._init_panel_positions()
        self.led_info = self._calculate_led_positions()
        self.panel_masks = self._create_panel_masks()
    
    def _init_panel_positions(self) -> List[Tuple[int, int]]:
        """Initialize the panel positions in + shape"""
        return [
            (0, -1),   # Top panel
            (-1, 0),   # Left panel
            (1, 0),    # Right panel
            (0, 1)     # Bottom panel
        ]
    
    def _create_panel_masks(self) -> List[np.ndarray]:
        """Create masks for each panel in + shape"""
        masks = []
        regions = [
            (0, 8, 4, 12),     # Top panel (8x8)
            (8, 16, 0, 8),     # Left panel (8x8)
            (8, 16, 8, 16),    # Right panel (8x8)
            (16, 24, 4, 12)    # Bottom panel (8x8)
        ]
        
        for y1, y2, x1, x2 in regions:
            mask = np.zeros((self.display_height, self.display_width))
            mask[y1:y2, x1:x2] = 1
            masks.append(mask)
        return masks
    
    def _calculate_led_positions(self) -> List[Tuple[float, float, float, float]]:
        """Calculate LED positions with linear spreading from center"""
        led_info = []
        base_panel_size = self.panel_size * self.base_led_size
        
        # Spacing configuration - reduced for higher density
        min_spacing = self.base_led_size * 1.1  # Reduced from 1.2
        panel_gap = self.base_led_size * 1.8    # Reduced from 2.0
        
        for panel, (px, py) in enumerate(self.panel_positions):
            for row in range(self.panel_size):
                for col in range(self.panel_size):
                    # Calculate base position relative to panel center
                    base_x = col * min_spacing - (base_panel_size // 2)
                    base_y = row * min_spacing - (base_panel_size // 2)
                    
                    # Add panel offset with proper spacing
                    panel_offset = base_panel_size // 2 + panel_gap
                    x = self.center + base_x + (px * panel_offset)
                    y = self.center + base_y + (py * panel_offset)
                    
                    # Calculate linear spreading factor based on distance from center
                    dx = x - self.center
                    dy = y - self.center
                    max_dist = max(abs(dx), abs(dy))
                    spread_factor = 1.0 + (max_dist / (self.window_size / 4)) * 2.5  # Reduced from 3.0
                    
                    # Apply spreading
                    final_x = self.center + dx * spread_factor
                    final_y = self.center + dy * spread_factor
                    
                    # Calculate LED size (smaller at edges)
                    dist_ratio = max_dist / (self.window_size / 2)
                    size = self.base_led_size * (0.95 - 0.1 * dist_ratio)  # Increased base size factor
                    boundary_size = size * (1.08 + 0.25 * dist_ratio)  # Reduced boundary growth
                    
                    led_info.append((final_x, final_y, size, boundary_size))
        
        return led_info
    
    def get_display_dimensions(self) -> Tuple[int, int]:
        """Get the dimensions of the display array"""
        return self.display_height, self.display_width
    
    def get_panel_mapping(self, panel: int, row: int, col: int) -> Tuple[int, int]:
        """Get the mapping from panel coordinates to display array coordinates"""
        if panel == 0:  # Top panel
            return col + 4, row
        elif panel == 1:  # Left panel
            return col, row + 8
        elif panel == 2:  # Right panel
            return col + 8, row + 8
        else:  # Bottom panel
            return col + 4, row + 16
