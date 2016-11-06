#!/usr/bin/env python
#Name: ds-keyboard.py
#Depends: ds-keyboard, setxkbd
#Author: Dave (david@daveserver.info)
#Purpose: Configure keyboard on per user basis for a session.

#!/usr/bin/env python
#Name: ds-mouse.py
#Depends: python, gtk, xset
#Author: Dave (david@daveserver.info)
#Purpose: Configure mouse on per user basis for a session. This is the gui frontend

import gtk
import os
import re
import gettext
gettext.install("antixcckeyboard.sh", "/usr/share/locale")
class Error:
    def __init__(self, error):
        dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, message_format=_("There is an error,\nplease rerun and correct the following error!")+"\n\n"+error)
        dlg.set_title(_("Error"))
        dlg.set_keep_above(True) # note: set_transient_for() is ineffective!
        dlg.run()
        dlg.destroy() 
       
class Success:
    def __init__(self, success):
        dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, message_format=_("Successfully updated")+":\n\n"+success)
        dlg.set_title(_("Successfully updated"))
        dlg.set_keep_above(True) # note: set_transient_for() is ineffective!
        dlg.run()
        dlg.destroy() 
       
class Var: 
    def read(self):        
        var = Var
        var.USER_HOME = os.environ['HOME']
        var.CONF_USER_DIR = var.USER_HOME+"/.desktop-session/"
        var.CONF_USER_FILE = var.CONF_USER_DIR+"keyboard.conf"
        var.CONF_SYSTEM_FILE = "/etc/desktop-session/keyboard.conf"
        
        if not os.path.exists(var.CONF_USER_DIR):
            os.system("mkdir %s" % (var.CONF_USER_DIR))
            os.system("cp %s %s" % ((var.CONF_SYSTEM_FILE),(var.CONF_USER_DIR)))
        else:
            if not os.path.isfile(var.CONF_USER_FILE):
                os.system("cp %s %s" % ((var.CONF_SYSTEM_FILE),(var.CONF_USER_DIR)))
            
        for line in open(var.CONF_USER_FILE, "r").xreadlines():
            if "#" not in line:
                if re.search(r'^.*=', line):
                    pieces = line.split('=')
                    var.VARIABLE=(pieces[0])
                    var.VARIABLE = re.sub(r'\n', '', var.VARIABLE)
                    OBJECT=(pieces[1])
                    OBJECT = re.sub(r'\n', '', OBJECT)
                    setattr(var, var.VARIABLE, OBJECT)
        
    def write(self, variable, item):
        WRITE_FILE = Var.CONF_USER_FILE+".tmp"
        READ_FILE = Var.CONF_USER_FILE
        
        text = file((WRITE_FILE), "w");text.write("");text.close()
        text = file((WRITE_FILE), "a")
        for line in open(READ_FILE, "r").xreadlines():
            if "#" not in line:
                if re.search(r'^%s=' % (variable), line):
                    text.write (variable+"="+str(item)+"\n") 
                else:
                    text.write (line) 
            else:
                text.write (line) 
        text.close()        
        os.system("mv %s %s" % ((WRITE_FILE), (READ_FILE)))

