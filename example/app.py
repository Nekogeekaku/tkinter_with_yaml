from tkinter import *
from tkinter import ttk
import commands

import yaml

debug=False

def log_debug(text):
    if debug:
        print(text)



class Widget:
    def __init__(self, parent):
        self.parent = parent
        self.load_attributes()
    def load_attributes(self,attributeDefinitions):
        self.attributes = {}
        log_debug(attributeDefinitions)
        for key, value in attributeDefinitions.items():
            self.attributes[key] = value



           

class WidgetButton(Widget):
    attributes = None
    element= None
    command = None
    def __init__(self, parent,yamdefinition):
        pass

        super().load_attributes(yamdefinition['WidgetButton']['attributes'])
        log_debug('------------')
        log_debug('WidgetButton __init__')
        log_debug(yamdefinition['WidgetButton']["command"])
        log_debug(getattr(commands, yamdefinition['WidgetButton']["command"]))
        self.command = getattr(commands, yamdefinition['WidgetButton']["command"]) 

        self.element = ttk.Button(parent,text= self.attributes["text"],command=self.handle_command)


        self.element.grid(column=self.attributes["column"], row=self.attributes["row"])
    def handle_command(self):
        log_debug("Command called")
        self.command()
        
 # func = getattr(Module, 'randint') 





class WidgetLabel(Widget):
    attributes = None
    element= None
    def __init__(self, parent,yamdefinition):
        pass
        log_debug(parent)
        log_debug(yamdefinition)

        log_debug(yamdefinition['WidgetLabel'])

        log_debug(yamdefinition['WidgetLabel']['attributes'])
        log_debug('------------')
        super().load_attributes(yamdefinition['WidgetLabel']['attributes'])

        self.element = ttk.Label(parent,text= self.attributes["text"])
        # self.element.text = self.attributes["text"] ça c'est pas possible, il faut le déclarer avant.

        self.element.grid(column=self.attributes["column"], row=self.attributes["row"])


# documentation for all the attributes and widgets
# https://tkdocs.com/shipman/
class RootWindow:
    root= None
    frm= None
    attributes = None
    frame_attributes = None
    use_frame= NO
    widgets= []
    def __init__(self, gui):
        log_debug('--------------------------------------------------------------------------')
        log_debug('RootWindow __init__')

        self.root = Tk()
        log_debug(f"root:{self.root}")
        # load the attributes
        self.load_attributes()
 


        self.root.title(self.attributes['title'])
        self.root.geometry(self.attributes['geometry']) # la taille de la fenêtre.
        log_debug(f"use_frame:{self.attributes['use_frame']}")
        if self.attributes['use_frame']:
            log_debug("has frame")
            use_frame = YES
            self.load_frame_attributes()
            self.frm = ttk.Frame(self.root, padding=self.frame_attributes["padding"])
            self.frm.grid()
            

        log_debug(f"root:{self.root.title}")
        # Process each widget    
        for widget in gui['application']['widgets']:
            # print(widget)
            # The first element is always the widget type
            first_key = next(iter(widget))
            widget_type = first_key
            # widget.pop(first_key)
            # print(widget)
            # print(widget_type)

            #todo later : get class its name
            if widget_type=="WidgetLabel":
                widget = WidgetLabel(self.frm,widget)
                self.widgets.append(widget)

            if widget_type=="WidgetButton":
                widget = WidgetButton(self.frm,widget)
                self.widgets.append(widget)






        # text = Text(frm, height=8) 
        # scroll = Scrollbar(frm) 
        # text.configure(yscrollcommand=scroll.set) 
        # # text.pack(side=LEFT) 
        
        # scroll.config(command=text.yview) 
        # # scroll.pack(side=RIGHT, fill=Y) 
        # text.grid(column=0,row=0,columnspan = 2, sticky = W+E)
        # # Label(frm, text =description).grid(column=0, row=0)
        # text.insert(END, description) 
        # button_lauch = ttk.Button(frm,text=launchLabel)
        # button_lauch.grid(column=0, row=2)
        # button_lauch.bind("<Button-1>", launchFunction)

        # button_close = ttk.Button(frm,text="Fermer")
        # button_close.grid(column=1, row=2)
        # button_close.bind("<Button-1>", lambda e:self.close_window())
 

    def load_attributes(self):
        self.attributes = {}

        for key, value in gui['application']['attributes'].items():
            self.attributes[key] = value
    def load_frame_attributes(self):
        self.frame_attributes = {}

        for key, value in gui['application']['frame_attributes'].items():
            self.frame_attributes[key] = value

    def close_window(self):
        self.destroy()




if __name__ == '__main__':

    print('launching app')


    with open('gui.yaml', 'r') as file:
        gui = yaml.safe_load(file)
    log_debug('----------------------------------------------------------------------')
    log_debug(gui)
    log_debug('----------------------------------------------------------------------')
    log_debug('  ')
    rootWindow = RootWindow(gui)

    log_debug(rootWindow.widgets)
    rootWindow.root.mainloop()

