from PIL import Image, ImageDraw
import math

def logistic_map(x, r):
    return r * x * (1 - x)

def fibonacci_sequence_for_colors(n):
    color_spectrum_length = 0xFFFFFF + 1  # Number of colors in the spectrum
    fib_sequence = [0, 1]

    for _ in range(2, n):
        next_color = (fib_sequence[-1] + fib_sequence[-2]) % color_spectrum_length
        fib_sequence.append(next_color)

    hex_sequence = ["#" + format(color, '06x') for color in fib_sequence]
    return hex_sequence

def hex_to_rgb(hex_str):
    return tuple(int(hex_str[i:i+2], 16) for i in (1, 3, 5))

def create_canvas(width, height, colors, block_size, chaos_parameter):
    canvas = Image.new("RGB", (width, height), color=(255, 255, 255))  # Set background color to white
    draw = ImageDraw.Draw(canvas)

    # Calculate the golden ratio
    phi = (1 + math.sqrt(5)) / 2

    # Initialize variables for drawing the golden spiral
    x, y = width // 2, height // 2  # Start in the center of the canvas
    angle = 0

    for color in colors:
        # Use the red component of the RGB tuple for the size calculation
        size = int(color[0] * phi)

        # Calculate the chaotic modification to the angle
        chaotic_factor = logistic_map(math.cos(math.radians(angle)), chaos_parameter)
        angle += math.pi + int(180 * chaotic_factor)  # Adjust the angle based on the chaotic factor

        # Calculate the next position based on the modified angle
        x += int(math.cos(math.radians(angle)) * size)
        y += int(math.sin(math.radians(angle)) * size)

        # Handle color codes exceeding the maximum value
        if x > width or y > height:
            x %= width
            y %= height

        # Draw the cage-like block
        print(size)
        if size % 2 == 1:
            print("odd")

            # Since odd we grab the color compliment
            compliment = tuple(255 - value for value in color)

            draw.ellipse([x, y, x + size, y + size], fill=compliment)
        else:    
            print("even")
            draw.rectangle([x, y, x + size, y + size], fill=color)

    return canvas

fibonacci_length = 1000  # You can change this to the desired length of the sequence
block_size = 10  # You can adjust the block size as needed
chaos_parameter = math.pi  # You can experiment with different chaos parameters

# Generate Fibonacci color sequence
fibonacci_colors = fibonacci_sequence_for_colors(fibonacci_length)

# Convert hex colors to RGB
rgb_colors = [hex_to_rgb(color) for color in fibonacci_colors]

# Create the canvas with chaos theory modification
canvas_width = 21  # inches
canvas_height = 9  # inches
canvas = create_canvas(int(canvas_width * 100), int(canvas_height * 100), rgb_colors, block_size, chaos_parameter)

# Save the canvas as an image file (e.g., PNG)
canvas.save("FibPhot/chaos_compliment.png")
