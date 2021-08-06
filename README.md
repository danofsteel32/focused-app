# Focused App

Get the currently focused app/window on your desktop and the context on what that app is currently doing.
### Examples
- If focused app is browser return the url of the active tab.
- If using a PDF viewer or image viewer return the path to the file being viewed.

Then you can extend it to do whatever you want with that info.

## Roadmap
Support all of the major Linux Desktops on Wayland and X11. X11 should be easier because of xdotool and xprop. It would also be cool to create a testing framework
based on kvm/ansible to enable spinning up a virtual machine for each desktop. [ldtp](https://ldtp.freedesktop.org/wiki/) is pretty cool but hasn't been updated in years and doesn't support all of the desktop evironments. Or maybe it's easier to have one VM that has all the desktops installed and just script it to login, run tests, logout in a loop. 

## Prior Art
[ActivityWatch](https://github.com/ActivityWatch/aw-watcher-window) is a really cool project that has some of the functionality I'm going for but without support for finding the file currently being viewed in the active window.

## Project Values
- Keep dependencies to a minimum
