import os
from utils.path_normalizer import PathNormalizer

class IconManager:
    SIMPLESTUDIO_ICON_PATH = PathNormalizer.resource_path(os.path.join("icons","favicon.ico"))
    INFO_ICON_LIGHT = PathNormalizer.resource_path(os.path.join("icons","info_light.png"))
    INFO_ICON_DARK = PathNormalizer.resource_path(os.path.join("icons","info_dark.png"))