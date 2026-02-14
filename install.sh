#!/bin/bash
sudo cp /home/jedijamez/dev/copilot-key-handler/copilot-key-handler.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now copilot-key-handler
sudo systemctl status copilot-key-handler
