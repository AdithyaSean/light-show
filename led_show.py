import numpy as np
import time
import pygame
from typing import Tuple, List, Callable
import sys
from screen_structure import LEDScreenStructure
from led_renderer import LEDRenderer

class LEDShow:
    def __init__(self, panel_size: int = 8, window_size: int = 1000):
        # Initialize components
        self.screen_structure = LEDScreenStructure(panel_size, window_size)
        self.renderer = LEDRenderer(self.screen_structure, window_size)
        
        # Get dimensions for pattern generation
        self.display_height, self.display_width = self.screen_structure.get_display_dimensions()
        
        # Create coordinate matrices for pattern generation
        y, x = np.mgrid[-1:1:complex(0, self.display_height), -1:1:complex(0, self.display_width)]
        self.r = np.sqrt(x**2 + y**2)
        self.theta = np.arctan2(y, x)
        self.x, self.y = x, y
    
    def _generate_pattern(self, func: Callable, t: float) -> np.ndarray:
        """Helper to generate and normalize patterns"""
        pattern = func(t)
        return (pattern + 1) / 2
    
    def ripple_pattern(self, t: float, frequency: float = 2, speed: float = 3) -> np.ndarray:
        """Generate a ripple pattern emanating from the center"""
        return self._generate_pattern(
            lambda t: np.sin(2 * np.pi * frequency * self.r - speed * t)
        , t)
    
    def spiral_pattern(self, t: float, arms: int = 2, speed: float = 3) -> np.ndarray:
        """Generate a spinning spiral pattern"""
        return self._generate_pattern(
            lambda t: np.sin(arms * self.theta + speed * t - 2 * np.pi * self.r)
        , t)
    
    def sparkle_pattern(self, t: float, density: float = 0.1) -> np.ndarray:
        """Generate random sparkles with time-based variation"""
        np.random.seed(int(t * 30))
        pattern = np.random.random(self.renderer.display.shape) < density
        return pattern.astype(float)
    
    def wave_pattern(self, t: float, frequency: float = 2) -> np.ndarray:
        """Generate a wave pattern across the display"""
        return self._generate_pattern(
            lambda t: np.sin(2 * np.pi * frequency * (self.x + self.y) + t)
        , t)
    
    def apply_pattern(self, pattern_func: Callable, t: float, **kwargs) -> None:
        """Apply a pattern to the display with panel masks"""
        base_pattern = pattern_func(t, **kwargs)
        self.renderer.clear_display()
        
        for mask in self.screen_structure.panel_masks:
            self.renderer.display += base_pattern * mask
        
        self.renderer.set_display(self.renderer.display)
    
    def run_demo(self, fps: float = 60):
        """Run a continuous demo of different patterns"""
        patterns = [
            (self.ripple_pattern, {'frequency': 3, 'speed': 4}),
            (self.spiral_pattern, {'arms': 2, 'speed': 3}),
            (self.wave_pattern, {'frequency': 1.5}),
            (self.sparkle_pattern, {'density': 0.15}),
        ]
        
        clock = pygame.time.Clock()
        start_time = time.time()
        
        try:
            while True:
                if not self.renderer.handle_events():
                    break
                
                t = time.time() - start_time
                pattern_idx = int(t / 4) % len(patterns)  # Change pattern every 4 seconds
                pattern_func, kwargs = patterns[pattern_idx]
                
                self.apply_pattern(pattern_func, t, **kwargs)
                self.renderer.render()
                clock.tick(fps)
        
        except KeyboardInterrupt:
            pass
        finally:
            self.renderer.cleanup()

if __name__ == "__main__":
    show = LEDShow()
    show.run_demo()
