#!/bin/bash
#
# Workspaces i3blocklet backend daemon
#
# args are output names
# subscribes to i3 window and workspace events and
# updates a file that i3blocks cats as a blocklet
#
_i3subscribe="~/.i3/i3_blocklets/i3subscribe.pl"
_workspaces_gen="~/.i3/i3_blocklets/workspaces_gen.py"
_dump_file="/dev/shm/workspaces.pango"

$_i3subscribe window workspace | \
while read -r _event; do
    grep 'focus$' >/dev/null <<< $_event \
    || $_workspaces_gen "$@" > $_dump_file;
done
