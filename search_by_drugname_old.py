__author__ = 'animeshk'
from gi.repository import Gtk
from main import draw_side_effects

class ToggleButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Search Side effects by Drug Name")
        self.set_border_width(10)

        grid = Gtk.Grid()
        self.add(grid)

        label = Gtk.Label()
        label.set_markup("Enter Drug Name")
        label.set_line_wrap(True)

        self.textview = Gtk.TextView()
        textbuffer = self.textview.get_buffer()
        textbuffer.set_text("")

        searchButton = Gtk.Button(label="Search")
        searchButton.connect("clicked", on_search_clicked)
        cancelButton = Gtk.Button(label="Cancel")
        searchButton.connect("clicked", on_cancel_clicked)
        grid.add(label)
        grid.attach(textview, 1, 0, 2, 1)
        grid.attach_next_to(searchButton, label, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(cancelButton, textview, Gtk.PositionType.RIGHT, 2, 1)


    def on_search_clicked(self, button):
        draw_side_effects(self.textview.get_buffer)

def on_cancel_clicked(button):
    win = ToggleButtonWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


# win = ToggleButtonWindow()
# win.connect("delete-event", Gtk.main_quit)
# win.show_all()
# Gtk.main()