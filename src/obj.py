# Carga un archivo tipo OBJ
import struct
from PIL import Image
from os import error

def color(r, g, b):
    # Accepts values between 0 and 1
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


class Obj(object):
    def __init__(self, filename):
        
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        self.readFile()
    
    def readFile(self):
        for line in self.lines:
            if line and line[0] != '#':
                prefix, value = line.split(' ', 1)

                if prefix == 'v': # Vertex
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt': # Texture Coords
                    self.texcoords.append(list(map(float, value.split(' '))))
                elif prefix == 'vn': # Normal
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'f': # Faces
                    self.faces.append([ list(map(int, vert.split('/'))) for vert in value.split(' ') if vert != ''])
                
class Texture(object):
    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
        if self.filename.find(".bmp") > 0:
            with open(self.filename, "rb") as image:
                image.seek(10)
                headerSize = struct.unpack('=l', image.read(4))[0]

                image.seek(14 + 4)
                self.width = struct.unpack('=l', image.read(4))[0]
                self.height = struct.unpack('=l', image.read(4))[0]

                image.seek(headerSize)

                self.pixels = []
                
                for x in range(self.width):
                    self.pixels.append([])
                    for y in range(self.height):
                        b = ord(image.read(1)) / 255
                        g = ord(image.read(1)) / 255
                        r = ord(image.read(1)) / 255
                        
                        self.pixels[x].append(color(r, g, b))

            image.close()

        else:
            img = Image.open(self.filename)

            self.width = img.width
            self.height = img.height

            self.pixels = []

            for x in range(self.width):
                self.pixels.append([])
                for y in range(self.height):
                    r = img.getpixel((x,y))[0] / 255
                    g = img.getpixel((x,y))[1] / 255
                    b = img.getpixel((x,y))[2] / 255

                    self.pixels[x].append(color(r, g, b))

            img.close()

    def getColor(self, xcoord, ycoord):
        if 0 <= xcoord < 1 and 0 <= ycoord < 1:
            x = round(xcoord * self.width)
            y = round(ycoord * self.height)
            if y < len(self.pixels):
                if x < len(self.pixels[y]):
                    return self.pixels[y][x]
                else:
                    return color(0,0,0)
            else:
                return color(0,0,0)
            #return self.pixels[y][x]
        else:
            return color(0,0,0)