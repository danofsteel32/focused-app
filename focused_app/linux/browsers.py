# browsers.py

import json
import re
import sqlite3
from pathlib import Path
from subprocess import check_output
from .models import Browser

# Stolen from Django
regex = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$", re.IGNORECASE)


def is_url(active_tab: str) -> bool:
    return True if regex.match(active_tab) else False


def get_active_tab(browser: Browser, sandboxed: bool):
    """Returns url of active browser tab or raises ValueError if can"t find"""
    active_tab = None
    if browser is Browser.CHROMIUM or browser is Browser.GOOGLE_CHROME:
        session_file = get_chrome_session_file(browser, sandboxed)
        active_tab = get_chrome_active_tab(session_file)
    elif browser is Browser.FIREFOX:
        active_tab = get_firefox_active_tab(sandboxed)
    elif browser is Browser.QUTEBROWSER:
        active_tab = get_qutebrowser_active_tab()
    if not active_tab:
        raise ValueError(f"Couldn't get active tab for browser: {browser}")
    if is_url(active_tab):
        return active_tab
    else:
        raise ValueError(f"Not a valid url: {active_tab}")


def get_chrome_session_file(browser: Browser, sandboxed: bool) -> Path:
    if browser is Browser.CHROMIUM:
        if sandboxed:
            sessions_dir = (".var/app/org.chromium.Chromium/config/"
                            "chromium/Default/Sessions")
        else:
            sessions_dir = ".config/chromium/Default/Sessions"
    elif browser is Browser.GOOGLE_CHROME:
        sessions_dir = (".config/google-chrome/Default/Sessions")

    sessions_path = Path.home() / sessions_dir
    all_files = [f for f in sessions_path.iterdir() if "Session" in f.name]
    sorted_by_atime = sorted(all_files, key=lambda x: x.stat().st_mtime,
                             reverse=True)
    return sorted_by_atime[0]


def get_chrome_active_tab(session_file: Path):
    # TODO figure out why this doesn't work sometimes
    tabs = check_output(["chrome-session-dump", "-active", str(session_file)], text=True)
    active_tab = tabs.strip()
    if is_url(active_tab):
        return active_tab
    tabs_json = check_output(["chrome-session-dump", "-json", str(session_file)], text=True)
    windows = json.loads(tabs_json)["windows"]
    for w in windows:
        for t in w["tabs"]:
            if t["active"]:
                return t["url"]
    raise ValueError("chrome-session-dump no url found")


def get_firefox_active_tab(sandboxed: bool):
    if sandboxed:
        ff_dir = Path.home() / ".var/app/org.mozilla.firefox/.mozilla/firefox/"
    else:
        ff_dir = Path.home() / ".mozilla/firefox"
    for f in ff_dir.iterdir():
        if f.match("*.default-release"):
            places_db = f / "places.sqlite"
    conn = sqlite3.connect(places_db)
    cur = conn.cursor()
    cur.execute("""SELECT place_id
                     FROM moz_historyvisits
                 ORDER BY visit_date
                     DESC LIMIT 1""")
    place_id = cur.fetchone()[0]
    cur.execute("""SELECT url
                     FROM moz_places
                    WHERE id = ?""", (place_id,))
    active_tab = cur.fetchone()[0]
    conn.close()
    return active_tab


def get_qutebrowser_active_tab():
    history_db = Path.home() / ".local/share/qutebrowser/history.sqlite"
    conn = sqlite3.connect(history_db)
    cur = conn.cursor()
    cur.execute("""SELECT url
                     FROM History
                 ORDER BY atime
                     DESC LIMIT 1""")
    active_tab = cur.fetchone()[0]
    conn.close()
    return active_tab
