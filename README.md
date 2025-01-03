# LED Panel Light Show

A Python-based light show generator for a unique LED panel setup consisting of four 8x8 LED matrices arranged in a plus (+) shape. The panels are arranged resulting in a small gap in the middle, and the spacing between individual LEDs increases as you move towards the outer edges, creating a natural circular appearance.

## Physical Setup Description
```screen structure
            [Top Panel]
[Left Panel]      +     [Right Panel]
            [Bottom Panel]
```

- 4 LED panels, each containing an 8x8 grid (total 256 LEDs)
- Panels arranged in a plus (+) shape resulting in a small gap in the center
- LED density decreases towards outer edges (increasing space between LEDs)
- Visual effect: Creates a seamless circular display pattern

## Mathematical Concepts Used

### Mathematical Concepts

The light show utilizes several mathematical concepts to create dynamic visual patterns:

1. **Polar Coordinates and Trigonometry**
   - Uses `arctan2(y, x)` for angle calculation in spiral patterns
   - Converts between Cartesian (x,y) and polar (r,θ) coordinates
   - Applies sinusoidal waves with phase shifts for smooth animations

2. **Linear Interpolation and Scaling**
   - Linear spreading factor: `1.0 + (distance / max_distance) * scale`
   - LED size interpolation: `base_size * (min_factor + (1 - min_factor) * distance_ratio)`
   - Boundary growth: `size * (1 + growth_factor * distance_ratio)`

3. **Vector Mathematics**
   - Distance calculations using Manhattan distance: `max(|dx|, |dy|)`
   - Normalized vector components for directional effects
   - Vector scaling for position adjustments

4. **Wave Functions and Interference**
   - Ripple pattern: `sin(2π * frequency * r - speed * t)`
   - Spiral pattern: `sin(arms * θ + speed * t - 2π * r)`
   - Wave pattern: `sin(2π * frequency * (x + y) + t)`

5. **Grid-based Transformations**
   - Panel coordinate mapping between display grid and physical space
   - Uniform grid spacing with variable density
   - Linear transformation matrices for coordinate systems

6. **Random Number Generation**
   - Time-seeded random generation for sparkle effects
   - Probability-based intensity distribution
   - Controlled density through threshold functions

These mathematical principles work together to create fluid, organic-looking animations while maintaining precise LED positioning and timing.

## Installation & Running

1. Clone the repository:
   ```bash
   git clone https://github.com/AdithyaSean/light-show
   cd light-show
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   # Run the setup script
   chmod +x run.sh
   ./run.sh
   ```

### One-Liner Setup

```bash
git clone https://github.com/AdithyaSean/light-show.git && cd light-show && chmod +x run.sh && ./run.sh
```

3. The program will automatically:
   - Create a virtual environment
   - Install required packages
   - Start the light show

## Controls
- ESC or close window to exit
- Patterns change automatically every 5 seconds

## Dependencies
- Python 3.x
- NumPy: For mathematical operations
- Pygame: For visualization

## How It Works
1. Panel Layout:
   - Four 8x8 LED panels arranged in a plus (+) shape
   - Small gap in the center where panels meet
   - LED spacing increases with distance from center

2. Pattern Generation:
   - Uses mathematical functions to create patterns
   - Coordinates are transformed to match physical layout
   - Patterns are synchronized across all panels

3. Visualization:
   - Real-time rendering using Pygame
   - LED intensity shown through brightness
   - Smooth transitions between patterns
