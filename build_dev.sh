#!/bin/bash
apt update && apt install libgtkextra-dev libgconf2-dev libnss3 libasound2 libxtst-dev libxss1 libgtk-3-0 nodejs npm libgbm-dev libasound2 x11-apps libappindicator1 -y
npm install electron --save-dev
pip install -r ./server/requirements.txt
npm install -g @vue/cli
npm install -g n
n 16

