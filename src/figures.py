from msmath import *
from gl import WHITE, baryCoords

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
OPAQUE_REFLECTIVE = 3

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1, ior = 1, reflex = 0.85, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType
        self.reflex = reflex

class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texCoords = texCoords
        self.sceneObject = sceneObject

class DirectionalLight(object):
    def __init__(self, direction = V3(0,-1,0), intensity = 1, color = WHITE ):
        self.direction = normalize(direction)
        self.intensity = intensity
        self.color = color

class AmbientLight(object):
    def __init__(self, strength = 0, color = WHITE):
        self.strength = strength
        self.color = color

    def getColor(self):
        return V3(self.strength * self.color[0],
                  self.strength * self.color[1],
                  self.strength * self.color[2])

class PointLight(object):
    # Luz con punto de origen que va en todas direcciones
    def __init__(self, position = V3(0,0,0), intensity = 1, color = WHITE):
        self.position = position
        self.intensity = intensity
        self.color = color

class Sphere(object):
    def __init__(self, center, radius, material = Material()):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):

        # P = O + t * D

        L = subtract(self.center, orig)
        l = magnitude(L)

        tca = dot(L, dir)

        d = sqroot(l * l - tca * tca)

        if d > self.radius:
            return None

        thc = pow((pow(self.radius,2) - pow(d,2)), 0.5)
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        hit = add(orig, scalarVec(t0, dir))
        normal = subtract(hit, self.center)
        normal = normalize(normal)

        u = 1 - ((arctangent2( normal[2], normal[0]) / (2 * pi)) + 0.5)
        v = arccosine(-normal[1]) / pi

        uvs = V2(u,v)

        return Intersect(distance = t0 ,
                         point = hit,
                         normal = normal,
                         texCoords = uvs,
                         sceneObject = self)

class Triangle(object):
    def __init__(self, A, B, C, material = Material(), isSingleSided = True):
        self.vertA = A
        self.vertB = B
        self.vertC = C
        self.isSingleSided = isSingleSided
        self.AB = subtract(B, A)
        self.AC = subtract(C, A)
        self.BC = subtract(C, B)
        self.CA = subtract(A, C)
        self.normal = normalize(cross(self.AB, self.AC))
        self.material = material

    def ray_intersect(self, orig, dir):
        # t = - (dot(N, orig) + D) / dot(N, dir)
        denom = dot(self.normal, dir)

        if abs(denom) > 0.0001:

            #Single/Double sided feature
            if dot(dir, self.normal) > 0 and self.isSingleSided:
                return None

            D = dot(self.normal, self.vertA)
            num = (dot(self.normal, orig) + D)
            t = num/denom

            if t > 0:
                hit = add(orig, scalarVec(t, dir))

                # edge 0
                edge0 = self.AB
                vp0 = subtract(hit, self.vertA)
                C = cross(edge0, vp0)
                if dot(self.normal, C) < 0: 
                    return None

                # edge 1
                edge1 = self.BC
                vp1 = subtract(hit, self.vertB)
                C = cross(edge1, vp1)
                if dot(self.normal, C) < 0:
                    return None
                
                # edge 2
                edge2 = self.CA
                vp2 = subtract(hit, self.vertC)
                C = cross(edge2, vp2)
                if dot(self.normal, C) < 0:
                    return None


                # Tex Coords
                tx = None
                ty = None

                if self.material.texture:
                    # u, v, w = baryCoords(self.vertA, self.vertB, self.vertC, hit)
                    # tx = self.vertA.x * u + self.vertB.x * v + self.vertC.x * w
                    # ty = self.vertA.y * u + self.vertB.y * v + self.vertC.y * w
                    # ¿Por qué dividido 5???????????
                    tx = abs(hit.x / 5)
                    ty = abs(hit.y / 5)
                    #print("TX= ", tx, " - TY= ", ty)

                if tx and ty:
                    uvs = V2(tx, ty)
                else:
                    uvs = None


                return Intersect(
                    distance = t,
                    point = hit,
                    normal = self.normal,
                    texCoords = uvs,
                    sceneObject = self
                )

        return None


class Plane(object):
    def __init__(self, position, normal, material = Material()):
        self.position = position
        self.normal = normalize(normal)
        self.material = material

    def ray_intersect(self, orig, dir):
        #t = (( planePos - origRayo) dot planeNormal) / (dirRayo dot planeNormal)
        denom = dot(dir, self.normal)

        if abs(denom) > 0.0001:
            num = dot(subtract(self.position, orig), self.normal)
            t = num / denom
            if t > 0:
                # P = O + t * D
                hit = add(orig, scalarVec(t, dir))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObject = self)

        return None

