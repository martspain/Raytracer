from msmath import *
from gl import Raytracer, color
from obj import Obj, Texture, EnvMap
from figures import *

width = 1920
height = 1080

# brick = Material(diffuse = color(0.8,0.25,0.25))
# stone = Material(diffuse = color(0.4,0.4,0.4))
# grass = Material(diffuse = color(0.4,1,0))
# snow = Material(diffuse = color(1, 0.98, 0.98))
# marineBlue = Material(diffuse = color(0, 0.267, 0.506))
# carrot = Material(diffuse = color(0.929, 0.569, 0.129))
# mouth = Material(diffuse = color(0.345, 0.094, 0.122))
# button = Material(diffuse = color(0.0627, 0.0627, 0.0627))
# mirror = Material(spec = 128, matType = REFLECTIVE)
# silver = Material(diffuse = V3(0.7529, 0.7529, 0.7529), spec = 32, matType=REFLECTIVE)
# crystal = Material(diffuse = V3(0.235, 0.875, 1), spec = 48, ior = 2, matType=TRANSPARENT)

# glass = Material(spec = 64, ior = 1.5, matType = TRANSPARENT)
# marble = Material(texture = Texture('res/textures/marble.jpg'),spec=128, ior=1.690, matType=OPAQUE_REFLECTIVE, reflex=0.95)

water = Material(diffuse = V3(0.8314, 0.9451, 0.9765), spec = 64, ior = 1.33, matType = TRANSPARENT)
pearl = Material(texture = Texture('res/textures/pearl.jpg'),spec=64, ior=1.690, matType=OPAQUE_REFLECTIVE, reflex=0.85)
diamond = Material(diffuse = V3(0.7255, 0.9490, 1), spec = 64, ior = 2.418, matType = TRANSPARENT)
gold = Material(spec = 312, matType=OPAQUE_REFLECTIVE, texture = Texture('res/textures/gold2.jpg'), reflex = 0.75)
shirt = Material(texture=Texture('res/textures/silver.jpg'), matType = OPAQUE_REFLECTIVE, spec=64, reflex=0.8)
# shirtF = Material(diffuse=V3(0.961, 0.961, 0.961), matType = REFLECTIVE)
jeans = Material(diffuse=V3(0.067, 0.208, 0.447), matType=OPAQUE, spec=32)
# jeansF = Material(texture=Texture('res/textures/jeans.jpg'), matType=OPAQUE, spec=32)
skin = Material(diffuse=V3(0.945, 0.761, 0.490), matType=OPAQUE, spec=32)
darkSkin = Material(diffuse=V3(0.878, 0.675, 0.412), matType=OPAQUE, spec=32)
wood = Material(texture = Texture('res/textures/wood.jpg'), spec=8, matType=OPAQUE)
beard = Material(texture = Texture('res/textures/beard.jpg'), spec=8, matType=OPAQUE)
cotton = Material(texture = Texture('res/textures/redCotton.jpg'), spec=8, matType=OPAQUE)
eyeBlank = Material(diffuse=V3(0.973, 0.961, 0.980), matType=OPAQUE_REFLECTIVE, spec=32, reflex=0.9)
eyeBlue = Material(diffuse=V3(0,0, 1), matType=OPAQUE_REFLECTIVE, spec=256, reflex=0.4)


# Inicializar
rtx = Raytracer(width,height)
rtx.envmap = EnvMap('res/envMaps/cannon_env.bmp')

# Iluminar
rtx.ambLight = AmbientLight(strength = 0.1)
rtx.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)
rtx.pointLights.append( PointLight(position = V3(-2, 2, 0), intensity = 0.5))
rtx.pointLights.append( PointLight(position = V3(0, -1.7, -11), intensity = 0.3))

#rtx.scene.append(Model(Obj('res/obj/model.obj'), V3(0,0, -10), V3(0.1, 0.1, 0.1)))

x = -1
y = -1
z = -1

# Shirt
rtx.scene.append(AABB(V3(2 + x, 1 + y, -10 + z), V3(2, 2.5, 1), shirt))
rtx.scene.append(AABB(V3(3.5 + x, 1.75 + y, -10 + z), V3(1, 1, 1), shirt))
rtx.scene.append(AABB(V3(0.5 + x, 1.75 + y, -10 + z), V3(1, 1, 1), shirt))

# Jeans
rtx.scene.append(AABB(V3(1.47 + x, -1.5 + y, -10 + z), V3(1, 2.5, 1), jeans))
rtx.scene.append(AABB(V3(2.53 + x, -1.5 + y, -10 + z), V3(1, 2.5, 1), jeans))

# Shoes
rtx.scene.append(AABB(V3(1.47 + x, -3 + y, -10 + z), V3(1, 0.5, 1), gold))
rtx.scene.append(AABB(V3(2.53 + x, -3 + y, -10 + z), V3(1, 0.5, 1), gold))

# Arms
rtx.scene.append(AABB(V3(-0.75 + x, 1.75 + y, -10 + z), V3(2,1,1), skin))
rtx.scene.append(AABB(V3(3.5 + x, 0.5 + y, -10 + z), V3(1,2,1), skin))

# Sword
rtx.scene.append(AABB(V3(-1.25 + x, 2 + y, -10 + z), V3(0.5, 1.75, 0.5), wood))
rtx.scene.append(AABB(V3(-1.25 + x, 2.75 + y, -10 + z), V3(2, 0.5, 0.75), pearl))
rtx.scene.append(AABB(V3(-1.25 + x, 4.5 + y, -10 + z), V3(0.5, 3, 0.5), diamond))

# Head
rtx.scene.append(AABB(V3(2 + x, 3.15 + y, -10 + z), V3(1.8, 1.8, 1.5), skin))
rtx.scene.append(AABB(V3(2 + x, 3.75 + y, -10 + z), V3(1.9, 0.3, 1.6), cotton))
rtx.scene.append(AABB(V3(1.375 + x, 3.25 + y, -9.25 + z), V3(0.25, 0.25, 0.1), eyeBlank))
rtx.scene.append(AABB(V3(1.645 + x, 3.25 + y, -9.25 + z), V3(0.25, 0.25, 0.1), eyeBlue))
rtx.scene.append(AABB(V3(2.645 + x, 3.25 + y, -9.25 + z), V3(0.25, 0.25, 0.1), eyeBlank))
rtx.scene.append(AABB(V3(2.375 + x, 3.25 + y, -9.25 + z), V3(0.25, 0.25, 0.1), eyeBlue))
rtx.scene.append(AABB(V3(2.01 + x, 3 + y, -9.25 + z), V3(0.48, 0.25, 0.1), darkSkin))
rtx.scene.append(AABB(V3(1.645 + x, 2.75 + y, -9.25 + z), V3(0.25, 0.25, 0.1), beard))
rtx.scene.append(AABB(V3(2.375 + x, 2.75 + y, -9.25 + z), V3(0.25, 0.25, 0.1), beard))
rtx.scene.append(AABB(V3(2.01 + x, 2.5 + y, -9.25 + z), V3(0.99, 0.25, 0.1), beard))

# Finalizar
rtx.glRender()
rtx.glFinish('output.bmp')
