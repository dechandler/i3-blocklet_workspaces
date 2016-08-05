# Workspaces for i3blocks

## Overview

Displays a window list by workspaces and screens.

![screenshot](https://cloud.githubusercontent.com/assets/5094374/17425586/7beffd06-5a94-11e6-8a7d-06068ce17441.png)

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