class Model(object):
    def __init__(self, model, position = V3(0,0,0), size = V3(1,1,1), rotation = V3(0,0,0), material = Material()):
        self.position = position
        self.size = size
        self.rotation = rotation
        self.object = model
        self.material = material
        self.modelMatrix = self.createObjectMatrix(position, size, rotation)
        self.triangles = []

        for face in model.faces:
            vertCount = len(face)

            vert0 = model.vertices[face[0][0] - 1]
            vert1 = model.vertices[face[1][0] - 1]
            vert2 = model.vertices[face[2][0] - 1]
            if vertCount == 4:
                vert3 = model.vertices[face[3][0] - 1]

            # vt0 = model.texcoords[face[0][1] - 1]
            # vt1 = model.texcoords[face[1][1] - 1]
            # vt2 = model.texcoords[face[2][1] - 1]
            # if vertCount == 4:
            #     vt3 = model.texcoords[face[3][1] - 1]

            # vn0 = model.normals[face[0][2] - 1]
            # vn1 = model.normals[face[1][2] - 1]
            # vn2 = model.normals[face[2][2] - 1]
            # if vertCount == 4:
            #     vn3 = model.normals[face[3][2] - 1]

            vert0 = self.transform(vert0, self.modelMatrix)
            vert1 = self.transform(vert1, self.modelMatrix)
            vert2 = self.transform(vert2, self.modelMatrix)

            if vertCount == 4:
                vert3 = self.transform(vert3, self.modelMatrix)

            self.triangles.append(Triangle(vert0, vert1, vert2, self.material))
            if vertCount == 4:
                self.triangles.append(Triangle(vert0, vert2, vert3, self.material))

    def createRotationMatrix(self, rotate = V3(0,0,0)):

        rotationX = [
            [1, 0, 0, 0],
            [0, cosine(rotate.x), -sine(rotate.x), 0],
            [0, sine(rotate.x), cosine(rotate.x), 0],
            [0, 0, 0, 1]
        ]

        rotationY = [
            [cosine(rotate.y), 0, sine(rotate.y), 0],
            [0, 1, 0, 0],
            [-sine(rotate.y), 0, cosine(rotate.y), 0],
            [0, 0, 0, 1]
        ]

        rotationZ = [
            [cosine(rotate.z), -sine(rotate.z), 0, 0],
            [sine(rotate.z), cosine(rotate.z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        return multMatrix(multMatrix(rotationX, rotationY), rotationZ)

    def createObjectMatrix(self, translate = V3(0,0,0), scale = V3(1,1,1), rotate = V3(0,0,0)):

        translateMatrix = [ 
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
        ]
        
        scaleMatrix = [
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ]

        rotationMatrix = self.createRotationMatrix(rotate)

        return multMatrix(multMatrix(translateMatrix, rotationMatrix), scaleMatrix)
    
    def transform(self, vertex, vMatrix):
        augVertex = [[vertex[0]], 
                     [vertex[1]], 
                     [vertex[2]], 
                     [1]]
        
        # Multiplies model Matrix per augVertex
        transVertex = multMatrix(vMatrix, augVertex)
        
        # Converts it to a V4
        transVertex = V4(transVertex[0][0], transVertex[1][0], transVertex[2][0], transVertex[3][0])

        # Converts it to a V3
        if transVertex.w != 0:
            transVertex = V3(transVertex.x / transVertex.w,
                             transVertex.y / transVertex.w,
                             transVertex.z / transVertex.w)
        else:
            transVertex = V3(transVertex.x * 100000000,
                             transVertex.y * 100000000,
                             transVertex.z * 100000000)
        
        return transVertex

    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        uvs = None

        for tri in self.triangles:
            triInter = tri.ray_intersect(orig, dir)
            if triInter is not None:
                if triInter.distance < t:
                    t = triInter.distance
                    intersect = triInter

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords = intersect.texCoords,
                         sceneObject = self)
            



class AABB(object):
    # Axis Aligned Bounding Box
    def __init__(self, position, size, material = Material()):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        halfSizeX = size[0] / 2
        halfSizeY = size[1] / 2
        halfSizeZ = size[2] / 2

        #Sides
        self.planes.append(Plane( add(position, V3(halfSizeX,0,0)), V3(1,0,0), material))
        self.planes.append(Plane( add(position, V3(-halfSizeX,0,0)), V3(-1,0,0), material))

        # Up and down
        self.planes.append(Plane( add(position, V3(0,halfSizeY,0)), V3(0,1,0), material))
        self.planes.append(Plane( add(position, V3(0,-halfSizeY,0)), V3(0,-1,0), material))

        # Front and Back
        self.planes.append(Plane( add(position, V3(0,0,halfSizeZ)), V3(0,0,1), material))
        self.planes.append(Plane( add(position, V3(0,0,-halfSizeZ)), V3(0,0,-1), material))

        #Bounds
        epsilon = 0.001
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + self.size[i]/2)
            self.boundsMax[i] = self.position[i] + (epsilon + self.size[i]/2)


    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter is not None:
                # Si estoy dentro de los bounds
                if planeInter.point[0] >= self.boundsMin[0] and planeInter.point[0] <= self.boundsMax[0]:
                    if planeInter.point[1] >= self.boundsMin[1] and planeInter.point[1] <= self.boundsMax[1]:
                        if planeInter.point[2] >= self.boundsMin[2] and planeInter.point[2] <= self.boundsMax[2]:
                            #Si soy el plano mas cercano
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                if abs(plane.normal[0]) > 0:
                                    u = (planeInter.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])
                                    v = (planeInter.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])
                                elif abs(plane.normal[1]) > 0:
                                    u = (planeInter.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                                    v = (planeInter.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])
                                elif abs(plane.normal[2]) > 0:
                                    u = (planeInter.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                                    v = (planeInter.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])
                                
                                uvs = V2(u, v)

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords = uvs,
                         sceneObject = self)
