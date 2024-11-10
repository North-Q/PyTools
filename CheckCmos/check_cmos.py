from PIL import Image

# Open the image file
image_path = './test/P1000003.JPG'
image = Image.open(image_path)
pixels = image.load()

# Initialize a list to store non-black pixel RGB values
non_black_pixels = []

# Iterate over each pixel
for x in range(image.width):
    for y in range(image.height):
        r, g, b = pixels[x, y][:3]
        if(r>10 and g>10 and b>10):
            print(f'Non-black pixel at ({x}, {y}): RGB = ({r}, {g}, {b})')
            non_black_pixels.append((r, g, b))

# Output the result
print(len(non_black_pixels))

