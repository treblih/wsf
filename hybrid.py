#!/usr/bin/env python 

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import glib
import os
from subprocess import *
from threading import Thread
import time
import locale
import gobject

encoding = locale.getpreferredencoding()
utf8conv = lambda x : unicode(x, encoding).encode('utf8')

autorun = True
cores = os.sysconf('SC_NPROCESSORS_CONF')
cores_use = cores
#import getpass
# getpass.getuser() -> user name
home = '/home/' + os.environ['USER'] + '/'
path_conf = home + '.hybridrc'

INDEX, NAME, TEXTVIEW, BASE_DIR, CMP_DIR, RUN_DIR, CMP, RUN = range(8)
cmd = {'cmp':  (0,
                '', 
                'tv_cmp',
                '',
                '',
                '',
                '',
                '',
               ),
       'wrf':  (1,
                'wrf', 
                'tv_wrf', 
                home+'wrf/', 
                home+'wrf/', 
                home+'wrf/',
                '',
                '',
               ), 
       ##################################
       ##################################
       ### no wrf now, change INDEX
       ##################################
       ##################################
       ##################################
       'swan': (1,
                'swan', 
                'tv_swan',
                home+'swan/', 
                home+'swan/', 
                home+'swan/', 
                #'ls /',
                'make clean && make config && make mpi',
                #'ping yahoo.com -c 15',
                #'cat /home/hask/share/txt/*',
                '',
               ),
       'fvcom':(2,
                'fvcom', 
                'tv_fvcom', 
                home+'FVCOM/', 
                home+'FVCOM/FVCOM_source/', 
                home+'FVCOM/run/',
                'make clean && make',
                'mpirun -np ' + str(cores) + ' ../FVCOM_source/fvcom chn',
               ),
      }
 
