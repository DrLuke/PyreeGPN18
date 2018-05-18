from pyreeEngine.node import RenderNode, BaseNode, signalInput, signalOutput, execOut, execIn
from pyreeEngine.basicObjects import ModelObject, FSQuad
from pyreeEngine.engine import *

from pyreeEngine.textures import TextureFromImage, RandomRGBATexture

import math
import time

import numpy as np
import quaternion

from OpenGL.GL import *
from OpenGL.GL import shaders

import pyutil
from pyutil import clk
from pyutil.filter import PT1

from pathlib import Path

from viddecoder.vidtexture import VideoTexture

import random

from pythonlpd8.lpd8mido import LPD8DeviceMido

class SwitchAnim:
    def __init__(self):
        self.prog = 0
        self.finished = False

    def start(self):
        self.finished = False
        self.prog = 0

    def tick(self, dt) -> bool:
        if self.finished:
            return False
        self.prog += dt*0.5
        if self.prog >= 1.:
            self.prog = 0.
            self.finished = True
        if self.prog > 0.5:
            return True
        return False


class PremiumLounge(RenderNode):
    def __init__(self, globdata):
        super(PremiumLounge, self).__init__(globdata)

        self.fsQuad = None
        self.fsShader = None
        self.vidTex = None
        self.vidFPS = clk.FPS()

        self.logoQuad = None
        self.logoQuadShader = None

        self.logoCam = OrthoCamera()

        self.logoFPS = clk.FPS()
        self.logoAnim = SwitchAnim()

        self.currLogo = None
        self.nextLogo = None

        """self.videoPool = [
            Path("res/vid/MiamiAerial.mp4"),
            Path("res/vid/tokyo_scale.webm"),
            Path("res/vid/osaka1.webm"),
            Path("res/vid/osaka2.webm"),
            Path("res/vid/osaka3.webm"),
            Path("res/vid/newyork.mp4"),
            Path("res/vid/miami2.mp4")
        ]
        """
        self.videoPool = [
            Path("res/vid/space.mp4")
        ]


        self.logoPool = [
            Path("res/pl/lounge_logo.png"),
            Path("res/pl/brain.png"),
            Path("res/pl/entropia.png"),
            Path("res/pl/ccc.png"),
            Path("res/pl/pyree.png"),
            Path("res/pl/dn.png"),
            #Path("res/poltergeist_sq2.png"),
        ]


        self.logoTextures = []

        for texPath in self.logoPool:
            self.logoTextures.append(TextureFromImage(texPath))
        self.currLogo = random.choice(self.logoTextures)
        self.nextLogo = random.choice(self.logoTextures)

        self.beatAccum = 0
        self.beatPT1 = PT1(0.3)
        self.jerkPT1 = PT1(0.3)

        self.rand1 = random.random()
        self.rand2 = random.random()
        self.rand3 = random.random()
        self.rand4 = random.random()
        self.rand5 = random.random()
        self.rand6 = random.random()

        self.lpd8 = None

        self.pad = None


    def init(self):
        if self.fsQuad is None:
            self.fsQuad = FSQuad()
            self.fsQuad.pos = np.array([0, 0, 1.])
        if self.fsShader is None:
            self.fsShader = HotloadingShader(Path("res/default_vert.glsl"), Path("res/pl/quad_frag.glsl"))
            self.fsQuad.shaderProgram = self.fsShader.getShaderProgram()
        if self.vidTex is None:
            self.vidTex = VideoTexture(random.choice(self.videoPool))
        if self.logoQuad is None:
            self.logoQuad = FSQuad()
        if self.logoQuadShader is None:
            self.logoQuadShader = HotloadingShader(Path("res/default_vert.glsl"), Path("res/renderTex1.glsl"))
            self.logoQuad.shaderProgram = self.logoQuadShader.getShaderProgram()
        if not self.logoTextures:
            pass    # TODO: Load textures

        if self.lpd8 is None:
            time.sleep(2)
            self.lpd8 = LPD8DeviceMido()

        for i in range(8):
            self.lpd8.addPadCB(0, i, self.knobCB)
            self.lpd8.addKnobCB(0, i, self.knobCB)

        if self.pad is None:
            self.pad = [0] * 8


    def getData(self):
        a = {}
        a["lpd8"] = self.lpd8
        a["pad"] = self.pad

        for i in range(8):
            self.lpd8.removePadCB(0, i, self.padCB)
            self.lpd8.removeKnobCB(0, i, self.knobCB)
        return a

    def setData(self, data):
        if "lpd8" in data:
            self.lpd8 = data["lpd8"]
        if "pad" in data:
            self.pad = data["pad"]

    def padCB(self, programNum: int, padNum: int, knobNum: int, value: int, noteon: int, noteoff: int, cc: int,
               pc: int):
        print("padcb")

    def knobCB(self, programNum: int, padNum: int, knobNum: int, value: int, noteon: int, noteoff: int, cc: int, pc: int):
        if knobNum is not None:
            self.pad[knobNum] = value

    def nextVideo(self):
        self.vidTex = VideoTexture(random.choice(self.videoPool))

    @execIn("run")
    def run(self):
        self.register()

        self.lpd8.tick()

        self.fsShader.tick()
        self.fsQuad.shaderProgram = self.fsShader.getShaderProgram()

        if self.vidFPS.tick(25, self.globalData.dt):
            if not self.vidTex.fetchNext():
                self.nextVideo()
            self.fsQuad.textures = [self.vidTex.getTexture(), self.globalData.FBO.texture]

        glDisable(GL_DEPTH_TEST)

        self.render([self.fsQuad], Camera(), None)

        if self.logoFPS.tick(0.1, self.globalData.dt):
            self.logoAnim.start()
            self.nextLogo = random.choice(self.logoTextures)

        if self.logoAnim.tick(self.globalData.dt):
            if not self.currLogo == self.nextLogo:
                self.currLogo = self.nextLogo

        if self.currLogo is not None:
            self.logoQuad.textures = [self.currLogo.getTexture()]

        ## Uniforms

        if self.globalData.beat[0]:
            self.beatAccum += 1
            self.beatPT1.set = self.beatAccum
            self.jerkPT1.cur = 1

            self.rand1 = random.random()
            self.rand2 = random.random()
            self.rand3 = random.random()
            self.rand4 = random.random()
            self.rand5 = random.random()
            self.rand6 = random.random()

        self.beatPT1.tick(self.globalData.dt)
        self.jerkPT1.tick(self.globalData.dt)

        self.fsQuad.uniforms["beat"] = self.beatPT1.cur
        self.fsQuad.uniforms["jerk"] = self.jerkPT1.cur

        self.fsQuad.uniforms["rand1"] = self.rand1
        self.fsQuad.uniforms["rand2"] = self.rand2
        self.fsQuad.uniforms["rand3"] = self.rand3
        self.fsQuad.uniforms["rand4"] = self.rand4
        self.fsQuad.uniforms["rand5"] = self.rand5
        self.fsQuad.uniforms["rand6"] = self.rand6

        for i in range(8):
            self.fsQuad.uniforms["pad" + str(i)] = self.pad[i]


        self.fsQuad.uniforms["time"] = self.globalData.time

        ##

        self.logoQuad.rot = quaternion.from_euler_angles(np.array([0, ((self.logoAnim.prog + 0.5) % 1. - 0.5) * math.pi, 0]))

        #if self.currLogo == self.logoTextures[5]:
        #    self.logoCam.setOrtho(2.5, self.globalData.resolution[0]/self.globalData.resolution[1], 0.1, 10.)
        #else:
        self.logoCam.setOrtho(5., self.globalData.resolution[0] / self.globalData.resolution[1], 0.1, 10.)
        self.logoCam.lookAt(np.array([0., 0., 1.]), np.array([0., 0., 0.]), np.array([0, 1., 0.]))

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.render([self.logoQuad], self.logoCam, None)

        glDisable(GL_BLEND)


__nodeclasses__ = [PremiumLounge]
