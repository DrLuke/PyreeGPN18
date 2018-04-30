from pyreeEngine.engine import Engine, LaunchOptions

from pathlib import Path

if __name__ == "__main__":
    opt = LaunchOptions()
    opt.projectPath = Path("gpn18.json")
    eng = Engine(opt)