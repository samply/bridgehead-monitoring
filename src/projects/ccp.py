import sys, pathlib
from importlib import import_module

pathlib.Path(__file__).parent.resolve()

for p in sys.path:
    print(p)

blaze = import_module("projects.components.blaze")

services = []

services += blaze.services