class mainWindow():
    def apply(self,widget,option):
        if option == 0: #apply button

            model = self.model.get_model()
            index = self.model.get_active()
            model_value = model[index][0]

            model = self.layout.get_model()
            index = self.layout.get_active()
            layout_value = model[index][0]

            model = self.variant.get_model()
            index = self.variant.get_active()
            variant_value = model[index][0]
            
            Var().write('MODEL', model_value)
            Var().write('LAYOUT', layout_value)
            Var().write('VARIANT', variant_value)
            
            if self.moreoptions.get_active():
                model = self.layout2.get_model()
                index = self.layout2.get_active()
                layout2_value = model[index][0]
                
                options_value=self.options.get_text()
                
                systemwide_value=self.systemwide.get_active()
                
                Var().write('OPTIONS', options_value)
                Var().write('LAYOUT2', layout2_value)
                Var().write('SYSTEMWIDE', systemwide_value)
                
                
            #try:
            #    os.system("ds-keyboard")
            #except:
            #    Error(_("Could not run ds-keyboard"))
            #else:
            #    Success(_("All Options Set"))
        
    def make_frame(self, text):
        frame = gtk.Frame(_(text))
        frame.set_border_width(10)
        self.mainbox.pack_start(frame)
        frame.show()
        
        self.framebox = gtk.VBox()
        frame.add(self.framebox)
        self.framebox.show()
    
    def build_drop_box(self, option, name):
        os.system("awk -v RS='' \"/! %s/\" /usr/share/X11/xkb/rules/base.lst |cut -d ' ' -f3 > /tmp/xkb.txt" % option)
        for line in open("/tmp/xkb.txt", "r").xreadlines():
            if "!" not in line:
                line = re.sub(r'\n', '', line)
                if name == 'model':
                    self.model.append_text(line)
                elif name == 'layout':
                    self.layout.append_text(line)
                elif name == 'variant':
                    self.variant.append_text(line)
                elif name == 'layout2':
                    self.layout2.append_text(line)
                    
    def showhidden(self, mode):
        if self.hiddenbox.flags() & gtk.VISIBLE :
            self.hiddenbox.hide()
        else:
            self.hiddenbox.show()
        
        
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(300,500)
        window.set_title(_("Keyboard Config"))
        window.connect("destroy", lambda w: gtk.main_quit())
        
        self.mainbox = gtk.VBox()
        window.add(self.mainbox)
        self.mainbox.show()
        
        self.make_frame("Layout")
        
        self.layout = gtk.combo_box_new_text()
        self.layout.append_text(_(Var.LAYOUT))
        self.build_drop_box("layout", "layout")
        self.layout.set_active(0)
        self.framebox.pack_start(self.layout)
        self.layout.show()
        
        self.make_frame("Model")
        
        self.model = gtk.combo_box_new_text()
        self.model.append_text(_(Var.MODEL))
        self.build_drop_box("model", "model")
        self.model.set_active(0)
        self.framebox.pack_start(self.model)
        self.model.show()
        
        self.make_frame("Variant")
        
        self.variant = gtk.combo_box_new_text()
        self.variant.append_text(_(Var.VARIANT))
        self.build_drop_box("variant", "variant")
        self.variant.set_active(0)
        self.framebox.pack_start(self.variant)
        self.variant.show()
        
        self.make_frame("Options")
        
        self.moreoptions = gtk.CheckButton("More Options")
        self.moreoptions.connect("toggled", self.showhidden)
        self.framebox.pack_start(self.moreoptions)
        self.moreoptions.show()
        
        self.hiddenbox = gtk.VBox()
        self.framebox.pack_start(self.hiddenbox)
        
        label = gtk.Label("Secondary layout")
        self.hiddenbox.pack_start(label,padding=5)
        label.show()
        
        self.layout2 = gtk.combo_box_new_text()
        self.layout2.append_text(_(Var.LAYOUT2))
        self.build_drop_box("layout", "layout2")
        self.layout2.set_active(0)
        self.hiddenbox.pack_start(self.layout2,padding=5)
        self.layout2.show()
        
        label = gtk.Label("Options")
        self.hiddenbox.pack_start(label,padding=5)
        label.show()
        
        self.options = gtk.Entry()
        self.options.set_text(Var.OPTIONS)
        self.hiddenbox.pack_start(self.options,padding=5)
        self.options.show()
        
        self.systemwide = gtk.CheckButton("Set System Wide")
        if Var.SYSTEMWIDE == "True":
            self.systemwide.set_active(1)
        else:
            self.systemwide.set_active(0)
        self.hiddenbox.pack_start(self.systemwide,padding=5)
        self.systemwide.show()
        
        

        #BUTTON BOX
        
        buttonbox = gtk.HButtonBox()
        self.mainbox.pack_start(buttonbox)
        buttonbox.show()
        
        aply = gtk.Button(stock=gtk.STOCK_APPLY)
        aply.connect("clicked", self.apply, 0)
        buttonbox.pack_start(aply)
        aply.show()
        
        close = gtk.Button(stock=gtk.STOCK_CLOSE)
        close.connect("clicked", lambda w: gtk.main_quit())
        buttonbox.add(close)
        close.show()
        window.show()

Var().read()
mainWindow()
gtk.main()
