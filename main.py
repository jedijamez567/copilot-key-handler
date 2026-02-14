#!/usr/bin/env python3
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import os
import re


def get_active_terminal_cwd(user):
    """Get the CWD of the focused terminal tab from the window title."""
    try:
        # Get the active window ID
        win_id = subprocess.check_output(
            ['sudo', '-u', user, 'bash', '-c',
             'DISPLAY=:0 xdotool getactivewindow'],
        ).decode().strip()

        # Check if the active window is a terminal
        wm_class = subprocess.check_output(
            ['xprop', '-id', win_id, 'WM_CLASS'],
            env={'DISPLAY': ':0'},
        ).decode().strip().lower()

        if 'terminal' not in wm_class and 'kitty' not in wm_class and 'alacritty' not in wm_class:
            return None

        # Get the window title (e.g. "jedijamez@JedijamezLaptop: ~/dev/keyd")
        title = subprocess.check_output(
            ['sudo', '-u', user, 'bash', '-c',
             'DISPLAY=:0 xdotool getactivewindow getwindowname'],
        ).decode().strip()

        # Parse the directory from the title (format: "user@host: /path" or "user@host: ~/path")
        match = re.search(r':\s+(~?/.*)$', title)
        if match:
            path = match.group(1)
            # Expand ~ to home directory
            path = path.replace('~', f'/home/{user}')
            if os.path.isdir(path):
                return path

        return None
    except Exception:
        return None


device = InputDevice('/dev/input/event4')
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        key = categorize(event)
        if 'KEY_F23' in key.keycode and key.keystate == key.key_down:
            user = os.environ.get('SUDO_USER', 'jedijamez')
            uid = subprocess.check_output(['id', '-u', user]).decode().strip()

            cwd = get_active_terminal_cwd(user)
            if not cwd:
                cwd = f'/home/{user}'

            workdir_flag = f'--working-directory={cwd}'
            subprocess.Popen([
                'sudo', '-u', user,
                'bash', '-c',
                f'DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{uid}/bus gnome-terminal {workdir_flag} -- /home/jedijamez/.local/bin/claude'
            ])
