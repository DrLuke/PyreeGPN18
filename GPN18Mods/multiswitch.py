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

from pathlib import Path

from viddecoder.vidtexture import VideoTexture

from pythonlpd8.lpd8mido import LPD8DeviceMido

from pyutil import artnet

import mido

class MultiSwitch(RenderNode):
    def __init__(self, globdata):
        super(MultiSwitch, self).__init__(globdata)

        self.lpd8 = LPD8DeviceMido()

        self.lpd8.setPadToggle(0, 7, True)
        for i in range(8):
            self.lpd8.addPadCB(0, i, self.padCBprog, pc=True, note=False)
            self.lpd8.addPadCB(0, i, self.padCBnote)

        self.currentProgram = 0
        self.currentEffect = 0

        self.beatMute = False

        globdata.FBO = RegularFramebuffer(globdata.resolution[0], globdata.resolution[1])

        self.artnet = artnet.ArtNetReceiver(8)
        self.artnet.clb = self.artnetCB

        self.midi = None
        try:
            self.midi = mido.open_input("Scarlett 2i4 USB:Scarlett 2i4 USB MIDI 1 24:0")
        except:
            self.midi = None
            print("Failed to open MIDI")

        self.globalData.beat = [0, 0, 0, 0]


    def init(self):
        self.fsQuad = FSQuad()
        self.fsQuadShader = HotloadingShader(Path("res/default_vert.glsl"), Path("res/renderTex1.glsl"))
        self.fsQuad.shaderProgram = self.fsQuadShader.getShaderProgram()
        self.fsQuad.textures = [self.globalData.FBO.texture]

    def getData(self):
        pass

    def setData(self, data):
        pass

    def padCBnote(self, programNum: int, padNum: int, knobNum: int, value: int, noteon: int, noteoff: int, cc: int,
                  pc: int):
        if padNum == 7 and noteon:
            self.beatMute = True
            return
        if padNum == 7 and noteoff:
            self.beatMute = False
            return


    def padCBprog(self, programNum: int, padNum: int, knobNum: int, value: int, noteon: int, noteoff: int, cc: int, pc: int):
        if pc is not None:
            self.currentProgram = padNum

    def padCBeffects(self, programNum: int, padNum: int, knobNum: int, value: int, noteon: int, noteoff: int, cc: int, pc: int):
        if pc is not None:
            self.currentEffect = padNum

    def artnetCB(self, chan, val):
        if not self.beatMute:
            self.globalData.beat[0] = 1
            self.globalData.beat[1] = 1

    @execIn("run")
    def run(self):
        self.register()

        if self.midi is not None:
            for msg in self.midi.iter_pending():
                if msg.type == "note_on":
                    if msg.note == 36:
                        self.globalData.beat[0] = 1
                    elif msg.note == 48:
                        self.globalData.beat[1] = 1
                    elif msg.note == 24:
                        self.globalData.beat[2] = 1
                    elif msg.note == 60:
                        self.globalData.beat[3] = 1
                if msg.type == "note_off":
                    if msg.note == 12:
                        self.globalData.beat[2] = 0
                    elif msg.note == 48:
                        self.globalData.beat[3] = 0


        if self.globalData.resChanged:
            self.globalData.FBO = RegularFramebuffer(self.globalData.resolution[0], self.globalData.resolution[1])
            self.fsQuad.textures = [self.globalData.FBO.texture]

        self.fsQuadShader.tick()
        self.fsQuad.shaderProgram = self.fsQuadShader.getShaderProgram()

        self.globalData.FBO.bindFramebuffer()

        self.lpd8.tick()

        if self.currentProgram == 0:
            self.runP0()
        elif self.currentProgram == 1:
            self.runP1()
        elif self.currentProgram == 2:
            self.runP2()
        elif self.currentProgram == 3:
            self.runP3()
        elif self.currentProgram == 4:
            self.runP4()
        elif self.currentProgram == 5:
            self.runP5()

        DefaultFramebuffer().bindFramebuffer()
        if self.currentEffect == 0:
            self.render([self.fsQuad], Camera(), None)
        elif self.currentEffect == 1:
            self.runE1()
        elif self.currentEffect == 2:
            self.runE2()
        elif self.currentEffect == 3:
            self.runE3()
        elif self.currentEffect == 4:
            self.runE4()
        elif self.currentEffect == 5:
            self.runE5()

        self.globalData.beat[0] = 0
        self.globalData.beat[1] = 0

    @execOut("p0")
    def runP0(self):
        pass

    @execOut("p1")
    def runP1(self):
        pass

    @execOut("p2")
    def runP2(self):
        pass

    @execOut("p3")
    def runP3(self):
        pass

    @execOut("p4")
    def runP4(self):
        pass

    @execOut("p5")
    def runP5(self):
        pass


    @execOut("e1")
    def runE1(self):
        pass

    @execOut("e2")
    def runE2(self):
        pass

    @execOut("e3")
    def runE3(self):
        pass

    @execOut("e4")
    def runE4(self):
        pass

    @execOut("e5")
    def runE5(self):
        pass

__nodeclasses__ = [MultiSwitch]
