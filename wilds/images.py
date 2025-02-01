import os
from PIL import Image
import numpy as np

base = os.environ["BASE"]

def multiply_image_by_color(img, color):
    img = img.convert("RGBA")  # Ensure it has an alpha channel
    img_array = np.array(img, dtype=np.float32)  # Convert to float for multiplication
    img_array[..., :3] *= np.array(color, dtype=np.float32) / 255.0  # Normalize color
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)  # Clip and convert back to uint8
    return Image.fromarray(img_array, "RGBA")

def split_spritesheet(image_path, sprite_width, sprite_height):
    img = Image.open(image_path)
    img_width, img_height = img.size
    cols = img_width // sprite_width
    rows = img_height // sprite_height
    sprites = []
    for row in range(rows):
        for col in range(cols):
            left = col * sprite_width
            top = row * sprite_height
            right = left + sprite_width
            bottom = top + sprite_height
            sprite = img.crop((left, top, right, bottom))
            sprites.append(sprite)
    return sprites

def add_padding(img, padding, color=(0, 0, 0, 0)):
    img = img.convert("RGBA")  # Ensure transparency is preserved
    new_size = (img.width + 2 * padding, img.height + 2 * padding)
    new_img = Image.new("RGBA", new_size, color)
    new_img.paste(img, (padding, padding), img)
    return new_img

icon_dim = 100
ICONS_TEX = split_spritesheet(os.path.join(base, "natives/stm/gui/ui_texture/tex000000/tex000201_0_imlm4.tex.240701001.png"), icon_dim, icon_dim)
add_icon_dim = 64
ADD_ICONS_TEX = split_spritesheet(os.path.join(base, "natives/stm/gui/ui_texture/tex000000/tex000201_20_imlm4.tex.240701001.png"), add_icon_dim, add_icon_dim)
icon_dim = 100
COL_ICONS = split_spritesheet(os.path.join(base, "natives/stm/gui/ui_texture/tex000000/tex000201_1_imlm4.tex.240701001.png"), icon_dim, icon_dim)
COL_ICONS[0].show
