#!/usr/bin/env python2

from debugger import Debugger
from gi.repository import Gtk, Gdk


TITLE = "MikroRechner-Projekt EmulatorUi"
BUTTON_OPEN_TEXT = "Open"
BUTTON_START_TEXT = "Start"
BUTTON_STEP_OVER = "Step over"
BUTTON_STEP_INTO = "Step into"
BUTTON_STOP = "Stop"
BUTTON_REGISTER_AS_DECIMAL = "Decimal"
BUTTON_REGISTER_AS_HEX = "Hex"

LABEL_FLAG_ZERO = "Z"
LABEL_FLAG_NEGATIVE = "N"
LABEL_FLAG_CARRY = "C"
LABEL_FLAG_OVERFLOW = "O"

LABEL_REGISTER_DEFAULT = "R"

LABEL_TITLE_CONTENT_KIT = ": "

class DebuggerUi(Gtk.Window):


    def __init__(self):


        Gtk.Window.__init__(self, title=TITLE)

        # chose a box layout for the ui.
        self.main = Gtk.VBox(False)
        self.buttonBox = Gtk.HBox(spacing=8)
        self.labelBox = Gtk.Box(spacing=8)
        self.registerGrid = Gtk.Grid()

        
        self.initButtons()

        self.initFlagLabel()

        self.initRegisterLabel()

        self.initTextView()
        
        # variables.
        self.debugger_is_running = False
        self.processing_file = False
        self.flags = [False]*4
        self.debugger = None
        self.registerFormat = 16 # hexa-decimal output per default


        # actual nesting of the components
        # nest label box into button "panel"
        self.buttonBox.pack_end(self.labelBox, True, True, 0)
        # nest buttons box in a VBox, disables vertical resizing.
        self.main.pack_start(self.buttonBox, False, False, 0)
        self.main.pack_start(self.registerGrid, False, False, 2)
        self.main.pack_end (self.scrolledwindow, True, True, 16)
        self.add(self.main)


        self.disableManipulation()


    #behaviour definition for the open button. this buttons purpose is to enable the user to feed a file to the application.
    def open_button_clicked(self, widget):
        if not self.debugger_is_running:
            dialog = Gtk.FileChooserDialog("Please choose a file", self,
                Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.filename = dialog.get_filename()
                self.debugger =  Debugger.loadFromFile(self.filename)
                self.enableManipulation()

            
            dialog.destroy()



    #behaviour definition for the normal start button. Makes the debugger impl start executing a loaded file,
    # if existent, until the first occurrence of a breakpoint (TODO: to be developed.)
    def start_button_clicked(self, widget):
        if self.debugger and not self.debugger_is_running:
            #set running status to true
            self.debugger_is_running = True

            self.debugger.run()
            self.debugger_is_running = False
            self.disableManipulation()
            return 0

    #behaviour definition for the button "deep line execution" or "step into"
    def execute_step_into(self, widget):
        self.startButton.set_sensitive(False)
        moreToExecute = self.debugger.step()
        self.populateChanges()
        if not moreToExecute:
            self.disableManipulation()
        return 0

    #behaviour definition for the button "single line execution" or "step over". Semantik: disables start button.
    def execute_step_over(self, widget):
        if not self.debugger:
            return 0
        self.debugger_is_running = True
        moreToExecute = self.debugger.stepOver()
        self.populateChanges()
        self.debugger_is_running = False
        if not moreToExecute:
            self.disableManipulation()
            self.debugger.reset()
            self.clearUi()
        return 0

    def stop_button_clicked(self, widget):
        self.disableManipulation()
        self.debugger.reset()
        self.clearUi()
        self.debugger_is_running = False
        return 0

    def switch_register_display(self, button, button_name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        if button_name == BUTTON_REGISTER_AS_HEX:
            self.registerFormat = 16
        elif button_name == BUTTON_REGISTER_AS_DECIMAL:
            self.registerFormat = 10
        # call populate to make the change visible
        self.populateChanges()

    def populateChanges(self):
        self.populateFlagStatus()
        self.populateRegisterContent()
        line_count = self.textbuffer.get_line_count()
        iterator = self.textbuffer.get_end_iter()
        iterator.backward_line()
        self.textbuffer.delete(iterator, self.textbuffer.get_end_iter())
        last = self.debugger.getLastExecutedCommand()
        if not last:
            last = "Start executing provided program content stepwise..." 
        self.textbuffer.insert(self.textbuffer.get_end_iter(), "I just executed: " + last + "\n")
        self.textbuffer.insert(self.textbuffer.get_end_iter(), "I will do next: " + self.debugger.getNextCommand() + "\n")

    # populates flag status changes to the frontend.
    def populateFlagStatus(self):
        flags = self.debugger.flags
        if self.flags != flags:
            self.flagZero.set_markup(LABEL_FLAG_ZERO + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='red'>"+str(flags[0])+"</span></b>")
            self.flagNegative.set_markup(LABEL_FLAG_NEGATIVE + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='red'>"+str(flags[1])+"</span></b>")
            self.flagCarry.set_markup(LABEL_FLAG_CARRY + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='red'>"+str(flags[2])+"</span></b>")
            self.flagOverflow.set_markup(LABEL_FLAG_OVERFLOW + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='red'>"+str(flags[3])+"</span></b>")
            self.flags = flags
        else:
            self.flagZero.set_markup(LABEL_FLAG_ZERO + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='#000000'>"+str(flags[0])+"</span></b>")
            self.flagNegative.set_markup(LABEL_FLAG_NEGATIVE + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='#000000'>"+str(flags[1])+"</span></b>")
            self.flagCarry.set_markup(LABEL_FLAG_CARRY + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='#000000'>"+str(flags[2])+"</span></b>")
            self.flagOverflow.set_markup(LABEL_FLAG_OVERFLOW + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='#000000'>"+str(flags[3])+"</span></b>")

    # populates register status changes to the frontend.
    def populateRegisterContent(self):
        cpuRegs = self.debugger.register
        for i in range(0, 16):
            content = cpuRegs[i]
            if self.registerFormat == 16:
                content = hex(content)
            oldContent = self.register[i][1]
            if content != oldContent:
                self.register[i][0].set_markup(LABEL_REGISTER_DEFAULT + str(i) + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='red'>" + str(content) + "</span></b>")
            elif content == False:
                self.register[i][0].set_markup(LABEL_REGISTER_DEFAULT + str(i) + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='#000000'>" + str(0) + "</span></b>")
            else:
                self.register[i][0].set_markup(LABEL_REGISTER_DEFAULT + str(i) + LABEL_TITLE_CONTENT_KIT + "<b><span foreground='#000000'>" + str(content) + "</span></b>")
            self.register[i][1] = content

    def clearUi(self):
        self.flagZero.set_markup(LABEL_FLAG_ZERO)
        self.flagNegative.set_markup(LABEL_FLAG_NEGATIVE)
        self.flagCarry.set_markup(LABEL_FLAG_CARRY)
        self.flagOverflow.set_markup(LABEL_FLAG_OVERFLOW)
        for i in range(0, 16):
            self.register[i][0].set_markup(LABEL_REGISTER_DEFAULT + str(i))
            self.register[i][1] = False
        self.textbuffer.set_text("")

    # enables all buttons which are responsible for guaranteeing user-interaction with the executional part of the system.
    # disables the "open file" button.
    def enableManipulation(self):
        self.startButton.set_sensitive(True)
        self.stepOverButton.set_sensitive(True)
        self.stepIntoButton.set_sensitive(True)
        self.stopButton.set_sensitive(True)
        self.openButton.set_sensitive(False)
        # TODO: enable when button has function
        #self.stepIntoButton.set_sensitive(True)

    # disables all buttons, except for the "open file" button which gets enabled.
    def disableManipulation(self):
        self.startButton.set_sensitive(False)
        self.stepOverButton.set_sensitive(False)
        self.stepIntoButton.set_sensitive(False)
        self.stopButton.set_sensitive(False)
        self.openButton.set_sensitive(True)

    # initialises the labels and add them to their own container.
    def initFlagLabel(self):
        # status flag label, flags are zero, negative, carry and overflow
        self.flagZero = Gtk.Label(LABEL_FLAG_ZERO)
        self.flagNegative = Gtk.Label(LABEL_FLAG_NEGATIVE)
        self.flagCarry = Gtk.Label(LABEL_FLAG_CARRY)
        self.flagOverflow = Gtk.Label(LABEL_FLAG_OVERFLOW)
        self.labelBox.pack_start(self.flagZero, True, True, 0)
        self.labelBox.pack_start(self.flagNegative, True, True, 2)
        self.labelBox.pack_start(self.flagCarry, True, True, 4)
        self.labelBox.pack_start(self.flagOverflow, True, True, 6)

    # initialises the buttons for this application and adds them to their dedicated container.
    def initButtons(self):
        #open files
        self.openButton = Gtk.Button(BUTTON_OPEN_TEXT)
        self.openButton.connect("clicked", self.open_button_clicked)
        self.buttonBox.pack_start(self.openButton, True, True, 0)

        #start button
        self.startButton = Gtk.Button(BUTTON_START_TEXT)
        self.startButton.connect("clicked", self.start_button_clicked)
        self.buttonBox.pack_start(self.startButton, True, True, 2)

        # debugging buttons
        self.stepOverButton = Gtk.Button(BUTTON_STEP_OVER)
        self.stepOverButton.connect("clicked", self.execute_step_over)
        self.buttonBox.pack_start(self.stepOverButton, True, True, 4)

        self.stepIntoButton = Gtk.Button(BUTTON_STEP_INTO)
        self.stepIntoButton.connect("clicked", self.execute_step_into)
        self.buttonBox.pack_start(self.stepIntoButton, True, True, 6)

        self.stopButton = Gtk.Button(BUTTON_STOP)
        self.stopButton.connect("clicked", self.stop_button_clicked)
        self.buttonBox.pack_start(self.stopButton, True, True, 8)

        self.registerAsHexButton = Gtk.RadioButton.new_with_label_from_widget(None, BUTTON_REGISTER_AS_HEX)
        self.registerAsHexButton.connect("toggled", self.switch_register_display, BUTTON_REGISTER_AS_HEX)
        self.buttonBox.pack_end(self.registerAsHexButton, False, False, 0)

        self.registerAsDecimalButton = Gtk.RadioButton.new_from_widget(self.registerAsHexButton)
        self.registerAsDecimalButton.set_label(BUTTON_REGISTER_AS_DECIMAL)
        self.registerAsDecimalButton.connect("toggled", self.switch_register_display, BUTTON_REGISTER_AS_DECIMAL)
        self.buttonBox.pack_end(self.registerAsDecimalButton, False, False, 1)

    def initRegisterLabel(self):
        self.register = [[False, False]]*16
        for i in range(0, 16):
            self.register[i] = [Gtk.Label(LABEL_REGISTER_DEFAULT + str(i) + LABEL_TITLE_CONTENT_KIT), False]
            self.register[i][0].set_width_chars(25)
            self.register[i][0].set_alignment(0, 0)
            if(i == 0):
                self.registerGrid.attach(self.register[i][0], 1, 0, 1, 1)
            elif(i < 8):
                self.registerGrid.attach_next_to(self.register[i][0], self.register[i-1][0], Gtk.PositionType.BOTTOM, 1, 1)
            else:
                self.registerGrid.attach_next_to(self.register[i][0], self.register[i-8][0], Gtk.PositionType.RIGHT, 1, 1)


    def initTextView(self):
        """Inits the textview as content of a scrolledwindow. Exports its textbuffer to the object wide variable textbuffer."""
        page_size = Gtk.Adjustment(lower=10, page_size=100)
        self.scrolledwindow = Gtk.ScrolledWindow(page_size)
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        #export the textbuffer to variable with object wide scale, name self.textbuffer
        self.textbuffer = textview.get_buffer()
        
        self.scrolledwindow.add(textview)

    
def on_key_press_event(widget, event):
    keyname = Gdk.keyval_name(event.keyval)
    if(keyname == "Q" or keyname == "q"):
        Gtk.main_quit()


if __name__ == "__main__":
    window = DebuggerUi()
    window.connect("delete-event", Gtk.main_quit)
    window.connect('key_press_event', on_key_press_event)
    window.show_all()
    Gtk.main()
