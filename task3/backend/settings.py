import importlib
import os
from pathlib import Path
from decouple import config


try:
    SETTINGS_MODULES = importlib.import_module(f"{os.environ.get('APP', config('APP'))}.settings")
except ModuleNotFoundError:
    SETTINGS_MODULES = importlib.import_module("backend.default_settings")

MODULES_NAMES = [
    module
    for module in SETTINGS_MODULES.__dict__
    if not module.startswith("_") and module.isupper()
]
globals().update({items: getattr(SETTINGS_MODULES, items) for items in MODULES_NAMES})