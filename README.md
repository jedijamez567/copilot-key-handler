# Copilot Key Handler

Remaps the Windows Copilot key (found on ASUS ROG and other modern laptops) to launch [Claude Code](https://docs.anthropic.com/en/docs/claude-code) on Linux.

## How it works

The Copilot key generates a `Shift+Super+F23` keypress at the hardware level. This daemon listens for the `KEY_F23` event using Python's `evdev` library and opens a GNOME Terminal running Claude Code.

If a terminal window is focused when the key is pressed, Claude Code opens in that terminal's working directory. Otherwise, it opens in the user's home directory.

## Dependencies

- Python 3.12+
- [evdev](https://pypi.org/project/evdev/)
- `xdotool`
- `xprop` (part of `x11-utils`)
- GNOME Terminal

## Installation

```bash
# Install system dependencies
sudo apt install xdotool x11-utils

# Install Python dependencies
pip install evdev

# Install the systemd service
./install.sh
```

## Usage

Once installed, the service runs automatically on boot. Press the Copilot key to launch Claude Code.

To manually start/stop the service:

```bash
sudo systemctl start copilot-key-handler
sudo systemctl stop copilot-key-handler
```

To check the service status:

```bash
sudo systemctl status copilot-key-handler
```

## Configuration

The script currently expects:

- Keyboard input device at `/dev/input/event4` (ASUS Keyboard)
- GNOME Terminal as the terminal emulator
- Claude Code installed at `~/.local/bin/claude`

Modify `main.py` to adjust these for your setup.
