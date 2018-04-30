from pyreeEngine.node import RenderNode, BaseNode, signalInput, signalOutput, execOut, execIn
from pyreeEngine.basicObjects import ModelObject
from pyreeEngine.engine import PerspectiveCamera, OrthoCamera, HotloadingShader

from pyreeEngine.textures import TextureFromImage

import math
import time

import numpy as np
import quaternion

from OpenGL.GL import *
from OpenGL.GL import shaders

from pathlib import Path

class cylinder(RenderNode):
    def __init__(self, globdata):
        super(cylinder, self).__init__(globdata)

        self.height = 1
        self.radius = 0.5
        self.faces = 128#256
        self.slices = 128#512

        self.cylinderModel1 = None
        self.cylinderModel2 = None

        self.outerTex = TextureFromImage(Path("res/cyl/frame.png"))
        self.innerTex = TextureFromImage(Path("res/poltergeist_sq.png"))

        self.innerShader = HotloadingShader(Path("res/cyl/inner_vert.glsl"), Path("res/cyl/inner_frag.glsl"))
        self.outerShader = HotloadingShader(Path("res/cyl/outer_vert.glsl"), Path("res/cyl/outer_frag.glsl"))


        self.camera = OrthoCamera()
        self.camera.setOrtho(3., 640/480, 0.1, 10.)

    def init(self):
        self.radius = 1.
        self.height = 2.

        self.cylinderModel1 = ModelObject()
        self.cylinderModel1.loadFromVerts(self.genVertices())

        self.height = 3.
        self.radius = 1.5

        self.cylinderModel2 = ModelObject()
        self.cylinderModel2.loadFromVerts(self.genVertices())

        self.cylinderModel1.textures.append(self.innerTex.getTexture())
        self.cylinderModel2.textures.append(self.outerTex.getTexture())

    def genVertices(self):
        vertices = []
        for slice in range(self.slices):
            # n+1 rings
            for face in range(self.faces):
                # m faces (2*m tris)
                u1 = face / self.faces
                ang1 = u1 * math.pi * 2.
                v1 = slice / (self.slices + 1)
                height1 = v1 * self.height - (self.height / 2)
                u2 = (face + 1) / self.faces
                ang2 = u2 * math.pi * 2.
                v2 = (slice + 1) / (self.slices + 1)
                height2 = v2 * self.height - (self.height / 2)
                vert1 = [math.cos(ang1) * self.radius, math.sin(ang1) * self.radius, height1, u1, v1, math.cos(ang1), math.sin(ang1), 0]
                vert2 = [math.cos(ang2) * self.radius, math.sin(ang2) * self.radius, height1, u2, v1, math.cos(ang2), math.sin(ang2), 0]
                vert3 = [math.cos(ang1) * self.radius, math.sin(ang1) * self.radius, height2, u1, v2, math.cos(ang1), math.sin(ang1), 0]
                vert4 = [math.cos(ang2) * self.radius, math.sin(ang2) * self.radius, height2, u2, v2, math.cos(ang2), math.sin(ang2), 0]

                vertices += vert1 + vert2 + vert3 + vert2 + vert4 + vert3
        return vertices

    def getData(self):
        data = {}


    def setData(self, data):
        pass

    @execIn("run")
    def run(self):
        t = time.time()

        if self.globalData.resChanged:
            self.camera.setOrtho(3., self.globalData.resolution[0]/self.globalData.resolution[1], 0.1, 10.)

        self.innerShader.tick()
        self.outerShader.tick()
        self.cylinderModel1.shaderProgram = self.innerShader.getShaderProgram()
        self.cylinderModel2.shaderProgram = self.outerShader.getShaderProgram()

        self.cylinderModel1.rot = quaternion.from_euler_angles(t * -0.1, 0., 0)
        self.cylinderModel2.rot = quaternion.from_euler_angles(t * 0.2, 0. + t*0., -t*0.)


        glClearColor(25/255, 25/255, 112/255, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.camera.lookAt(np.array([5., 0, 1.3]), np.array([0, 0., 0]), np.array([0, -0.1*math.sin(t*0.2) - 0.2, 1]))

        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        self.render([self.cylinderModel1, self.cylinderModel2], self.camera, None)

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)

__nodeclasses__ = [cylinder]