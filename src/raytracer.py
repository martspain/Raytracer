from msmath import *
from gl import Raytracer, color
from obj import Obj, Texture
from figures import Sphere, Material

width = 720
height = 1080

brick = Material(diffuse = color(0.8,0.25,0.25))
stone = Material(diffuse = color(0.4,0.4,0.4))
grass = Material(diffuse = color(0.4,1,0))
wood = Material(diffuse = color(0.5,0.5,0.1))

snow = Material(diffuse = color(1, 0.98, 0.98))
gold = Material(diffuse = color(0.83, 0.686, 0.216))
marineBlue = Material(diffuse = color(0, 0.267, 0.506))
carrot = Material(diffuse = color(0.929, 0.569, 0.129))
mouth = Material(diffuse = color(0.345, 0.094, 0.122))
button = Material(diffuse = color(0.0627, 0.0627, 0.0627))
crystal = Material(diffuse = color(0.235, 0.875, 1))

rtx = Raytracer(width,height)
rtx.glClearColor(0, 0, 0.325)
rtx.glClear()

#rtx.scene.append( Sphere(V3(0,0,-10), 10, marineBlue)) 
# Bottom body
rtx.scene.append( Sphere(V3(0,-20,-30), 15, snow) )

# Middle Body
rtx.scene.append( Sphere(V3(0,3,-30), 12, snow) )

# Head
rtx.scene.append( Sphere(V3(0,23,-30), 8, snow) )

# Nose
rtx.scene.append( Sphere(V3(0,16,-20), 1.5, carrot) )

# Mouth top left
rtx.scene.append( Sphere(V3(-2,13,-20), 0.5, mouth) )

# Mouth left
rtx.scene.append( Sphere(V3(-0.75,12.5,-20), 0.5, mouth) )

# Mouth right
rtx.scene.append( Sphere(V3(0.75,12.5,-20), 0.5, mouth) )

# Mouth top right
rtx.scene.append( Sphere(V3(2,13,-20), 0.5, mouth) )

# Left eye
rtx.scene.append( Sphere(V3(-1.5,20,-20), 1, crystal) )
rtx.scene.append( Sphere(V3(-1.25,16,-16), 0.5, button) )
rtx.scene.append( Sphere(V3(-0.9,13,-13), 0.2, snow) )

# Right eye
rtx.scene.append( Sphere(V3(1.5,20,-20), 1, crystal) )
rtx.scene.append( Sphere(V3(1.25,16,-16), 0.5, button) )
rtx.scene.append( Sphere(V3(1.1,13,-13), 0.2, snow) )

# Top button
rtx.scene.append( Sphere(V3(0,5,-19), 2, button) )

# Middle button
rtx.scene.append( Sphere(V3(0,-4,-19), 2, button) )

# Bottom button
rtx.scene.append( Sphere(V3(0,-13,-15), 2, button) )

rtx.glRender()

rtx.glFinish('output.bmp')