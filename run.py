from focused_app import linux, get_focused_app, get_focused_context


def print_linux_windows():
    for w in linux.get_all_windows():
        print(w)

print(get_focused_app())
print(get_focused_context())
