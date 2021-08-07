from focused_app


def print_linux_windows():
    for w in linux.get_all_windows():
        print(w)

print(mock_focused_app("evince"))
#print(get_focused_app())
#print(get_focused_context())

