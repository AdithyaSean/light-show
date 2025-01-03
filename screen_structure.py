from typing import List, Tuple, Dict
import numpy as np

class LEDScreenStructure:
    def __init__(self, panel_size: int = 8, window_size: int = 1000):
        self.panel_size = panel_size
        self.window_size = window_size
        self.base_led_size = 16
        self.display_width = panel_size * 2    # Total width (16)
        self.display_height = panel_size * 3   # Total height (24)
        self.center = window_size // 2  # Calculate center once
        
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
        """Calculate LED positions and sizes with linear spreading from center"""
        led_info = []
        base_panel_size = self.panel_size * self.base_led_size

        # Define weight factors for horizontal and vertical spacing
        weight_x = 1.5
        weight_y = 1.5

        for panel, (px, py) in enumerate(self.panel_positions):
            for row in range(self.panel_size):
                for col in range(self.panel_size):
                    # Calculate base grid position within the panel square
                    base_x = col * self.base_led_size - (base_panel_size // 2)
                    base_y = row * self.base_led_size - (base_panel_size // 2)
                    
                    # Adjust position based on panel position with minimal gap
                    x_offset = px * (base_panel_size * 0.5 + self.base_led_size * 1.5)
                    y_offset = py * (base_panel_size * 0.5 + self.base_led_size * 1.5)
                    x = self.center + base_x + x_offset
                    y = self.center + base_y + y_offset
                    
                    # Calculate normalized distance from center (0 to 1)
                    dx = x - self.center
                    dy = y - self.center
                    max_distance = self.window_size / 3  # Maximum expected distance

                    # Apply weight factors based on desired direction
                    r = max(abs(dx * weight_x), abs(dy * weight_y)) / max_distance
                    
                    # Linear spreading factor
                    spread = 1 + r * 4.0  # Linear spreading
                    
                    # Apply linear spreading
                    final_x = self.center + dx * spread
                    final_y = self.center + dy * spread
                    
                    # LED size decreases linearly with distance
                    size = self.base_led_size * (0.9 - 0.1 * r)
                    
                    # Boundary grows linearly with distance
                    boundary_size = size * (1.1 + 0.4 * r)
                    
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
