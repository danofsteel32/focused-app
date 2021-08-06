import ast
import os

from subprocess import check_output
from typing import Dict, List, Optional
from . import models


def get_desktop(desktop: str = None) -> models.LinuxDesktop:
    while not desktop:
        desktop = os.getenv("XDG_CURRENT_DESKTOP")
        desktop = os.getenv("XDG_SESSION_DESKTOP")
    if not desktop:
        raise ValueError("Could not detect desktop")
    case = {
            "gnome": models.LinuxDesktop.GNOME,
            "pop-wayland": models.LinuxDesktop.GNOME,
            "pop:gnome": models.LinuxDesktop.GNOME,
            "ubuntu:gnome": models.LinuxDesktop.GNOME,
    }
    mapped_desktop = case.get(desktop.lower(), None)
    if mapped_desktop:
        return mapped_desktop
    else:
        raise ValueError(f"{desktop}")


def get_display_server() -> models.LinuxDisplayServer:
    if os.getenv("WAYLAND_DISPLAY"):
        return models.LinuxDisplayServer.WAYLAND
    elif os.getenv("DISPLAY"):
        return models.LinuxDisplayServer.X11
    else:
        raise ValueError("Could not detect display server")


def get_app_role(app: str) -> Optional[str]:
    for role in models.role_maps:
        if app in models.role_maps[role]:
            return models.AppRole(role)
    return None


def create_linux_window(window: Dict) -> models.LinuxWindow:
    sandboxed = False
    if window["sandboxed_id"]:
        sandboxed = True
    app = window["class"].lower()
    role = get_app_role(app)
    return models.LinuxWindow(app=app, title=window["title"],
                              pid=window["pid"], focused=window["focused"],
                              sandboxed=sandboxed, role=role)


def get_all_windows() -> List[models.LinuxWindow]:
    display_server = get_display_server()
    if display_server is models.LinuxDisplayServer.X11:
        # Handle using xprop
        print("Need to implement X11 support")
        return []
    desktop = get_desktop()
    if desktop is models.LinuxDesktop.GNOME:
        return get_gnome_all_windows()


def get_gnome_all_windows() -> List[models.LinuxWindow]:
    gdbus_args = [
        "gdbus", "call", "--session",
        "--dest", "org.gnome.Shell",
        "--object-path", "/org/gnome/Shell",
        "--method", "org.gnome.Shell.Eval"
    ]
    js_chain = ("global.get_window_actors().map(w=>w.meta_window)"
                ".map(w=>({class: w.get_wm_class(), title: w.get_title(),"
                "focused: w.has_focus(), pid: w.get_pid(), role: w.get_role(),"
                "sandboxed_id: w.get_sandboxed_app_id()}))")
    cmd = gdbus_args + [js_chain]
    raw = check_output(cmd, text=True).strip()
    fix_true = raw.replace("true", "True")
    fix_false = fix_true.replace("false", "False")
    cleaned = fix_false.replace("null", "None")
    to_pyobj = ast.literal_eval(cleaned)
    windows = ast.literal_eval(to_pyobj[1])
    return [create_linux_window(window) for window in windows]
