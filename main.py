from PIL import Image
import os
from collections import deque

def get_adjacent_pixels(x, y, image_width, image_height):
    adjacent_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in adjacent_positions:
        adj_x, adj_y = x + dx, y + dy
        if 0 <= adj_x < image_width and 0 <= adj_y < image_height:
            yield adj_x, adj_y

def flood_fill(start_x, start_y, pixels, image_width, image_height):
    to_fill = deque([(start_x, start_y)])
    filled = set()
    min_x, max_x = start_x, start_x
    min_y, max_y = start_y, start_y

    while to_fill:
        x, y = to_fill.pop()
        if (x, y) not in filled and pixels[x, y][3] > 0:
            filled.add((x, y))
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
            for adj in get_adjacent_pixels(x, y, image_width, image_height):
                to_fill.appendleft(adj)
    # Calculate the area of the bounding box
    area = (max_x - min_x + 1) * (max_y - min_y + 1)
    return filled, (min_x, min_y, max_x + 1, max_y + 1), area

def find_bricks(image_path, output_folder):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        pixels = img.load()

        visited = set()
        brick_num = 0

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for x in range(img.width):
            for y in range(img.height):
                if (x, y) not in visited and pixels[x, y][3] > 0:
                    brick_pixels, bounding_box, area = flood_fill(x, y, pixels, img.width, img.height)
                    if area >= 50:  # Only accept regions larger than 50px^2
                        visited.update(brick_pixels)
                        brick_image = img.crop(bounding_box)
                        brick_image.save(os.path.join(output_folder, f'brick_{brick_num}.png'))
                        brick_num += 1

# Define the source image path and the output folder
image_path = '/Users/ryanhuang/Documents/GitHub/export-bricks/The_first_one.png'
output_folder = '/Users/ryanhuang/Documents/GitHub/export-bricks/bricks_output'

# Find and save the bricks
find_bricks(image_path, output_folder)
