# Workspaces for i3blocks

## Overview

Displays a window list by workspaces and screens.

![screenshot](https://github.com/dechandler/i3-blocklet_workspaces/raw/master/screenshot.png)

## Setup

Put the daemon and gen file someplace and edit the first few lines of workspaces_daemon.sh to reflect where you put things

Start the daemon from your i3 config with the correct path and screens (the screen order is preserved)
```
exec ~/.i3/i3_blocklets/workspaces_daemon.sh eDP1 DP1-2 DP1-1 DVI-I-1
```

In your i3blocks.conf
```
[workspaces]
command=cat /dev/shm/workspaces.pango
interval=1
markup=pango
```
