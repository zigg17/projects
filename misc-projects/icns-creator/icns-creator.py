import os
import subprocess
from PIL import Image

# Path to your source PNG file
source_image = '/Users/jakeziegler/Desktop/IMAGES-FOR-MAC/world_network_directories-4.png'

# List of sizes to generate (icon size, and Retina size marked with @2x)
sizes = [
    (16, 16),
    (32, 32),
    (64, 64),
    (128, 128),
    (256, 256),
    (512, 512),
    (1024, 1024),
]

# Create the .iconset directory
iconset_dir = 'MyIcon.iconset'
if not os.path.exists(iconset_dir):
    os.makedirs(iconset_dir)

# Open the source image
img = Image.open(source_image)

# Resize the image for each size and save it in the .iconset folder
for size in sizes:
    img_resized = img.resize(size, Image.Resampling.LANCZOS)  # Updated to LANCZOS
    icon_name = f'icon_{size[0]}x{size[1]}.png'
    img_resized.save(os.path.join(iconset_dir, icon_name))

    # Save @2x (Retina) version if size is 512px or below
    if size[0] <= 512:
        retina_size = (size[0] * 2, size[1] * 2)
        img_resized_2x = img.resize(retina_size, Image.Resampling.LANCZOS)  # Updated to LANCZOS
        retina_icon_name = f'icon_{size[0]}x{size[1]}@2x.png'
        img_resized_2x.save(os.path.join(iconset_dir, retina_icon_name))

print(f'Iconset created in {iconset_dir}')

# Convert .iconset to .icns using the iconutil command
icns_file = 'MyIcon.icns'
try:
    subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', icns_file], check=True)
    print(f'ICNS file created at {icns_file}')
except subprocess.CalledProcessError as e:
    print(f"Error during icns creation: {e}")
