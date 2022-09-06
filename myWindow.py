from __future__ import print_function
from datetime import date
from distutils.log import info
from json import load
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, GdkPixbuf
from myFunctions import *
import requests




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

        # append box to window
        self.set_child(self.box1)  # Horizontal box to window
        self.box1.append(self.box2)  # Put vert box in that box

        # Array with anime genres
        genre_list = ["Action", "Adventure", "Comedy", "Drama", "Ecchi", "Fantasy", 
                        "Horror", "Mahou Shoujo", "Mecha", "Music", "Mystery", "Psychological", 
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
        self.grid.set_halign(Gtk.Align.CENTER)
        self.box2.append(self.grid)
        
        self.grid.attach(self.label, 0, 0, 6, 1)
        for i in range(6):
            self.grid.attach(self.genre_check[i], i, 1, 1, 1)
        for i in range(6):
            self.grid.attach(self.genre_check[i+6], i, 2, 1, 1)
        for i in range(6):
            self.grid.attach(self.genre_check[i+12], i, 3, 1, 1)

        self.slider_grid = Gtk.Grid()
        self.slider_grid.set_halign(Gtk.Align.CENTER)
        self.box2.append(self.slider_grid)
        
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
        self.year_label.set_halign(Gtk.Align.CENTER)
        # Create 2 dropdown for select a range of years
        self.year_grid = Gtk.Grid()
        self.box2.append(self.year_grid)
        self.year_grid.set_halign(Gtk.Align.CENTER)
        
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
        self.year_grid.attach(self.year_label, 0, 0, 2, 1)
        self.year_grid.attach(self.dropdown1   , 0, 1, 1, 1)
        self.year_grid.attach(self.dropdown2   , 1, 1, 1, 1)
        
        #set default value
        self.dropdown1.set_selected(int(date.today().year)-1962)
        self.dropdown2.set_selected(int(date.today().year)-1940)

        # Create a Confirm button
        self.confirm_button = Gtk.Button(label="Confirm")
        self.confirm_button.connect("clicked", self.on_confirm_clicked)
        self.confirm_button.set_margin_top(20)
        self.confirm_button.set_halign(Gtk.Align.CENTER)
        self.confirm_button.set_hexpand(False)
        self.box2.append(self.confirm_button)
        
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

        anime = get_anime(genre_list = selected_genres , years = selected_years, vote = self.vote_slider.get_value())
        
        # Create a Dialog with anime info
        self.dialog = DialogAnime(self, anime=anime)
        self.dialog.set_transient_for(self)
        self.dialog.show()
        
        #self.dialog.destroy()
        
# ----------------------------------------------------------------------------------------------------------------------

class DialogAnime(Gtk.Dialog):
    def __init__(self, parent, anime):
        super().__init__(title=anime["name_romaji"], transient_for=parent)
        #create ok button to close dialog
        ok = self.add_button("Ok", Gtk.ResponseType.OK)
        
        # close dialog 
        ok.connect("clicked", self.on_ok_clicked)
        
        # Title label with anime name
        label_title = Gtk.Label()
        label_title.set_margin_top(20)
        markup = get_font_markup('Noto Sans Regular 20', anime["name_romaji"])
        label_title.set_markup(markup)
        label_title.set_valign(Gtk.Align.CENTER)
        
        # Description label with anime description
        desc = Gtk.Label(label=anime["desc"].split("<br>")[0])
        # wrap label 
        desc.set_wrap(True)
        desc.set_max_width_chars(50)
        desc.set_width_chars(50)
        
        #add image from url
        cover_image = Gtk.Image()
        response = requests.get(anime["cover_image"])
        content = response.content
        loader = GdkPixbuf.PixbufLoader()
        loader.write_bytes(GLib.Bytes.new(content))
        loader.close()
        cover_image.set_from_pixbuf(loader.get_pixbuf())
        #set image size
        cover_image.set_size_request(230, 345)
        
        # Grid with extra info
        info_format = Gtk.Label(label="Format: " + anime["airing_format"])
        info_format.set_halign(Gtk.Align.CENTER)
        info_episodes = Gtk.Label(label="Episodes: " + str(anime["airing_episodes"]))
        info_episodes.set_halign(Gtk.Align.CENTER)
        info_status = Gtk.Label(label="Status: " + anime["airing_status"])
        info_status.set_halign(Gtk.Align.CENTER)
        info_score = Gtk.Label(label="Vote: " + str(anime["average_score"]))
        info_score.set_halign(Gtk.Align.CENTER)
        
        info_grid = Gtk.Grid()
        info_grid.attach(info_format, 0, 0, 1, 1)
        info_grid.attach(info_episodes, 0, 1, 1, 1)
        info_grid.attach(info_status, 1, 0, 1, 1)
        info_grid.attach(info_score, 1, 1, 1, 1)
        info_grid.set_column_spacing(10)
        info_grid.set_halign(Gtk.Align.CENTER)
        info_grid.set_margin_top(20)
        
        # Create a grid
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_top(20)
        grid.attach(cover_image, 0, 0, 1, 3)
        grid.attach(desc, 1, 1, 1, 1)
        grid.attach(info_grid, 1, 0, 1, 1)
        
        #self.set_default_size(150, 100)
        box = self.get_content_area()
        box.append(label_title)
        box.append(grid)
        self.show()
    
    def on_ok_clicked(self, widget):
        self.destroy()
