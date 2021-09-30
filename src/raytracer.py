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

gold = Material(spec = 32, matType=OPAQUE_REFLECTIVE, texture = Texture('res/textures/gold2.jpg'), reflex = 0.75)
pearl = Material(texture = Texture('res/textures/pearl.jpg'),spec=64, ior=1.690, matType=OPAQUE_REFLECTIVE, reflex=0.85)
glass = Material(spec = 64, ior = 1.5, matType = TRANSPARENT)
water = Material(diffuse = V3(0.8314, 0.9451, 0.9765), spec = 64, ior = 1.33, matType = TRANSPARENT)
marble = Material(texture = Texture('res/textures/marble.jpg'),spec=128, ior=1.690, matType=OPAQUE_REFLECTIVE, reflex=0.95)
wood = Material(texture = Texture('res/textures/wood.jpg'), spec=8, matType=OPAQUE)

# Inicializar
rtx = Raytracer(width,height)
rtx.envmap = EnvMap('res/envMaps/shangai_env.bmp')

# Iluminar
rtx.ambLight = AmbientLight(strength = 0.1)
rtx.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)
rtx.pointLights.append( PointLight(position = V3(0, 2, 0), intensity = 0.5))

# Esferas
# Reflectivos
rtx.scene.append(Sphere(V3(-3.5, 2, -10), 1.5, gold))
rtx.scene.append(Sphere(V3(0, 2, -10), 1.5, pearl))
# Transparentes
rtx.scene.append(Sphere(V3(3.5, 2, -10), 1.5, water))
rtx.scene.append(Sphere(V3(-3.5, -2, -10), 1.5, glass))
# Opacos
rtx.scene.append(Sphere(V3(0, -2, -10), 1.5, wood))
rtx.scene.append(Sphere(V3(3.5, -2, -10), 1.5, marble))

# Finalizar
rtx.glRender()
rtx.glFinish('output.bmp')
