# PNGTube Overlay

A lightweight always-on-top desktop overlay that animates a PNG character based on an app's audio activity. Built for use during streams or screen shares.

## Features
- Borderless transparent window
- Always on top
- Reacts to any app's audio (Discord, Teams, etc.)
- Draggable
- Near-zero CPU usage

## Setup
1. Install dependencies
   pip install -r requirements.txt

2. Add your assets
   Place your PNG images in the assets/ folder
   - assets/idle.png
   - assets/talk.png

3. Configure
   Open window.py and change these variables to your preference
   - WIDTH, HEIGHT — window size
   - FPS — frame rate
   - THRESHOLD — talking sensitivity (default 0.0001)
   
   Open audioengine.py and change the app name in get_session()
   - Default is "Discord.exe", change to "Teams.exe" etc.

4. Run
   python window.py

## Dependencies
See requirements.txt
