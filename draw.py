from PIL import Image, ImageDraw, ImageFont

# Create a new blank image
width, height = 400, 400
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Draw a bunny
draw.ellipse((150, 100, 250, 250), fill=(
    255, 255, 255), outline=(0, 0, 0))  # head
draw.ellipse((180, 160, 200, 180), fill=(0, 0, 0))  # left eye
draw.ellipse((220, 160, 240, 180), fill=(0, 0, 0))  # right eye
draw.chord((170, 200, 230, 240), start=180,
           end=0, fill=(255, 150, 150))  # mouth
draw.polygon([(150, 250), (200, 300), (250, 250)],
             fill=(255, 255, 255), outline=(0, 0, 0))  # body

# Save the image
image.save("bunny.png")
