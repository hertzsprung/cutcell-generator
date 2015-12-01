#!/usr/bin/env python
from __future__ import print_function
from math import cos, pi
import scipy.optimize

class DomainSpec:
    def __init__(self, width, height, nx, nz):
        self.xMin = - width / 2.0
        self.width = width
        self.height = height
        self.nx = nx
        self.nz = nz
        self.dx = width/nx
        self.dz = height/nz

    def toMesh(self):
        vertices = []
        for z in self.horizontalFacePositions():
            for x in self.verticalFacePositions():
                vertices.append((x, z))

        mesh = Mesh(vertices)

        for z in self.horizontalFacePositions():
            for xLeft, xRight in self.verticalFacePositionPairs():
                vertexLeft = mesh.vertexIndex((xLeft, z))
                vertexRight = mesh.vertexIndex((xRight, z))
                mesh.addFace([vertexLeft, vertexRight]) 

        for x in self.verticalFacePositions():
            for zBottom, zTop in self.horizontalFacePositionPairs():
                vertexBottom  = mesh.vertexIndex((x, zBottom))
                vertexTop = mesh.vertexIndex((x, zTop))
                mesh.addFace([vertexBottom, vertexTop]) 

        return mesh

    def verticalFacePositions(self):
        return [self.xMin + self.dx * i for i in range(0, self.nx+1)]

    def verticalFacePositionPairs(self):
        return self.pairs(self.verticalFacePositions())

    def horizontalFacePositions(self):
        return [self.dz * k for k in range(0, self.nz+1)]

    def horizontalFacePositionPairs(self):
        return self.pairs(self.horizontalFacePositions())

    def pairs(self, l):
        return zip(l, l[1:])

class Mesh:
    def __init__(self, vertices):
        self.vertices = vertices
        self.faces = []

    def addVertex(self, v):
        self.vertices.append(v)

    def getVertices(self):
        return self.vertices

    def removeVertices(self, removals):
        for v in removals:
            self.vertices.remove(v)

    def vertexIndex(self, v):
        return self.vertices.index(v)

    def addFace(self, f):
        self.faces.append(f)

class Shaver:
    def shave(self, mesh, domainSpec, mountain):
        for x in domainSpec.verticalFacePositions():
            z = mountain.heightAt(x)
            mesh.addVertex((x, z))

        for z in domainSpec.horizontalFacePositions():
            for xLeft, xRight in domainSpec.verticalFacePositionPairs():
                if (mountain.heightAt(xLeft)-z) * (mountain.heightAt(xRight)-z) < 0:
                    xIntersect = scipy.optimize.brentq(lambda x: mountain.heightAt(x)-z, xLeft, xRight)
                    mesh.addVertex((xIntersect, mountain.heightAt(xIntersect)))

        verticesBelowGround = []
        for v in mesh.getVertices():
            if v[1] < mountain.heightAt(v[0]):
                verticesBelowGround.append(v)

        mesh.removeVertices(verticesBelowGround) 

class SchaerCosMountain:
    def __init__(self, halfWidth, peakHeight, wavelength):
        self.a = halfWidth
        self.h0 = peakHeight
        self.lmbda = wavelength

    def heightAt(self, x):
        if (abs(x) < self.a):
            return self.h0 * cos(0.5*pi*x/self.a)**2 * cos(pi*x/self.lmbda)**2
        else:
            return 0

def printVertices(mesh, fh):
    for v in mesh.vertices:
        print(v[0], v[1], file=f)

def printFaces(mesh, fh):
    for f in mesh.faces:
        v1 = mesh.vertices[f[0]]
        v2 = mesh.vertices[f[1]]
        print(v1[0], v1[1], v2[0], v2[1], file=fh)

domain = DomainSpec(25e3, 15e3, 50, 15)
mesh = domain.toMesh()
mountain = SchaerCosMountain(5e3, 5e3, 4e3);
shaver = Shaver()
#shaver.shave(mesh, domain, mountain)

with open('vertices.dat', 'w') as f:
    printVertices(mesh, f)

with open('faces.dat', 'w') as f:
    printFaces(mesh, f)
