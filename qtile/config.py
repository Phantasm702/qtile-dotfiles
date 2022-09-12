# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration
from libqtile.config import Match, Screen,Click, Drag, Key, Group
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile

import subprocess
import shlex
import os


######################################################
####################--KEYBINDINGS--####################
######################################################


mod = "mod4"
mod1 = "mod1"
terminal = guess_terminal()
home = os.path.expanduser("~") + "/"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Custom keybinds
    Key([mod1], "f", lazy.spawn("firefox"), desc="Start firefox"),
    Key([mod], "l", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.widget["volume"].decrease_vol()),
    Key([], "XF86AudioRaiseVolume", lazy.widget["volume"].increase_vol()),
    Key([], "Print", lazy.spawn("scrot " + home + "Pictures/screenshot_%Y-%m-%d.png -e 'xclip -selection clipboard -t image/png -i $f'"), desc="Take a screenshot"),
    Key(["control"], "Print", lazy.spawn("scrot " + home + "Pictures/screenshot_%Y-%m-%d.png -s -e 'xclip -selection clipboard -t image/png -i $f'"), desc="Take a screenshot of an area"),
    Key([mod], "z", lazy.group["6"].toscreen(), desc="Switch to zoom group"),
    Key(["control"], "p", lazy.spawn("playerctl -a play-pause")),
    Key([mod1], "space", lazy.hide_show_bar("bottom"), desc="Show/Hide the bar"),
    Key([mod1], "l", lazy.spawn("lightlocker-command -l"), desc="lock screen")
]





######################################################
####################--MOUSE+KEYS--####################
######################################################


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]





##################################################
####################--GROUPS--####################
##################################################



icons = ["", "", "", "ﱘ", "", "辶"]

groups = [
        Group("1", label=icons[0], matches=[Match(wm_class=["Alacritty"])], layout="Columns"),
        Group("2", label=icons[1], matches=[Match(wm_class=["firefox"])], layout="max"),
        Group("3", label=icons[2], matches=[Match(wm_class=["code-oss"])], layout="max"),
        Group("4", label=icons[3], matches=[Match(wm_class=["Spotify", "spotify"])], layout="max"),
        Group("5", label=icons[4], matches=[Match(wm_class=["brave-browser"])]),
        Group("6", label=icons[5], matches=[Match(wm_class=["zoom", "xdg-desktop-portal-kde"])], exclusive=True, layout="max")
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )





###################################################
####################--LAYOUTS--####################
####################################################

dark = "#141821" #"#14101D"
light = "#AD8998"

layouts = [
    layout.Columns(border_focus_stack=["#0A121C", "46847C"], border_focus=light, border_normal=dark, border_width=3, margin=10),
    layout.Max(margin=5),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]





###############################################
####################--BAR--####################
###############################################


widget_defaults = dict(
    font="Ubuntu Mono Nerd Font",
    fontsize=14,
    padding=3,
)

# icons
volume = "墳"
brightness = ""
cpu = ""
time = ""
calendar = ""
power = ""
update = "ﮮ"

# colours
dark = "#141821" #"#14101D"
light = "#AD8998"
darker_light = "#305A53"
greyed_out = "#38534E"
transparent = "#00000000"
vibrant_selected = "162941" #1E3655"

# fontsize
fs = 17 # 17

toleft = "\ue0b2" #""
toright = "\ue0b0" #""


extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.TextBox(
                    text=" ",
                    foreground=dark,
                    background=dark,
                    decorations = [
                        RectDecoration(colour=dark, filled=True, radius=[10, 0, 0, 10], padding_y=0, use_widget_background=True),
                    ],
                ),
                widget.GenPollText(
                    func= lambda: subprocess.check_output("cat " + home + ".config/qtile/scripts/updates.txt", shell=True).decode("utf-8").strip(),
                    update_interval=1,
                    background=dark,
                    foreground=light,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("%s -e sudo pacman -Syu" % terminal, shell=True)},
                ),
                widget.TextBox(
                    text=toright,
                    font="Ubuntu Mono",
                    fontsize=fs,
                    background=light,
                    foreground=dark,
                    padding=0,
                    fontshadow=None
                ),
                widget.Systray(
                    background=light,
                    icon_size=14,
                ),
                widget.TextBox(
                    text=toright,
                    font="Ubuntu Mono",
                    fontsize=fs,
                    background=dark,
                    foreground=light,
                    padding=0,
                    fontshadow=None
                ),
                widget.TextBox(
                    text="Meta + R",
                    foreground=light,
                    background=dark,
                ),
                widget.TextBox(
                    text=toright,
                    font="Ubuntu Mono",
                    fontsize=fs,
                    background=light,
                    foreground=dark,
                    padding=0,
                    fontshadow=None
                ),
                widget.WindowName(
                    background=light,
                    foreground=dark,
                    max_chars=40,
                    width=bar.CALCULATED, #295, adjust total width of left section to be same as total width of right section
                    empty_group_string="Against the winds",
                    scroll=True,
                ),
                widget.TextBox(
                    text=" ",
                    foreground=light,
                    background=light,
                    decorations = [
                        RectDecoration(colour=light, filled=True, radius=[0, 10, 10, 0], padding_y=0, use_widget_background=True)
                    ],
                ),
