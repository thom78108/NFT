# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 09:53:15 2021

@author: tfrancois
"""

from PIL import Image, ImageDraw, ImageChops
import random
import colorsys

def random_color():
    
    h = random.random()
    s = 1 
    v = 1 
    
    float_rgb = colorsys.hsv_to_rgb(h,s,v)
    rgb = [int(x)*255  for x in float_rgb]
    
    return tuple(rgb)
    #return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def interpolate(start_color,end_color,factor:float):
    recip = 1 - factor 
    return(
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor),
        )
    
def generate_art(path):
    print("Generating Art")
    target_size_px = 256 
    scale_factor = 2
    image_size_px = target_size_px * scale_factor 
    padding_px = 16 * scale_factor
    image_bg_color = (0,0,0)
    start_color = random_color()
    end_color = random_color()
    image = Image.new("RGB", size =(image_size_px,image_size_px), color = image_bg_color)

    
    # Draw some lines 
    draw = ImageDraw.Draw(image)
    
    # Generate random points
    list_points = []
    
    for i in range(10):
        random_point = (
            random.randint(padding_px,image_size_px-padding_px),
            random.randint(padding_px,image_size_px-padding_px)
            )
        
        list_points.append(random_point)
       
    # Draw bounding box 
    min_x = min([p[0] for p in list_points])
    max_x = max([p[0] for p in list_points])
    min_y = min([p[1] for p in list_points])
    max_y = max([p[1] for p in list_points])
 
    # Center image 
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)
    
    for i,point in enumerate(list_points):
        list_points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)
    
    min_x = min([p[0] for p in list_points])
    max_x = max([p[0] for p in list_points])
    min_y = min([p[1] for p in list_points])
    max_y = max([p[1] for p in list_points])

    # Draw the points
    tickness = 0 
    n_points = len(list_points) - 1
    for i, point in enumerate(list_points):
        
        #overlay canvas
        overlay_image = Image.new("RGB", size =(image_size_px,image_size_px), color = image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)
        
        p1 = point
        
        if i == len(list_points) - 1:
            p2 = list_points[0]
        else: 
            p2 = list_points[i+1]
        
        line_xy = (p1,p2)
        color_factor = i / n_points
        line_color = interpolate(start_color,end_color,color_factor)
        tickness += 1 * scale_factor
        overlay_draw.line(line_xy,fill = line_color, width = tickness)
        image = ImageChops.add(image,overlay_image)
        
    # Image saved 
    image.resize((target_size_px,target_size_px), resample = Image.ANTIALIAS )
    image.save(path)
    
if __name__ == '__main__':
    for i in range(10):
        generate_art("test_image_{}.png".format(i))
    
    
