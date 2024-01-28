from PIL import Image, ImageDraw
import math
import random

def hex_to_dec(hex_str):
    return int(hex_str, 16)

def dec_to_hex(dec):
    return hex(dec).lstrip("0x").zfill(6)

def fibonacci_sequence_for_colors(n):
    color_spectrum_length = 0xFFFFFF + 1  # Number of colors in the spectrum
    fib_sequence = [0, 1]

    for _ in range(2, n):
        next_color = abs((fib_sequence[-1] + fib_sequence[-2]) % color_spectrum_length) # Use abs to handle negative values
        fib_sequence.append(next_color)

    hex_sequence = ["#" + dec_to_hex(color) for color in fib_sequence]
    return hex_sequence

def hex_to_rgb(hex_str):
    return tuple(int(hex_str[i:i+2], 16) for i in (1, 3, 5))

def create_canvas(width, height, colors, block_size):
    canvas = Image.new("RGB", (width, height), color=(255, 255, 255))  # Set background color to white
    draw = ImageDraw.Draw(canvas)

    # Calculate the golden ratio
    phi = (1 + math.sqrt(5)) / 2

    # Initialize variables for drawing the golden spiral
    x, y = width // 2, height // 2  # Start in the center of the canvas
    angle = 0

    # Get the Fibonacci sequence for the colors
    fib_sequence = fibonacci_sequence_for_colors(len(colors))

    for n, color in enumerate(colors):
        # Calculate the size of the rectangle based on the golden ratio
        a = hex_to_dec(fib_sequence[n].strip("#")) # Get the Fibonacci number for this rectangle from the list
        color_width = a / 255 # Use a different color width for each rectangle
        size = int(color_width * phi)

        # Calculate the next position based on the current angle
        x -= int(math.cos(math.radians(angle)) * size) # Use -= instead of +=
        y -= int(math.sin(math.radians(angle)) * size) # Use -= instead of +=

        # Handle color codes exceeding the maximum value
        if x > width or y > height:
            x %= width
            y %= height

        # Draw the cage-like block

        draw.rectangle([x, y, x + size, y + size], fill=color)
        draw.rectangle([x, y, x + size, y + size], outline=(0, 0, 0), width=2)
        angle += (math.pi * phi)
            

        # Update the angle
        #angle += 90  # Rotate the rectangle by 90 degrees for a square

    return canvas


fibonacci_length = 1000  # You can change this to the desired length of the sequence
block_size = 10  # You can adjust the block size as needed

# Generate Fibonacci color sequence
fibonacci_colors = fibonacci_sequence_for_colors(fibonacci_length)

# Convert hex colors to RGB
rgb_colors = [hex_to_rgb(color) for color in fibonacci_colors]

# Create the canvas
canvas_width = 21  # inches
canvas_height = 9 # inches
# Make Multiple

canvas = create_canvas(int(canvas_width * 100), int(canvas_height * 100), rgb_colors, block_size)

# Save the canvas as an image file (e.g., PNG)
canvas.save(f"fibonacci_ellipse1.png")