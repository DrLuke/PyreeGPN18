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


from pyreeEngine.objloader import ObjLoader

class Empty(RenderNode):
    def __init__(self, globdata):
        super(Empty, self).__init__(globdata)

        pass

    def init(self):
        pass

    def getData(self):
        pass

    def setData(self, data):
        pass

    @execIn("run")
    def run(self):
        self.register()

        self.render([], Camera(), None)


__nodeclasses__ = [Empty]