#                widget.TextBox(
#                    text=toright,
#                    font="Ubuntu Mono",
#                    fontsize=fs,
#                    background=transparent,
#                    foreground=light,
#                    padding=0,
#                    fontshadow=None
#                ),
                widget.Prompt(
                    foreground=light,
                    background=transparent,
                    ignore_dups_history=True,
                    scroll=True,
                ),
                widget.Spacer(
                    length=bar.STRETCH, #555,
                    background=transparent #dark + "80",
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.GroupBox(
                    background=transparent,
                    foreground=dark,
                    active=vibrant_selected,
                    inactive=greyed_out,
                    highlight_method="text",
                    highlight_color=[dark, darker_light],
                    this_current_screen_border=dark,
                    disable_drag=True,
                    padding_x=5,
                    decorations = [
                        RectDecoration(colour=light, filled=True, radius=10, padding_y=0)
                    ],
                ),
                widget.Spacer(
                    length=bar.STRETCH, #555,
                    background=transparent #dark + "80",
                ),
                widget.TextBox(
                    text=" ",
                    foreground=light,
                    background=light,
                    decorations = [
                        RectDecoration(colour=light, filled=True, radius=[10, 0, 0, 10], padding_y=0, use_widget_background=True)
                    ],
                ),
                widget.Clock(
                    foreground=dark,
                    background=light,
                    format=calendar + " %d-%m %a | " + time + " %I:%M %p",
                ),
                widget.TextBox(
                    text=toleft,
                    font="Ubuntu Mono",
                    fontsize=fs,
                    background=light,
                    foreground=dark,
                    padding=0,
                    fontshadow=None
                ),
                widget.Backlight(
                    backlight_name="intel_backlight",
                    format=brightness + " " + "{percent:2.0%}",
                    background=dark,
                    foreground=light,
                ),
                widget.TextBox(
                    foreground=light,
                    background=dark,
                    text="|",
                ),
                widget.Volume(
                    step = 2,
                    fmt=volume + " " + "{}",
                    background=dark,
                    foreground=light,
                ),
                widget.TextBox(
                    text=toleft,
                    font="Ubuntu Mono",
                    fontsize=fs,
                    background=dark,
                    foreground=light,
                    padding=0,
                    fontshadow=None
                ),
                widget.GenPollText(
                    func= lambda: subprocess.check_output("/home/alpha/.config/qtile/scripts/script.py eth", shell=True).decode("utf-8").strip(),
                    update_interval=1,
                    background=light,
                    foreground=dark,
                ),
                widget.GenPollText(
                    func= lambda: subprocess.check_output("/home/alpha/.config/qtile/scripts/script.py wifi", shell=True).decode("utf-8").strip(),
                    update_interval=1,
                    background=light,
                    foreground=dark,
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("/home/alpha/.config/qtile/scripts/script.py lclick wifi")}
                ),
                widget.GenPollText(
                    func= lambda: subprocess.check_output("/home/alpha/.config/qtile/scripts/script.py bt", shell=True).decode("utf-8").strip(),
                    update_interval=1,
                    background=light,
                    foreground=dark,
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn("/home/alpha/.config/qtile/scripts/script.py lclick bt"),
                        "Button3": lambda: qtile.cmd_spawn("/home/alpha/.config/qtile/scripts/script.py rclick bt")
                    }
                ),
                widget.TextBox(
                    foreground=dark,
                    background=light,
                    text="|",
                ),
                widget.GenPollText(
                    func= lambda: subprocess.check_output("/home/alpha/.config/qtile/scripts/script.py bat", shell=True).decode("utf-8").strip(),
                    update_interval=1,
                    background=light,
                    foreground=dark,
                ),
                widget.TextBox(
                    text=toleft,
                    font="Ubuntu Mono",
                    fontsize=fs,
                    background=light,
                    foreground=dark,
                    padding=0,
                    fontshadow=None
                ),
                widget.QuickExit(
                    default_text=" " + power,
                    background=dark,
                    foreground=light,
                    countdown_format='[{}]',
                ),
                widget.TextBox(
                        text=" ",
                        foreground=dark,
                        background=dark,
                        decorations = [
                        RectDecoration(colour=dark, filled=True, radius=[0, 10, 10, 0], padding_y=0, use_widget_background=True)
                    ],
                ),
#                widget.TextBox(
#                    text="                                              ",
#                    foreground=dark,
#                    background=dark
#                )
            ],
            22,
            background="#00000000",
            opacity=1,
            margin=[5, 5, 5, 5]
 #           border_width=[5, 5, 5, 5],  # Draw top and bottom borders
 #           border_color=["#101D2E", "#101D2E", "#101D2E", "#101D2E"]  # Borders are magenta
        ),
    ),
]





######################################################
####################--OTHER VARS--####################
######################################################


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="zoom"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

subprocess.call(home + ".config/qtile/autostart.sh")
