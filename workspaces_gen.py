#!/usr/bin/env python3
## -*- coding: utf-8 -*-
"""
Args: Output names in desired order (eg, "DVI-1-2 DVI-0 DVI-1")

Depends on:
    i3blocks 1.4+
    fontawesome

"""
import sys

import i3
from jinja2 import Template

template = Template(''.join([
"<span color='#00ffff'><sub>",
"{{ available | join(',') }} ",
"</sub></span>",
"<span size='smaller'>",
"{% for output in outputs %}",
"<big><span color='#aa00dd'>[ </span></big>",
  "{% for ws in output %}",
    "<span color='{{ '#ff0000' if ws.urgent else '#00ffff' }}'><sub>",
    "{{ ws.num }} ",
    "</sub></span>",
    "{% if ws.urgent  %}<span color='#ff0000'>{% endif %}",
    "{{ ws.labels | join(' ') }}",
    "{% if ws.urgent %}</span>{% endif %}",
    "{% if not loop.last %} | {% endif %}",
    "{% endfor %}",
  "<big><span color='#aa00dd'> ]</span></big>",
"{% endfor %}",
"</span>"
]))


class Workspaces(object):

    def __str__(self):
        return template.render(outputs=self.outputs, available=self.available)

    def __init__(self):

        tree = i3.get_tree()
        output_order = sys.argv[1:]

        output_map = {
            x['name']: self.get_workspaces(x)
            for x in tree['nodes']
        }
        self.outputs = [
            output_map[o]
            for o in output_order
        ]

        ws_nums = []
        for output in self.outputs:
            for workspace in output:
                ws_nums.append(workspace['num'])
                for window in workspace['windows']:
                    window['label'] = self.get_win_label(window)
                self.set_ws_attrs(workspace)

        self.available = [ num for num in range(1,9) if num not in ws_nums ]

    def get_workspaces(self, output):

        def flatten(container):
            """
            Digs through containers to return a flat list of windows

            """
            if not container['nodes']:
                return [container]
            else:
                windows = []
                for pane in container['nodes']:
                    pane_windows = flatten(pane)
                    windows.extend( pane_windows )
                return windows

        content = [ x for x in output['nodes'] if x['name'] == "content" ][0]
        workspaces = content['nodes']

        return [
            {
                'windows': flatten(workspace),
                'num': workspace['num']
            }
            for workspace in workspaces
        ]

    def get_win_label(self, window):

        try:
            win_class = window['window_properties']['class']
            win_instance = window['window_properties']['instance']
        except KeyError:
            return ""

        multi_subs = [
            [["Pidgin"], "\uf075 "],  # fa-comment
            [["Sublime_text", "Atom"], "\uf044"],  # fa-pencil-square-o # \uf121 fa-code
            [["Firefox"], "\uf269 "],  # fa-firefox
            [["libreoffice-calc"], "\uf0ce "],  # fa-table
            [["libreoffice-writer"], "\uf036 "],  # fa-align-left
            [["Virt-manager"], "\uf24d "],  # fa-clone
            [["Inkscape"], "\uf248 "],  # fa-object-ungroup
            [["Steam"], "\uf1b6"],  # fa-steam
            [["load-RazorSQL"], "\uf1c0 "],  # fa-database
            [["xfreerdp"], "\uf26c "],  # fa-television
            [["Totem"], "\uf16a "], # fa-youtube-play
            [["Nautilus", "Thunar"], "\uf115 "],  # fa-folder-open-o
            [["Eog"], "\uf03e"],  # fa-picture
            [["Evince"], "\uf1c1"],  # fa-file-pdf-o
            [["Quodlibet", "Rhythmbox"], "♪"],
            [["X-terminal-emulator", "Terminator"], "~$"],
        ]
        for sub in multi_subs:
            if win_class in sub[0]:
                return sub[1]

        substr_subs = [
            ["Minecraft", "\uf1b3 "],  # fa-cubes
            ["google-chrome", "\uf268 "]  # fa-chrome
        ]
        for sub in substr_subs:
            if sub[0] in win_class:
                return sub[1]

        if ( win_class     == "processing-app-Base" and
               win_instances == "sun-awt-X11-XFramePeer" ):
            return "Arduino"

        return win_class

    def set_ws_attrs(self, workspace):
        """
        """
        uniq_labels = []
        for l in [ win['label'] for win in workspace['windows'] ]:
            if l not in uniq_labels:
                uniq_labels.append(l)

        workspace.update({
            'labels': uniq_labels,
            'urgent': any([ w['urgent'] for w in workspace['windows'] ]),
            'focused': any([ w['focused'] for w in workspace['windows'] ])
        })


if __name__ == "__main__":
    print(str(Workspaces()))