class win_main(object):        
    def __init__(self):
        #self.builder = gtk.Builder()
        #self.builder.add_from_file('hybrid2.xml')
        #self.builder.connect_signals(
        self.glade = gtk.glade.XML('hybrid2.glade')
        self.win_main = self.glade.get_widget('win_main')
        self.run = 1

        #self.textbuffer.set_text("nihao\nwakkak\n")
        signals = {'on_win_main_destroy':gtk.main_quit,
                   'on_but_swan_clicked':(self.on_but_cmd_clicked, cmd['swan']),
                   'on_but_fvcom_clicked':(self.on_but_cmd_clicked, cmd['fvcom']),
                   'on_toggle_swan_clicked':(self.on_toggle_cmd_clicked, cmd['swan']),
                   'on_toggle_fvcom_clicked':(self.on_toggle_cmd_clicked, cmd['fvcom']),
                   'on_but_settings_clicked':self.on_but_settings_clicked,
                   'on_but_about_clicked':self.on_but_about_clicked,
                   #'on_but_set_cancel_clicked':self.on_but_set_cancel_clicked,
                  }
        self.glade.signal_autoconnect(signals)
        #self.window = self.builder.get_object('win_main')
        self.win_main.show_all()

    # it could be def on_but_cmd_clicked(self, widget):
    def on_but_cmd_clicked(self, widget, which):
        widget.set_sensitive(False)
        t = Thread(target=self.redirect_to_textbuffer, args=(widget, which))
        t.daemon = True
        t.start()

    def redirect_to_textbuffer(self, widget, which, textview='tv_cmp', base_dir=''):
        print textview
        view = self.glade.get_widget(textview)
        buffer = view.get_buffer()
        log = ''
        f_log = None
        if base_dir:
            p = Popen(which[RUN], shell=True, stdout=PIPE, stderr=STDOUT, cwd=which[RUN_DIR])
            ## Sun Apr 24 19:06:25 2011 -> Apr_24_19:06:25_2011.log
            log = base_dir + time.asctime()[4:].replace(' ', '_') + '.log'
            f_log = open(log, 'w')
        else:
            p = Popen(which[CMP], shell=True, stdout=PIPE, stderr=STDOUT, cwd=which[CMP_DIR])
        while 1:
            line = p.stdout.readline()
            if not line or self.run == 0:
                break
            gtk.gdk.threads_enter()
            if f_log:
                f_log.write(line)
            iter = buffer.get_end_iter()
            buffer.place_cursor(iter)
            buffer.insert(iter, utf8conv(line))
            view.scroll_to_mark(buffer.get_insert(), 0.1)
            gtk.gdk.threads_leave()
        if base_dir:
            f_log.close()
            widget.set_label('Run ' + which[NAME])
        else:
            widget.set_sensitive(True)

    def on_toggle_cmd_clicked(self, widget, which):
        #if widget.get_active() and self.run:
        if widget.get_active():
            self.run = 1
            widget.set_label('Stop ' + which[NAME])
            cmd_t = Thread(target=self.redirect_to_textbuffer, args=(widget, which, which[TEXTVIEW], which[BASE_DIR]))
            cmd_t.daemon = True
            cmd_t.start()
        else:
            self.run = 0

    def on_but_settings_clicked(self, widget):
        glade = gtk.glade.XML('hybrid2.glade')
        about = glade.get_widget('dia_settings')
        chk_autorun = glade.get_widget('chk_autorun')
        spn_core = glade.get_widget('spn_core')
        ent_swan = glade.get_widget('ent_swan')
        ent_fvcom = glade.get_widget('ent_fvcom')
        cancel = glade.get_widget('but_set_cancel')
        ok = glade.get_widget('but_set_ok')
        chk_autorun.set_active(autorun)
        spn_core.set_value(cores)
        ent_swan.set_text(cmd['swan'][PATH])
        ent_fvcom.set_text(cmd['fvcom'][PATH])
        ok.connect('clicked', self.settings_ok, 
                   chk_autorun, spn_core, ent_swan, ent_fvcom)
        about.run()
        #about.destroy()

    def on_but_about_clicked(self, widget):
        # essential, otherwise next time about will be NoneType
        self.glade = gtk.glade.XML('/home/hask/hybrid/hybrid2.glade')
        about = self.glade.get_widget('dia_about')
        about.run()
        about.destroy()

    def write_to_buffer(self, fd, condition, textbuffer, widget, f_log):
        line = fd.readline() # WE READ ONE BYTE PER TIME, TO AVOID BLOCKING
        if f_log:
            f_log.write(line)
        self.textbuffer.insert_at_cursor(line) # WHEN RUNNING DON'T TOUCH THE TEXTVIEW!!
        return True
    
    def settings_ok(self, widget, chk_autorun, spn_core, ent_swan, ent_fvcom):
        global autorun, cores_use
        autorun = chk_autorun.get_active()
        cores_use = spn_core.get_value_as_int()
        if cores_use > cores:
            glade = gtk.glade.XML('hybrid2.glade')
            warning = glade.get_widget('dia_msg_core')
            warning.set_markup('Your system has only ' + str(cores) + ' cores,\n'
                              'which is less than demanded.\nSet to default!')
            warning.run()
            warning.destroy()
            cores_use = cores
        

''' Drop sys_cores from config file, count it every running.
    for the sake of miss-manipulation. '''
conf_str = \
'''autorun=True
swan_dir_path='''   + cmd['swan'][BASE_DIR]  + '''
fvcom_dir_pathm=''' + cmd['fvcom'][BASE_DIR] + '''
'''

 
if __name__ == '__main__':
    gobject.threads_init()
    gtk.gdk.threads_init()
    #if os.path.exists(path_conf):
        #f = open(path)
    #else:
        #f = open(path_conf, 'w')
        #f.write(conf_str)
        #sys.exit(1)
    app = win_main()
    gtk.main()

# TODO:
#   wrf
#   config file
#   self.run is global
