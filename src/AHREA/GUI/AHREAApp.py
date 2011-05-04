from Tkinter import *
import traceback, tkMessageBox
import Tkconstants, tkFileDialog
import AHREA
import AHREA.GUI.AHREAPage as AHREAPage
from AHREA.parser.SettingsParser import *
import os.path
import shutil
import sys
import platform
class AHREAApp(Frame):
    def __init__(self, root, controller):
        root.report_callback_exception = self.report_callback_exception
        Frame.__init__(self, root)
        self.root = root
        self.root.title( "AUREA - Adaptive Unified Relative Expression Analyser")
        self.controller = controller
        #start on welcome page

        self.curr_page = None
        self.pages = []
        self.menu = AHREAMenu(self)
        self.remote = AHREARemote(self)
        self.buttonList = self.remote.buttonList
        #self.buildNav()
        #self.layoutNav()
        self.root.config(menu = self.menu)
        self.status = StatusBar(self)#root)
        self.root.grid_columnconfigure(1,minsize=350)
        self.remote.grid(row=0, column=0, sticky=N+E+W)
        self.initPages()
        self.displayPage('welcome')
        numcolumns, numrows = self.grid_size()
        self.status.grid(row=numrows,column=0, columnspan=numcolumns, sticky=W+E+S)
        self.update_idletasks()
        
        self.pack(fill=BOTH)
        
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
        
        self.curr_page.grid(column=1, row=0,sticky=N+S+E+W)
        self.root.update_idletasks()

    def buildNextButton(self):       
        return Button(self.root, text="Next >", command=self.next)

    def buildPrevButton(self):
        return Button(self.root, text="< Prev", command=self.prev)

    def buildNav(self):
        """
        Create button objects
        """
        a=self.home_button = Button(self, text="Home", command=self.nullaction)
        b=self.import_button = Button(self, text="Import Data", command=self.nav_importData)
        c=self.class_button = Button(self, text="Class Definition", command=self.nullaction)
        d=self.settings_button = Button(self, text="Learner Settings", command=self.nullaction)
        e=self.train_button = Button(self, text="Train Classifiers", command=self.nullaction)
        f=self.test_button = Button(self, text="Test Classifiers", command=self.nullaction)
        g=self.evaluate_button = Button(self, text="Evaluate Performance", command=self.nullaction)
        self.buttonList = [a,b,c,d,e,f,g]

    def layoutNav(self):
        """
        Layout Button objects
        """
        stickyicky = E+W
        for i,button in enumerate(self.buttonList):
            #button.configure(state=DISABLED)
            button.grid(row=i, column=0, sticky=stickyicky )

    def nullaction(self):
        pass

    def nav_importData(self):
        self.displayPage('filebrowse')

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


    def report_callback_exception(self, *args):
        """
        displays exceptions
        TYVM : http://stackoverflow.com/questions/4770993/silent-exceptions-in-python-tkinter-should-i-make-them-louder-how
        """
            
        err = traceback.format_exception(*args)
        #print "AHREAAPP.py-line 99 -debug"
        #for e in err:
            #print e
       
        #please report
        msg = "An Error has occurred."
        #err.append(msg)
        t = Toplevel(self)
        #t.protocol('WM_DELETE_WINDOW', t.close_window)
        t.title("Oh Noes!!!! Error!!!!!")
        Label(t,text=msg).pack()
        import os
        errmsg = 'Please copy this error and go to https://github.com/JohnCEarls/AHREAPackage/issues to report it'+ os.linesep()
        errmsg += '(You may have to use Control-C or Apple-C to copy.)'+ os.linesep
        errmsg +=os.linesep.join(err)
        errBox = Text(t,wrap=WORD)
        errBox.pack()
        errBox.insert(END, errmsg) 
        #errBox.config(state=DISABLED)
        #Button(t,text="Copy Error", command=copyError)
        #tkMessageBox.showerror('AHREA: Error', err)


class StatusBar(Frame):
    """
    Note the statusbar is a child of the root
    """
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
        

class AHREARemote(Frame):
    """
    This frame acts as the remote control for the gui.
    """
    #Dependency enum, these should be static
    DataImport = 0
    NetworkImport = 1
    ClassCreation = 2
    TrainDirac = 3
    TrainTSP = 4
    TrainTST = 5
    TrainKTSP = 6
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.m = master
        self.buildNav()
        self.layoutNav()

    def buildNav(self):
        """
        Create button objects
        """
        a=self.home_button = Button(self, text="Home", command=self.nullaction)
        b=self.import_button = Button(self, text="Import Data", command=self.nullaction)
        c=self.class_button = Button(self, text="Class Definition", command=self.nullaction)
        d=self.settings_button = Button(self, text="Learner Settings", command=self.nullaction)
        e=self.train_button = Button(self, text="Train Classifiers", command=self.nullaction)
        f=self.test_button = Button(self, text="Test Classifiers", command=self.nullaction)
        g=self.evaluate_button = Button(self, text="Evaluate Performance", command=self.nullaction)
        self.buttonList = [a,b,c,d,e,f,g]
        welcome_img = os.path.join(self.m.controller.workspace, 'data', 'AUREA-logo-200.pgm')
        self.photo = photo = PhotoImage(file=welcome_img)
        self.plabel = Label(self,  image=photo)

    def layoutNav(self):
        """
        Layout Button objects
        """
        for i,button in enumerate(self.buttonList):
            button.grid(row=i, column=0, sticky=E+W,padx=3, pady=4 )
        self.plabel.config(width=200)
        self.plabel.grid(row=len(self.buttonList), column=0)
            

        #self.pack()

    def nullaction(self):
        raise Exception("""sadfasf ssssssssssssssadfasf
adfasadfasf adfasf adfasf adfasf adfasf 
aaaaaaadfasf adfasf adfasf adfasf adfasf adfasf 
dfasf adfasf adfasf adfasf adfasf adfasf 
dfasf adfasf adfasf adfasf adfasf adfasf 
dfasf adfasf adfasf adfasf adfasf adfasf 
dfasf adfasf adfasf adfasf adfasf adfasf 
dfasf adfasf adfasf adfasf adfasf adfasf 
dfasf adfasf adfasf adfasf adfasf adfasf 
adfasf  pass""")



class AHREAMenu(Menu):
    def __init__(self, daRoot):
        Menu.__init__(self, daRoot)
        self.root = daRoot
        self.buildFile()
        #self.buildSettings()
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
        helpmenu.add_command(label="Report a Problem", command=self.reportProblem)
        helpmenu.add_command(label="About", command=self.about)

    def reportProblem(self):
        msg = "Please go to https://github.com/JohnCEarls/AHREAPackage/issues to report any bugs. Thank you for helping make AHREA better."
        tkMessageBox.showinfo("AHREA: report error", msg)
    
    def about(self):
        msg = "AHREA v. " + AHREA.__version__
        msg += " Copyright (c) 2010-2011 John C. Earls"
        tkMessageBox.showinfo("AHREA", msg)
        

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
        if platform.platform()[0:3] != 'Dar':#mac does not like this
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
        if platform.platform()[0:3] != 'Dar':#mac does not like this
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

