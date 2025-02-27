import os
import platform

if "MicroPython" not in platform.platform():
    ASSET_PATH = f"{os.getcwd()}/"  # noqa: PTH109

else:
    apps = os.listdir("/apps")
    path = ""
    ASSET_PATH = "apps/"

    if "github_user_tildagon_particle_man" in apps:
        ASSET_PATH = "/apps/github_user_tildagon_particle_man/"

    if "pacman" in apps:
        ASSET_PATH = "apps/particle_man/"
