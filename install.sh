#!/bin/bash
sudo cp /home/jedijamez/dev/copilot-key-remap-claude/copilot-key-remap-claude.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now copilot-key-remap-claude
sudo systemctl status copilot-key-remap-claude
