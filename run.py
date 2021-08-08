from focused_app import get_focused_app, get_focused_context
from focused_app.linux import lib as linux

# print(linux.get_all_windows())

evince = linux.mock_focused_app("evince")
f = linux.get_file_from_window(evince)
print(f)
