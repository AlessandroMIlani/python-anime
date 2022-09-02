import myWindow
# Load Gtk
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio  

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.connect('open', self.on_activate)
        self.set_flags(Gio.ApplicationFlags.HANDLES_OPEN)
        self.win = None

    def on_activate(self, app):
        if not self.win:
            self.win = myWindow.MainWindow(application=app)
        self.win.present()


    def on_open(self,app,files,n_files,hint):
        self.on_activate(app)
        for fie in n_files:
            print("File to open: ", {fie.get_path()})