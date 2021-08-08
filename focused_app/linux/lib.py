""" linux/lib.py """

import ast
import os
import psutil

from pathlib import Path
from subprocess import check_output
from typing import Dict, List, Optional, Set

from ..common.models import Window, AppRole
from . import models


def get_pid_open_files(pid: int) -> List[Path]:
    for p in psutil.process_iter(["pid", "open_files"]):
        if p.info["pid"] == pid:
            return [Path(f.path) for f in p.info["open_files"]]
    return []


def get_ereader_files(pid: int, extensions: Set[str]) -> List[Path]:
    open_files = get_pid_open_files(pid)
    files = [f for f in open_files if f.name.split(".")[-1] in extensions]
    if not files:
        raise Exception("No files")
    return files


def get_filepath_from_title(title: str, extensions: Set[str]) -> Optional[Path]:
    title_elements = title.split(" ")
    for n, i in enumerate(title_elements):
        # No spaces in filename
        if i.split(".")[-1] in extensions:
            # Already have full path
            if Path(i).exists():
                return Path(i)
            # Gotta find full path
            else:
                for p in Path.home().rglob(f"*.{i.split('.')[-1]}"):
                    if p.name == i:
                        return p / i
        # Spaces in filename
        path_fragment = i.rsplit("/", 1)[0]
        if Path(path_fragment).exists():
            file_name = i.rsplit("/", 1)[1]
            for j in title_elements[n + 1:]:
                # build up filename str until hit extension
                file_name += f" {j}"
                if j.split(".")[-1] in extensions:
                    return Path(path_fragment) / file_name
    # Couldn't get filepath
    return None


def get_file_from_window(window: Window) -> Optional[Path]:

    if window.role is AppRole.E_READER:
        extensions = {"pdf", "epub"}
        files = get_ereader_files(window.pid, extensions)
        if len(files) > 1:
            raise Exception("Too many files to pick from")
        return files[0]

    elif window.role is AppRole.IMAGE_VIEWER:
        extensions = {"jpg", "jpeg", "png"}
        image_file = get_filepath_from_title(window.title, extensions)
        return image_file

    elif window.role is AppRole.CODE_EDITOR:
        # TODO: support neovim, vscode
        print("Needs to be implemented")
        return None
    else:
        raise ValueError(f"{window.role} doesn't make sense for get_file_from_pid()")
    return None


def mock_focused_app(app: str) -> Window:
    windows = get_all_windows()
    for w in windows:
        if w.app == app:
            w.focused = True
            return w


def get_desktop(desktop: str = None) -> models.Desktop:
    while not desktop:
        desktop = os.getenv("XDG_CURRENT_DESKTOP")
        desktop = os.getenv("XDG_SESSION_DESKTOP")
    if not desktop:
        raise ValueError("Could not detect desktop")
    case = {
            "gnome": models.Desktop.GNOME,
            "pop-wayland": models.Desktop.GNOME,
            "pop:gnome": models.Desktop.GNOME,
            "ubuntu:gnome": models.Desktop.GNOME,
    }
    mapped_desktop = case.get(desktop.lower(), None)
    if mapped_desktop:
        return mapped_desktop
    else:
        raise ValueError(f"{desktop}")


def get_display_server() -> models.DisplayServer:
    if os.getenv("WAYLAND_DISPLAY"):
        return models.DisplayServer.WAYLAND
    elif os.getenv("DISPLAY"):
        return models.DisplayServer.X11
    else:
        raise ValueError("Could not detect display server")


def get_app_role(app: str) -> Optional[str]:
    for role in models.role_maps:
        if app in models.role_maps[role]:
            return AppRole(role)
    return None


def create_window(window: Dict) -> Window:
    sandboxed = False
    if window["sandboxed_id"]:
        sandboxed = True
    app = window["class"].lower()
    role = get_app_role(app)
    return Window(app=app, title=window["title"],
                  pid=window["pid"], focused=window["focused"],
                  sandboxed=sandboxed, role=role)


def get_all_windows() -> List[Window]:
    display_server = get_display_server()
    if display_server is models.DisplayServer.X11:
        # Handle using xprop
        print("Need to implement X11 support")
        return []
    desktop = get_desktop()
    if desktop is models.Desktop.GNOME:
        return get_gnome_all_windows()


def get_gnome_all_windows() -> List[Window]:
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
    return [create_window(window) for window in windows]
