import tkinter as tk
import random
import math

def main():
    # The width and height of the scene window.
    width = 800
    height = 500

    # Create the Tk root object.
    root = tk.Tk()
    root.geometry(f"{width}x{height}")

    # Create a Frame object.
    frame = tk.Frame(root)
    frame.master.title("Scene")
    frame.pack(fill=tk.BOTH, expand=1)

    # Create a canvas object that will draw into the frame.
    canvas = tk.Canvas(frame)
    canvas.pack(fill=tk.BOTH, expand=1)

    # Call the draw_scene function.
    draw_scene(canvas, 0, 0, width-1, height-1)

    root.mainloop()


def draw_scene(canvas, scene_left, scene_top, scene_right, scene_bottom):
    """Draw a scene in the canvas. scene_left, scene_top,
    scene_right, and scene_bottom contain the extent in
    pixels of the region where the scene should be drawn.
    Parameters
        scene_left: left side of the region; less than scene_right
        scene_top: top of the region; less than scene_bottom
        scene_right: right side of the region
        scene_bottom: bottom of the region
    Return: nothing

    If needed, the width and height of the
    region can be calculated like this:
    scene_width = scene_right - scene_left + 1
    scene_height = scene_bottom - scene_top + 1
    """
    # Call your functions here, such as draw_sky, draw_ground,
    # draw_snowman, draw_tree, draw_shrub, etc.
    # tree_center = scene_left + 500
    # tree_top = scene_top + 100
    # tree_height = 150
    # draw_pine_tree(canvas, tree_center, tree_top, tree_height)

    #draw gradient sky
    sky_start_color = [50, 200, 255]
    sky_end_color = [70, 100, 255]
    draw_vertical_gradient(canvas, 0,0, 800, 280, 40, sky_start_color, sky_end_color)
    #draw lower horizon gradient sky
    sky_start_color = [70, 100, 255]
    sky_end_color = [50, 200, 255]
    draw_vertical_gradient(canvas, 0,280, 800, 420, 20, sky_start_color, sky_end_color)

    #draw a certain number of clouds
    for i in range(0, 10):
        draw_cloud(canvas,random.randint(0, 800),random.randint(0, 300), 100 + random.randint(0, 40) ,20 +random.randint(0, 30), 40)
   
    #draw ground gradient
    ground_start_color = [250, 180, 120]
    ground_end_color = [70, 20, 15]
    draw_vertical_gradient(canvas, 0,435, 800, 500, 12, ground_start_color, ground_end_color)
    #draw darker ground under grass edge gradient
    ground_start_color = [0, 95, 16]
    ground_end_color = [250, 180, 120]
    draw_vertical_gradient(canvas, 0,400, 800, 435, 10, ground_start_color, ground_end_color)

    #draw grass
    draw_grass(canvas, 0,320, 810,420, 50, 180,100, 2)
    
    

# Define more functions here, like draw_sky, draw_ground,
# draw_cloud, draw_tree, draw_kite, draw_snowflake, etc.


def draw_grass(canvas, x1,y1, x2,y2, length, thickness_x, thickness_y, randomize):
    """Draw a patch of grass in a given area
    Parameters
        canvas: The tkinter canvas
        x1, y1: The top-left corner of patch of grass
        x2, y2: The bottom-right corner of patch of grass
        length: length of grass blades
        thickness_x, thickness_y: how many grass blades to appear along width and height of patch
        randomize: the distance the position of each blade might randomly move
    Return: nothing
    """
    #find length between each blade of grass
    iteration_width = (x2-x1) / thickness_x
    iteration_height = (y2-y1) / thickness_y
    
    #loop through each blade from left to right and top to bottom accross patch
    for i in range(0, thickness_x):
        for j in range(0, thickness_y):
            #far away grass is smaller
            size = length*((j*0.01)+0.15)
            #find position for this grass blade
            x = random.randint(0, randomize*2) - randomize + (x1 + (i * iteration_width)) - size
            y = random.randint(0, randomize*2) - randomize + (y1 + (j * iteration_height)) - size * 0.5
            #random green color
            colorval = "#%02x%02x%02x" % (random.randint(0, 60) + int((thickness_y-j)*0.3), random.randint(150, 200)- int(abs(math.sin(((j+40)+(-i*0.5))/8))*60)+ int((thickness_y-j)* 0.2), int(abs(math.sin((j+(i*0.5))/10))*80) + int((thickness_y-j)*1.3))
            #draw this blade
            canvas.create_arc(x,y, x+size, y+size, outline=colorval, extent=50, style=tk.ARC, width=1.4)




