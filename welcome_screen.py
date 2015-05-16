__author__ = 'animeshk'
from gi.repository import Gtk
from search_by_drugname_old import ToggleButtonWindow

class LabelWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Drug Side Effects Detector")

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        label = Gtk.Label()
        label.set_markup("<span size='xx-large'>Welcome to Drug Side Effects Detector.</span>")
        label.set_line_wrap(True)
        vbox_left.pack_start(label, True, True, 0)

        button = Gtk.Button(label="Enter")
        button.connect("clicked", on_click_me_clicked)
        #label.set_mnemonic_widget(button)
        vbox_right.pack_start(button, True, True, 0)

        self.add(hbox)


def on_click_me_clicked(button):
    print 'hahahaha'
    win = ToggleButtonWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    window.destroy();


window = LabelWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()