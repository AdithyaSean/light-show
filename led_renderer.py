import pygame
import numpy as np
from typing import Tuple, List
from screen_structure import LEDScreenStructure

class LEDRenderer:
    def __init__(self, screen_structure: LEDScreenStructure, window_size: int = 1000):
        self.screen_structure = screen_structure
        self.window_size = window_size
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((window_size, window_size))
        pygame.display.set_caption("LED Light Show")
        
        # Get display dimensions
        self.display_height, self.display_width = screen_structure.get_display_dimensions()
        
        # Initialize display array
        self.display = np.zeros((self.display_height, self.display_width))
    
    def clear_display(self):
        """Clear the display array"""
        self.display.fill(0)
    
    def set_display(self, pattern: np.ndarray):
        """Set the display array with a pattern"""
        self.display = np.clip(pattern, 0, 1)
    
    def _draw_led(self, x: float, y: float, size: float, boundary_size: float, intensity: float):
        """Draw a single LED with boundary"""
        # Draw boundary
        pygame.draw.circle(
            self.screen,
            (40, 40, 40),  # Dark boundary color
            (int(x), int(y)),
            int(boundary_size * 0.5)
        )
        
        # Draw LED
        color = (
            int(255 * intensity),
            int(255 * intensity),
            255
        )
        pygame.draw.circle(
            self.screen,
            color,
            (int(x), int(y)),
            int(size * 0.4)
        )
    
    def render(self):
        """Render the current display state"""
        self.screen.fill((20, 20, 20))  # Dark gray background
        
        # Draw each LED
        led_idx = 0
        for panel in range(4):
            for i in range(self.screen_structure.panel_size):
                for j in range(self.screen_structure.panel_size):
                    x, y, size, boundary_size = self.screen_structure.led_info[led_idx]
                    display_x, display_y = self.screen_structure.get_panel_mapping(panel, i, j)
                    
                    if 0 <= display_x < self.display_width and 0 <= display_y < self.display_height:
                        intensity = self.display[display_y, display_x]
                        if intensity > 0.05:  # Only draw visible LEDs
                            self._draw_led(x, y, size, boundary_size, intensity)
                    led_idx += 1
        
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def cleanup(self):
        """Clean up pygame resources"""
        pygame.quit()