def interpolate_color(startcolor, endcolor, percent):
    """Interpolates between two colors to find a new rgb color
    Parameters
        startcolor: returned when percent=0
        endcolor: returned when percent=1
        percent (decimal): determines what amounts of each color to use 0.5 = perfect mix
    Return: new rgb color as a list[] with three values
    """
    rgb = []
    rgb.append(int(startcolor[0] + (endcolor[0] - startcolor[0]) * percent))
    rgb.append(int(startcolor[1] + (endcolor[1] - startcolor[1]) * percent))
    rgb.append(int(startcolor[2] + (endcolor[2] - startcolor[2]) * percent))
    return rgb


def draw_vertical_gradient(canvas, x1, y1, x2, y2, gradients, startcolor, endcolor):
    """Draws a vertical gradient out of colored rectangles in a given space
    Parameters
        canvas: The tkinter canvas
        x1, y1: The top-left corner of gradient area
        x2, y2: The bottom-right corner of gradient area
        gradients: how many rectangular splits the gradient will use (quality)
        startcolor: color of gradient to appear at the top
        endcolor: color of gradient to appear at the bottom
    Return: nothing
    """

    #find the height of each individual rectangle
    bar_height = (y2 - y1) / gradients

    #iterate through rectangles
    for i in range(0, gradients):
        #find gradient color for this rectangle
        rgb = interpolate_color(startcolor, endcolor, i / gradients)
        #convert color to hex
        colorval = "#%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])
        #draw this rectangle
        canvas.create_rectangle(x1, y1 + i * bar_height,
        x2, y1 + (i+1) * bar_height, width=0, fill=colorval)


def draw_cloud(canvas, posx, posy, width, height, bubbles):
    """Draws a cloud within a given area
    Parameters
        canvas: The tkinter canvas
        posx, posy: The position of the cloud
        width, height: The dimensions of the cloud area
        bubbles: how many individual ovals will make up this cloud
    Return: nothing
    """
    #use a list to store bubble info so we can get proper layering of colors
    cloudlist_x = []
    cloudlist_y = []
    cloudlist_width = []
    cloudlist_height = []

    #generate list of random buble positions and sizes
    for i in range(0, bubbles):
        cloudlist_x.append(posx + random.randint(0, width*2)-width)
        cloudlist_y.append(posy + random.randint(0, height*2)-width)

        cloudlist_width.append(50 + random.randint(0, width))
        cloudlist_height.append(30 + random.randint(0, height))
    
    #iterate through that list drawing dark circles and slowly shrink size and become white
    for j in range(0, 10):
        #each iteration gets a little lighter
        colorval = "#%02x%02x%02x" % (155 + (j*10), 205 + (j*5), 255 )
        for i in range(0, bubbles):
            #draw this cloud
            x1 = cloudlist_x[i] - cloudlist_width[i]/2
            y1 = cloudlist_y[i] - cloudlist_height[i]/2
            x2 = cloudlist_x[i] + cloudlist_width[i]/2
            y2 = cloudlist_y[i] + cloudlist_height[i]/2
            canvas.create_oval(x1,y1, x2,y2, width=0, fill=colorval)
            #shrink the width each iteration to make clouds look smooth
            cloudlist_width[i] *= 0.9
            cloudlist_height[i] *= 0.9


# Call the main function so that
# this program will start executing.
main()