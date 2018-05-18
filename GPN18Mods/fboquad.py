from pyreeEngine.node import RenderNode, BaseNode, signalInput, signalOutput, execOut, execIn
from pyreeEngine.basicObjects import ModelObject, FSQuad
from pyreeEngine.engine import *
from pyreeEngine.textures import *

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

from pyutil import *
from pyutil.filter import PT1


from pyreeEngine.objloader import ObjLoader

class FBOQuad(RenderNode):
    def __init__(self, globdata):
        super(FBOQuad, self).__init__(globdata)

        self.fsQuad = FSQuad()

    def init(self):
        self.shader = HotloadingShader(Path("res/default_vert.glsl"), Path("res/glsl/dn.glsl"))

        self.beatAccum = 0
        self.beatPT1 = PT1(0.3)
        self.jerkPT1 = PT1(0.3)

        self.rand1 = random.random()
        self.rand2 = random.random()
        self.rand3 = random.random()

        self.dntex = TextureFromImage(Path("res/pl/dn.png"))

    def getData(self):
        pass

    def setData(self, data):
        pass

    @execIn("run")
    def run(self):
        self.register()

        self.shader.tick()
        self.fsQuad.shaderProgram = self.shader.getShaderProgram()

        self.fsQuad.textures = [self.dntex.getTexture(), self.globalData.FBO.texture]

        ## Uniforms

        self.fsQuad.uniforms["time"] = self.globalData.time*0.5

        if self.globalData.beat[0]:
            self.beatAccum += 1
            self.beatPT1.set = self.beatAccum
            self.jerkPT1.cur = 1

            self.rand1 = random.random()
            self.rand2 = random.random()
            self.rand3 = random.random()

        self.beatPT1.tick(self.globalData.dt)
        self.jerkPT1.tick(self.globalData.dt)

        self.fsQuad.uniforms["beat"] = self.beatPT1.cur
        self.fsQuad.uniforms["jerk"] = self.jerkPT1.cur
        self.fsQuad.uniforms["rand1"] = self.rand1
        self.fsQuad.uniforms["rand2"] = self.rand2
        self.fsQuad.uniforms["rand3"] = self.rand3


        ##

        glClear(GL_DEPTH_BUFFER_BIT)
        self.render([self.fsQuad], Camera(), None)


__nodeclasses__ = [FBOQuad]