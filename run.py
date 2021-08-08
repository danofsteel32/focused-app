from focused_app import get_focused_app, get_focused_context
from focused_app.linux import lib as linux

for w in linux.get_all_windows():
    print(w)

