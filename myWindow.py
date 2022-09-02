import random
from datetime import date
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib  
from myFunctions import *



# ------------------------------------------------------------------------------

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set app name
        GLib.set_application_name("Random-Anime")

        # Size of window
        self.set_default_size(800, 600)

        # Title of window
        self.set_title("Random-Anime")

        # Button in the headerbar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        # Creare box
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # append box to window
        self.set_child(self.box1)  # Horizontal box to window
        self.box1.append(self.box2)  # Put vert box in that box
        self.box1.append(self.box3)  # And another one, empty for now
        self.box1.append(self.box4)  # And another one, empty for now

        # Array with anime genres
        genre_list = ["Action", "Adventure", "Comedy", "Drama", "Ecchi", "Fantasy", 
                        "Horror", "Shoujo", "Mecha", "Music", "Mystery", "Psychological", 
                        "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural", "Thriller"]

        # Create a Label
        self.label = Gtk.Label()
        self.label.set_text("Select genres")

        # Create 18 checkboxes for genres
        self.genre_check = []
        for i in range(18):
            self.genre_check.append(Gtk.CheckButton(label= genre_list[i]))
            self.genre_check[i].set_active(False)

        # append checkboxes on a grid 6 x 3
        self.grid = Gtk.Grid()
        self.box2.append(self.grid)
        self.grid.attach(self.label, 0, 0, 6, 1)
        for i in range(6):
            self.grid.attach(self.genre_check[i], i, 1, 1, 1)
        for i in range(6):
            self.grid.attach(self.genre_check[i+6], i, 2, 1, 1)
        for i in range(6):
            self.grid.attach(self.genre_check[i+12], i, 3, 1, 1)

        self.slider_grid = Gtk.Grid()
        self.box3.append(self.slider_grid)
        # Create a Slider 0.0 to 10.0
        self.vote_slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.0, 100, 1)
        self.vote_slider.set_value_pos(Gtk.PositionType.BOTTOM)
        self.vote_slider.set_hexpand(False)
        self.vote_slider.add_mark(50, Gtk.PositionType.BOTTOM, None)
        self.vote_slider.set_draw_value(True)

        # Create a Vote Label
        self.vote_label = Gtk.Label()
        self.vote_label.set_text("Select the minimum vote score")
        self.slider_grid.attach(self.vote_label, 0, 0, 1, 1)
        self.slider_grid.attach(self.vote_slider, 0, 1, 1, 1)

        # Create a label for year
        self.year_label = Gtk.Label()
        self.year_label.set_text("Select the year range")

        # Create 2 dropdown for select a range of years
        self.year_grid = Gtk.Grid()
        self.box3.append(self.year_grid)
        # Gtk.StringList with years from 1900 to 2022
        self.year_list = Gtk.StringList()
        for i in range(int(date.today().year)-1940 + 1):
            self.year_list.append(str(1940 + i))
        self.dropdown1 = Gtk.DropDown.new(self.year_list)
        self.dropdown2 = Gtk.DropDown.new(self.year_list)
        self.dropdown1.set_margin_top(20)
        self.dropdown1.set_margin_start(20)
        self.dropdown1.set_size_request(200, -1)
        self.dropdown1.set_halign(Gtk.Align.START)
        self.dropdown2.set_margin_top(20)
        self.dropdown2.set_margin_start(20)
        self.dropdown2.set_size_request(200, -1)
        self.dropdown2.set_halign(Gtk.Align.START)
        # add dropdown to grid
        self.year_grid.attach(self.year_label, 0, 0, 1, 1)
        self.year_grid.attach(self.dropdown1   , 0, 1, 1, 1)
        self.year_grid.attach(self.dropdown2   , 1, 1, 1, 1)


        # Create a Confirm button
        self.confirm_button = Gtk.Button(label="Confirm")
        self.confirm_button.connect("clicked", self.on_confirm_clicked)
        self.box4.append(self.confirm_button)

        # Create a new menu
        menu = Gio.Menu.new()

        # Create a popover
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        # add menu buttorn to head bar
        self.header.pack_end(self.hamburger)

        # Create ad anction for about dialog
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)

        menu.append("About", "win.about")

        
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    def show_about(self, action, parameter):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)
        self.about.set_authors(["Alessandro Milani"])
        self.about.set_copyright("Copyright 2022 Alessandro Milani")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("https://github.com/AlessandroMIlani")
        self.about.set_website_label("My github")
        self.about.set_version("1.0")
        self.about.set_logo_icon_name("org.example.example") # The icon will need to be added to appropriate location
                                                            # E.g. /usr/share/icons/hicolor/scalable/apps/org.example.example.svg
        self.about.show()

    def on_confirm_clicked(self, widget):
        # Create an array with selected genres
        selected_genres = []
        random_anime = []
        for i in range(18):
            if self.genre_check[i].get_active():
                selected_genres.append(self.genre_check[i].get_label())
        
        # Create array with selected years
        selected_years = []
        selected_years.append(self.dropdown1.get_selected_item().get_string())
        selected_years.append(self.dropdown2.get_selected_item().get_string())

        get_anime(genre_list = selected_genres , years = selected_years, vote = self.vote_slider.get_value())
# ----------------------------------------------------------------------------------------------------------------------
