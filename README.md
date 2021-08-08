# Focused App

Get the currently focused app/window on your desktop and the context on what that app is currently doing.

### Examples
- If focused app is browser return the url of the active tab.
- If using a PDF viewer or image viewer return the path to the file being viewed.

Then you can extend it to do whatever you want in your own scripts.

## Deps
Getting the active tab in chromium/chrome relies on [chrome-session-dump](https://github.com/lemnos/chrome-session-dump).

## Tests to write
- chromium integration tests
- firefox history test data places.sqlite
- firefox integration tests
- qutebrowser history.sqlite test data
- qutebroswer integration tests
- test escaped strings in gnome windows func

## TODO
- split unit tests from integration tests
- all gnome wayland tests (my workflow)
- install guide (chrome-session-dump)
- document how it all works
- examples
- X11 support
- macos support safari and preview

## Roadmap
Supporting my workflow (Gnome Wayland, Evince, Chromium/Qutebrowser, imv) is main priority but will work to support other apps/platforms if there's demand. Go to version 1.0.0 once gnome wayland fully tested and have install guide and examples written.

## Prior Art
[ActivityWatch](https://github.com/ActivityWatch/aw-watcher-window) is a really cool project that can get focused windows but without support for finding the file currently being viewed in the active window. Also way beyond the scope of this project.

## Project Values
- Keep dependencies to a minimum
- Simple interface
