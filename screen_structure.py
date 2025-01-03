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
        # Increase panel separation to prevent overlap
        panel_scale = 1.5  # Increased from 1.2 to create more space between panels
        return [
            (0, -panel_scale),    # Top panel
            (-panel_scale, 0),    # Left panel
            (panel_scale, 0),     # Right panel
            (0, panel_scale)      # Bottom panel
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
        """Calculate LED positions with proper spacing to prevent overlap"""
        led_info = []
        
        # Base configuration with increased spacing
        base_led_spacing = self.base_led_size * 1.4  # Increased from 1.2 for more space between LEDs
        panel_size_px = base_led_spacing * (self.panel_size - 1)  # Total panel size in pixels
        
        # Panel separation with increased gap
        panel_gap = self.base_led_size * 2.5  # Increased from 2.2 for larger gap between panels
        
        for panel, (px, py) in enumerate(self.panel_positions):
            for row in range(self.panel_size):
                for col in range(self.panel_size):
                    # Calculate base position within panel
                    rel_x = col * base_led_spacing - panel_size_px / 2
                    rel_y = row * base_led_spacing - panel_size_px / 2
                    
                    # Add panel offset with improved spacing
                    panel_offset = panel_size_px / 2 + panel_gap
                    x = self.center + rel_x + (px * panel_offset)
                    y = self.center + rel_y + (py * panel_offset)
                    
                    # Calculate distance from center for size adjustment
                    dx = x - self.center
                    dy = y - self.center
                    dist = np.sqrt(dx*dx + dy*dy)
                    max_dist = self.window_size / 3
                    dist_ratio = min(dist / max_dist, 1.0)
                    
                    # Improved size calculations to prevent overlap
                    min_size_factor = 0.7  # Minimum size relative to base size
                    base_size = self.base_led_size * (min_size_factor + (1 - min_size_factor) * (1.0 - 0.3 * dist_ratio))
                    size = base_size * 0.7  # Reduced from 0.8 to prevent LED overlap
                    boundary_size = base_size * 0.9  # Reduced boundary size to create clear separation
                    
                    led_info.append((x, y, size, boundary_size))
        
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
