"""
Utility functions for image processing tasks.
This module provides functions to generate a blurred background image with a gradient.

TODO: Implement blurred background generation and integrate with the main application.
"""


from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def generate_blur_background(width=800, height=600, color1=(245,245,255), color2=(230,240,255), blur_radius=16, output_path="blurred_bg.png"):
    # Cria imagem com gradiente
    base = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    # Adiciona um blur generoso
    blurred = base.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    blurred.save(output_path)
    return output_path
