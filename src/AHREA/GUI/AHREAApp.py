from Tkinter import *
import Tkconstants, tkFileDialog
import AHREAPage
from .parser.SettingsParser import *

class AHREAApp(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.root = root
        self.root.title( "AHREA - Adaptive Heuristic Relational Expression Analyser")
        self.controller = controller
        #start on welcome page
        self.curr_page = None
        self.pages = []
        self.menu = AHREAMenu(self)
        self.root.config(menu = self.menu)
        self.status = StatusBar(root)
        #self.pack(fill=BOTH)
        self.status.grid(row=3,sticky=W+E+S) #side=BOTTOM, fill=X)
        self.next_button = self.buildNextButton()
        self.next_button.grid(row=2, sticky=E+S)
        self.prev_button = self.buildPrevButton()
        self.prev_button.grid(row=2, sticky=W+S)
        self.grid(row=1, sticky=W+N)
        self.root.grid_rowconfigure(1, minsize=300)
        self.root.grid_columnconfigure(0,minsize=350)
        self.initPages()
        self.displayPage('welcome')
        self.update_idletasks()
        
        
    def initPages(self):
        self.pages.append(AHREAPage.WelcomePage(self))
        self.pages.append(AHREAPage.FileBrowsePage(self))
        self.pages.append(AHREAPage.FileLoadPage(self))
        self.pages.append(AHREAPage.ClassLabelPage(self))
        self.pages.append(AHREAPage.BuildTrainingSetPage(self))
        self.pages.append(AHREAPage.RunTraining(self))
        self.pages.append(AHREAPage.addUnclassified(self))
        self.pages.append(AHREAPage.classificationPage(self))

 
    def displayPage(self, page_id):
        self.status.clear()
        if self.curr_page:
            self.curr_page.clearPage()
            self.curr_page.pack_forget()
        for page in self.pages:
            if page.id == page_id:
                try:
                    page.setUpPage()
                    page.drawPage()
                except AHREAPage.ImplementationError as e:
                    print e.msg
                self.curr_page = page
                break
        #I may need to change this to grid
        self.curr_page.pack(side=LEFT)
        self.root.update_idletasks()

    def buildNextButton(self):       
        return Button(self.root, text="Next >", command=self.next)

    def buildPrevButton(self):
        return Button(self.root, text="< Prev", command=self.prev)

    def next(self):
        try:
            next = self.curr_page.next()
        except AHREAPage.ImplementationError as e:
            print e.msg

        if next:
            self.displayPage(next)

    def prev(self):
        try:
            prev = self.curr_page.prev()
        except AHREAPage.ImplementationError as e:
            print e.msg

        if prev:
            self.displayPage(prev)

     


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()               
        



class AHREAMenu(Menu):
    def __init__(self, daRoot):
        Menu.__init__(self, daRoot)
        self.root = daRoot
        self.buildFile()
        self.buildSettings()
        self.buildHelp()
        self.dialog = None


    def buildFile(self):
        filemenu = Menu( self )
        self.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Load Settings...", command=self.load_settings)
        filemenu.add_command(label="Save Settings...", command=self.save_settings)

    def buildSettings(self):
        settingsmenu = Menu( self )
        self.add_cascade(label="Settings", menu=settingsmenu)
        settingsmenu.add_command(label="Data...", command=self.data_settings)
        settingsmenu.add_command(label="Dirac...", command=self.dirac_settings)
        settingsmenu.add_command(label="TSP...", command=self.tsp_settings)
        settingsmenu.add_command(label="k-TSP...", command=self.ktsp_settings)
        settingsmenu.add_command(label="TST...", command=self.tst_settings)
        settingsmenu.add_command(label="Adaptive...", command=self.adaptive_settings)
         
    def buildHelp(self):
        helpmenu = Menu(self)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Content", command=self.unImplemented)
        helpmenu.add_command(label="Report a Problem", command=self.unImplemented)
        helpmenu.add_command(label="About", command=self.unImplemented)

    def dirac_settings(self):
        if self.dialog is None:
            self.settings_display("dirac", self.dirac_settings_write)

    def data_settings(self):
        if self.dialog is None:
            self.settings_display("datatable", self.data_settings_write)

    def data_settings_write(self):
        self.settings_write("datatable")
        self.dialog.destroy()
        self.dialog = None

    
    def settings_display(self, learner, write_function):
        dialog = self.dialog = Toplevel(self.root)
        self.dialog.protocol('WM_DELETE_WINDOW', self.close_window)
        self.dialog.title(learner + " settings")
        settings = self.root.controller.config.getSettings(learner)
        self.entries = []
        for i, setting in enumerate(settings):
            Label(dialog, text=setting[0]).grid(row=i, column=0)
            c_off = 1
            for j,val in enumerate(setting[1]):
                e = Entry(dialog)
                e.insert(0,val)
                self.entries.append(e)
                e.grid(row=i, column=c_off+j)
        b = Button(dialog, text="OK", command=write_function)
        b.grid(row=len(settings), column=0)
       
    def close_window(self):
        self.dialog.destroy()
        self.dialog = None

    def settings_write(self, learner):
        settings = self.root.controller.config.getSettings(learner)
        curr_entry = 0
        for setting in settings:
            config_list = []
            for x in setting[1]:
                vals = self.entries[curr_entry].get()
                config_list.append(vals)
                curr_entry += 1
            self.root.controller.config.setSetting(learner, setting[0], config_list)

        self.dialog.destroy()
    def dirac_settings_write(self):
        self.settings_write("dirac")
        self.dialog.destroy()
        self.dialog = None

    def tsp_settings(self):
        if self.dialog is None:
            self.settings_display("tsp", self.tsp_settings_write)
    def tsp_settings_write(self):
        self.settings_write("tsp")
        self.dialog.destroy()
        self.dialog = None

    def ktsp_settings(self):
        if self.dialog is None:
            self.settings_display("ktsp", self.ktsp_settings_write)
    def ktsp_settings_write(self):
        self.settings_write("ktsp")
        self.dialog.destroy()
        self.dialog = None

    def tst_settings(self):
        if self.dialog is None:
            self.settings_display("tst", self.tst_settings_write)

    def tst_settings_write(self):
        self.settings_write("tst")
        self.dialog.destroy()
        self.dialog = None

    def adaptive_settings(self):
        if self.dialog is None:
            self.settings_display("adaptive", self.adaptive_settings_write)

    def adaptive_settings_write(self):
        self.settings_write("adaptive")
        self.dialog.destroy()
        self.dialog = None


    def save_settings(self):        
        options = {}
        options['defaultextension'] = '' # couldn't figure out how this works
        options['filetypes'] = [('xml config', '.xml')]
        options['initialdir'] = 'data'
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Save config'
        filename = tkFileDialog.asksaveasfilename(**options)
        if filename:
            self.root.controller.config.writeSettings(filename)

    def load_settings(self):
        options = {}
        options['defaultextension'] = '' # couldn't figure out how this works
        options['filetypes'] = [('xml config', '.xml')]
        options['initialdir'] = 'data'
        options['initialfile'] = 'config.xml'
        options['parent'] = self
        options['title'] = 'Load config'
        filename = tkFileDialog.askopenfilename(**options)
        if filename:
            self.root.controller.config = SettingsParser(filename)


    def unImplemented(self):
        print "unimplemented"

