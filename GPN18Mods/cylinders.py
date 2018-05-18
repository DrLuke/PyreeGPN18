from pyreeEngine.node import RenderNode, BaseNode, signalInput, signalOutput, execOut, execIn
from pyreeEngine.basicObjects import ModelObject
from pyreeEngine.engine import *

from pyreeEngine.textures import TextureFromImage, RandomRGBATexture

import math
import time

import numpy as np
import quaternion

from OpenGL.GL import *
from OpenGL.GL import shaders

from pathlib import Path

from pyutil.filter import PT1

import random

from pyutil.img import imgAnim
from pyutil.clk import FPS

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
        self.outerTex.setMinFilter(TextureFromImage.Filter.linear)
        self.outerTex.setMagFilter(TextureFromImage.Filter.linear)
        self.innerTex = TextureFromImage(Path("res/pl/tschunkel.png"))
        self.innerTex.setMinFilter(TextureFromImage.Filter.linear)
        self.innerTex.setMagFilter(TextureFromImage.Filter.linear)

        self.randomTex = RandomRGBATexture([self.faces, self.slices+1])

        self.innerShader = HotloadingShader(Path("res/cyl/inner_vert.glsl"), Path("res/cyl/inner_frag.glsl"))
        self.outerShader = HotloadingShader(Path("res/cyl/outer_vert.glsl"), Path("res/cyl/outer_frag.glsl"))

        self.beatAccum = 0
        self.beatPT1 = PT1(0.3)
        self.jerkPT1 = PT1(0.3)

        self.snareAccum = 0
        self.snarePT1 = PT1(0.5)

        self.camera = OrthoCamera()
        self.camera.setOrtho(3., self.globalData.resolution[0] / self.globalData.resolution[1], 0.1, 10.)


        couchpahts = [
            Path("res/couch/winkefuchs1.png"),
            Path("res/couch/winkefuchs2.png"),
            Path("res/couch/winkefuchs3.png"),
            Path("res/couch/winkefuchs4.png")
        ]
        self.couchAnim = imgAnim(couchpahts)

        self.couchFPS = FPS()

    def init(self):
        self.radius = 1.
        self.height = 2.

        self.cylinderModel1 = ModelObject()
        self.cylinderModel1.loadFromVerts(self.genVertices())

        self.height = 3.
        self.radius = 1.5

        self.cylinderModel2 = ModelObject()
        self.cylinderModel2.loadFromVerts(self.genVertices())

        self.cylinderModel1.textures += [self.innerTex.getTexture(), self.randomTex.getTexture()]
        self.cylinderModel2.textures += [self.outerTex.getTexture(), self.randomTex.getTexture()]

        self.rand1 = 0
        self.rand2 = 0
        self.rand3 = 0

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
        self.register()

        t = time.time()

        #if self.globalData.resChanged:
        self.camera.setOrtho(3., self.globalData.resolution[0]/self.globalData.resolution[1], 0.1, 10.)

        self.innerShader.tick()
        self.outerShader.tick()
        self.cylinderModel1.shaderProgram = self.innerShader.getShaderProgram()
        self.cylinderModel2.shaderProgram = self.outerShader.getShaderProgram()

        if self.couchFPS.tick(5, self.globalData.dt):
            nexttex = self.couchAnim.nextFrame()
            #self.cylinderModel1.textures = [nexttex.getTexture()]

        ## UNIFORMS
        self.cylinderModel1.uniforms["time"] = self.globalData.time
        self.cylinderModel2.uniforms["time"] = self.globalData.time

        if self.globalData.beat[0]:
            self.beatAccum += 1
            self.beatPT1.set = self.beatAccum
            self.jerkPT1.cur = 1
            self.cylinderModel1.uniforms["rand1"] = random.random()
            self.cylinderModel2.uniforms["rand1"] = random.random()
            self.cylinderModel2.uniforms["rand3"] = random.random()

            self.rand1 = random.random()
            self.rand2 = random.random()
            self.rand3 = random.random()

        if self.globalData.beat[1]:
            self.snareAccum += 1
            self.snarePT1.set = self.snareAccum
            self.cylinderModel1.uniforms["rand2"] = random.random()
            self.cylinderModel2.uniforms["rand2"] = random.random()



        self.beatPT1.tick(self.globalData.dt)
        self.jerkPT1.tick(self.globalData.dt)
        self.snarePT1.tick(self.globalData.dt)

        self.cylinderModel1.uniforms["beat"] = self.beatPT1.cur
        self.cylinderModel2.uniforms["beat"] = self.beatPT1.cur
        self.cylinderModel1.uniforms["jerk"] = self.jerkPT1.cur
        self.cylinderModel2.uniforms["jerk"] = self.jerkPT1.cur
        self.cylinderModel1.uniforms["snare"] = self.snarePT1.cur
        self.cylinderModel2.uniforms["snare"] = self.snarePT1.cur

        ##

        self.cylinderModel1.rot = quaternion.from_euler_angles(t * -0.1, t*self.rand3*0.01, 0)
        self.cylinderModel2.rot = quaternion.from_euler_angles(t * 0.2, 0. + t*self.rand1, -t*self.rand2)


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