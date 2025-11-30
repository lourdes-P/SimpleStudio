import os
from utils.path_normalizer import PathNormalizer

class IconManager:
    SIMPLESTUDIO_ICON_PATH_WIN32 = PathNormalizer.resource_path(os.path.join("icons","favicon.ico"))
    SIMPLESTUDIO_ICON_PATH_DARWIN_LINUX = PathNormalizer.resource_path(os.path.join("icons","icon-180x180.png"))
    INFO_ICON_LIGHT = PathNormalizer.resource_path(os.path.join("icons","info_light.png"))
    INFO_ICON_DARK = PathNormalizer.resource_path(os.path.join("icons","info_dark.png"))