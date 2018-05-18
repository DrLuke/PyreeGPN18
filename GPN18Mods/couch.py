from pyreeEngine.node import RenderNode, BaseNode, signalInput, signalOutput, execOut, execIn
from pyreeEngine.basicObjects import ModelObject, FSQuad
from pyreeEngine.engine import PerspectiveCamera, OrthoCamera, HotloadingShader, Camera

from pyreeEngine.textures import TextureFromImage, RandomRGBATexture

import math
import time

import numpy as np
import quaternion

from OpenGL.GL import *
from OpenGL.GL import shaders

from pathlib import Path

from viddecoder.vidtexture import VideoTexture

import mido

import random

from pyutil.img import imgAnim
from pyutil.clk import Clkdiv


from pyreeEngine.objloader import ObjLoader

from pyutil.filter import PT1

class DuckGen():
    duckvertlist = ObjLoader(Path("res/couch/duck.obj")).verts
    verts = []
    for l in duckvertlist:
        verts += l

    @staticmethod
    def newDuckModel():
        newModel = ModelObject()
        newModel.loadFromVerts(DuckGen.verts)

        return newModel

class DuckCarpet:
    def __init__(self):
        self.width = 4
        self.height = 4

        self.spacing = 1
        self.scale = np.array([0.1, 0.1, 0.1])*0.5

        self.duckTex = TextureFromImage(Path("res/couch/duck.png"))
        self.duckShader = HotloadingShader(Path("res/couch/duck_vert.glsl"), Path("res/couch/duck_frag.glsl"))

        self.duckcontainer = []
        self.renderlist = None

        self.genDucks()

    def randomizeRot(self):
        pass

    def changeDuckCount(self, width, height):
        self.width = width
        self.height = height

        self.genDucks()

    def genDucks(self):
        self.duckContainer = []
        for w in range(self.width * 2 + 1):
            newcont = []
            self.duckcontainer.append(newcont)
            for h in range(self.height * 2 + 1):
                x, y = w - self.width, h - self.height
                newDuck = DuckGen.newDuckModel()
                newDuck.textures = [self.duckTex.getTexture()]
                newDuck.scale = self.scale
                newDuck.uniforms["indx"] = [x, y]
                newDuck.shaderProgram = self.duckShader.getShaderProgram()
                newcont.append(newDuck)
                newDuck.pos = np.array([x * self.spacing, 0, y * self.spacing], np.float32)

        self.renderlist = []
        for l in self.duckcontainer:
            self.renderlist += l

    def getRenderList(self):
        return self.renderlist

    def tick(self, globdata):
        self.duckShader.tick()
        for duck in self.renderlist:
            duck.uniforms["time"] = globdata.time
            duck.shaderProgram = self.duckShader.getShaderProgram()



class Couch(RenderNode):
    def __init__(self, globdata):
        super(Couch, self).__init__(globdata)

        self.camera = None  # type: PerspectiveCamera
        self.duckCarpet = None

        self.floorQuad = None
        self.floorShader = None

        self.pt1 = PT1(0.1)

        self.beatAccum = 0
        self.beatPT1 = PT1(0.3)
        self.jerkPT1 = PT1(0.3)

        self.snareAccum = 0
        self.snarePT1 = PT1(0.5)

        self.scaleDiv = Clkdiv()

    def init(self):
        if self.camera is None:
            self.camera = PerspectiveCamera()
            self.camera.setPerspective(50, self.globalData.resolution[0] / self.globalData.resolution[1], 0.1, 100.)

        if self.duckCarpet is None:
            self.duckCarpet = DuckCarpet()

        if self.floorQuad is None:
            self.floorQuad = FSQuad()
            self.floorQuad.rot = quaternion.from_euler_angles([math.pi/2, math.pi/2, 0])
            self.floorQuad.scale = np.array([1, 1, 1])*10
        if self.floorShader is None:
            self.floorShader = HotloadingShader(Path("res/couch/floor_vert.glsl"), Path("res/couch/floor_frag.glsl"))
            self.floorQuad.shaderProgram = self.floorShader.getShaderProgram()


        #self.midiIn = mido.open_input("Scarlett 2i4 USB:Scarlett 2i4 USB MIDI 1 16:0")


    def getData(self):
        return {
            "duckCarpet": self.duckCarpet
        }

    def setData(self, data):
        pass#self.duckCarpet = data["duckCarpet"]

    @execIn("run")
    def run(self):
        """for msg in self.midiIn.iter_pending():
            if msg.type == "note_on":
                print(msg.note)
                if(msg.note == 36):
                    self.duckModel.rot = quaternion.from_euler_angles(random.random()*360, random.random()*360, random.random()*360)
                    s = self.pt1.set = random.random()*0.1 + 0.05"""
        self.register()

        self.duckCarpet.tick(self.globalData)

        self.floorQuad.uniforms["time"] = self.globalData.time
        self.floorShader.tick()
        self.floorQuad.shaderProgram = self.floorShader.getShaderProgram()

        if self.globalData.resChanged:
            self.camera.setPerspective(50, self.globalData.resolution[0]/self.globalData.resolution[1], 0.1, 10.)

        ## Uniforms

        if self.globalData.beat[0]:
            self.beatAccum += 1
            self.beatPT1.set = self.beatAccum
            self.jerkPT1.cur = 1

            self.rand1 = random.random()
            self.rand2 = random.random()
            self.rand3 = random.random()

        if self.globalData.beat[1]:
            self.snareAccum += 1
            self.snarePT1.set = self.snareAccum


        self.beatPT1.tick(self.globalData.dt)
        self.jerkPT1.tick(self.globalData.dt)
        self.snarePT1.tick(self.globalData.dt)

        for duck in self.duckCarpet.renderlist:
            duck.uniforms["beat"] = self.beatPT1.cur
            duck.uniforms["jerk"] = self.jerkPT1.cur
            duck.uniforms["snare"] = self.snarePT1.cur

            duck.rot *= quaternion.from_euler_angles(np.array([random.random(), random.random(), random.random()] - np.ones(3)*0.5)*0.1)
            duck.scale += np.array([random.random(), random.random(), random.random()] - np.ones(3)*0.5)*0.0001
            duck.pos += np.array([random.random(), random.random(), random.random()] - np.ones(3)*0.5)*0.0001

        if self.scaleDiv.tick(100):
            for duck in self.duckCarpet.renderlist:
                duck.scale = np.array([0.1, 0.1, 0.1]) * random.random()

        ##



        orbitradius = 3
        orbitspeed = 0.05
        orbphase = self.globalData.time*orbitspeed*math.pi*2.
        #orbphase = math.pi*0.5
        self.camera.lookAt(np.array([math.cos(orbphase*1)*orbitradius, 2., math.sin(orbphase)*orbitradius]), np.array([0., 0.5 , 0.]), np.array([0., 1., 0.]))

        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

        #glBindFramebuffer(GL_FRAMEBUFFER, 0)

        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)

        self.render([self.floorQuad] + self.duckCarpet.getRenderList(), self.camera, None)


__nodeclasses__ = [Couch]
