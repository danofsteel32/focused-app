# Focused App

Get the currently focused app/window on your desktop and the context on what that app is currently doing.

## TODO
- split get file from window into sep funcs
- platform -> approle -> app -> func
  - make sure we're only checking if role,app, once
- more tests
  - Mock data for everything, known sessions files, history dbs, filenames with + w/o spaces
  - Run tests without needing to have any windows open
  - test poorly escaped strings in gnome windows func


### Examples
- If focused app is browser return the url of the active tab.
- If using a PDF viewer or image viewer return the path to the file being viewed.

Then you can extend it to do whatever you want in your own scripts.

## Lint and Test
`poetry run lint`
`poetry run test`

## Roadmap
Supporting my workflow (Gnome Wayland, Evince, Chromium/Qutebrowser, imv) is main priority but will work to support other apps/platforms if there's demand.

## Prior Art
[ActivityWatch](https://github.com/ActivityWatch/aw-watcher-window) is a really cool project that can get focused windows but without support for finding the file currently being viewed in the active window. Also way beyond the scope of this project.

## Project Values
- Keep dependencies to a minimum
- Simple interface
