#!/home/dan/.venv/remember/bin/python
from pathlib import Path
from typing import List, Union
from platform import system as get_system




def get_platform_context(system: str = None) -> models.PlatformContext:
    if not system:
        system = get_system()
    if system == "Linux":
        platform = models.Platform.LINUX
        open_windows = linux.get_open_windows()
        clipboard_provider = linux.get_clipboard_tool()
        desktop = linux.get_desktop()
        display_server = linux.get_display_server()
        return models.PlatformContext(platform=platform, open_windows=open_windows,
                                      clipboard_provider=clipboard_provider,
                                      linux_desktop=desktop,
                                      linux_display_server=display_server)

    elif system == "Darwin":
        platform = models.Platform.DARWIN
        raise ValueError("Darwin not supported yet")

    elif system == "Windows":
        platform = models.Platform.WINDOWS
        raise ValueError("Windows not supported yet")

def get_selected_text(platform: models.Platform, clipboard_provider: models.ClipboardProvider) -> str:
    if platform is models.Platform.LINUX:
        return linux.get_selected_text(clipboard_provider)
    else:
        raise ValueError("Unsupported Platform")


def get_selected_source(platform: models.Platform, focused_window: models.Window) -> Union[str, Path]:
    app = focused_window.app
    title = focused_window.title
    if platform is models.Platform.LINUX:
        if app in BROWSERS:
            active_tab = linux.get_active_tab(app)
            return active_tab
        elif app in PDF_VIEWERS:
            pdf_file = linux.get_pdf_file(app, title)
            return pdf_file
        else:
            return app
    else:
        raise ValueError("Unsupported Platform")

def get_source_type(focused_window: models.Window) -> models.ContentType:
    if focused_window.app in BROWSERS:
        return models.ContentType.URL
    elif focused_window.app in PDF_VIEWERS:
        return models.ContentType.PDF
    else:
        return models.ContentType.TEXT

def get_focused_window(windows: List[models.Window]) -> models.Window:
    return next(w for w in windows if w.focused)

def get_memoria(context: models.PlatformContext, focused_window: models.Window = None) -> models.Memoria:
    if not focused_window:
        focused_window = get_focused_window(context.open_windows)
    selected_text = get_selected_text(context.platform, context.clipboard_provider)
    source_type = get_source_type(focused_window)
    selected_source = get_selected_source(context.platform, focused_window)
    m = models.Memoria(window=focused_window, source=selected_source,
                       selected_text=selected_text, source_type=source_type)
    return m


def main(context: models.PlatformContext = None, memoria: models.Memoria = None):
    # First establish that we're on a supported platform
    if not context:
        try:
            context = get_platform_context()
        except ValidationError as e:
            raise(e)
    # Then validate memoria 
    if not memoria:
        try:
            memoria = get_memoria(context)
        except ValidationError as e:
            raise(e)
    print(context)
    print(memoria)
    with open("/tmp/remember.log", "w+") as f:
        f.write(str(context) + "\n")
        f.write(str(memoria))
    return memoria

def test_platform_context():
        platform = models.Platform.LINUX
        open_windows = linux.get_open_windows()
        clipboard_provider = linux.get_clipboard_tool()
        desktop = linux.get_desktop()
        display_server = linux.get_display_server()
        return models.PlatformContext(platform=platform, open_windows=open_windows,
                                      clipboard_provider=clipboard_provider,
                                      linux_desktop=desktop, linux_display_server=display_server)

def test_memoria():
    selected_text=get_selected_text(models.Platform.LINUX, models.ClipboardProvider.WL_PASTE)
    return models.Memoria(window=models.Window(app="evince", title="1903.06763.pdf", focused=True),
                          source_type=models.ContentType.PDF, selected_text=selected_text,
                          source=Path("/home/dan/code/remember/test_data/pdf/1903.06763.pdf"))

if __name__ == "__main__":
    main()
