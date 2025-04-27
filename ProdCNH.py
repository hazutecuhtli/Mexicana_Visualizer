'''*************************************************************************************************
Importing libraries
*************************************************************************************************'''
# Standard Libraries
import requests, zipfile, io, os, shutil
import math
import webbrowser
from datetime import datetime

# Third-Party Libraries
import matplotlib
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, Listbox, Entry, BOTH, LEFT, RIGHT, PanedWindow, Frame, Label, StringVar, messagebox
from tkinter import Button, Scrollbar, Y, X, YES, END, BOTTOM, font, Checkbutton, BooleanVar
from tkinter.filedialog import asksaveasfilename
from pandas import ExcelWriter

# Matplotlib Backend for Tkinter
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.cm as cm    

'''*************************************************************************************************
Defining GUI class
*************************************************************************************************'''

class MexicanaGUI(tk.Frame):

    '''
    Class for creating a Tkinter-based GUI to visualize oil and gas production data
    published by the Mexican National Hydrocarbons Commission (CNH).
    '''

    #-----------------------------------------Class constructor-------------------------------------
    def __init__(self, master=None):

        '''
        Initializing the Tkinter GUI
        '''
        
        bgColor = "#1e7b1e"
        tk.Frame.__init__(self, master, width=800, height=400)
        self.master.title("Mexicana, Smart Solutions")
        self.master.configure(background=bgColor)
        self.master.iconbitmap(os.path.join(os.getcwd(),'mssoil.ico'))
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (w, h))
        self.Resultados = Listbox()
        self.Search1 = Entry(self.master, width=40)
        self.FoundResults = []
        self.PannedWindowsConst()

    #--------------------------------Creating main fucntion for the class---------------------------
    
    def PannedWindowsConst(self):

        '''
        Method to create the panned windows of the class
        '''

        #Bottoms border space
        self.master['padx'] = 5
        self.master['pady'] = 5

        #Defining workspace characteristics dependening on the screen resolution
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        if h == 617:
            self.butheight= 1
            self.butwidth= int(w/1200)
            self.butheight2= 1
            self.butwidth2= int(w/40)
            offset = 40
            self.sizeArial12 = int(w/120)
            self.sizeArial15 = int(w/120)
            self.sizehelv20 = int(w/96)
            self.sizehelv18 = int(w/104)
        elif h == 720:
            self.butheight= 1
            self.butwidth= int(w/192)
            self.butheight2= 1
            self.butwidth2= int(w/60)
            offset = 20
            self.sizeArial12 = int(w/100)
            self.sizeArial15 = int(w/100)
            self.sizehelv20 = int(w/96)
            self.sizehelv18 = int(w/104)
        else:
            self.butheight= 1
            self.butwidth= int(w/192)
            self.butheight2= 1
            self.butwidth2= int(w/80)
            offset = 0
            self.sizeArial12 = int(w/120)
            self.sizeArial15 = int(w/120)
            self.sizehelv20 = int(w/96)
            self.sizehelv18 = int(w/104)

        #Defining fonts to be used
        Arial15 = font.Font(family='Arial', size=self.sizeArial15)
        helv20 = font.Font(family='Helvetica', size=self.sizehelv20)
        helv18 = font.Font(family='Helvetica', size=self.sizehelv18)
        Arial12 = font.Font(family='Arial', size=self.sizeArial12)
        self.Font = Arial15

        #Defining colors and styles to be used
        bgColor = "#1e7b1e"
        mygray = "#c2c2a3"
        mygray2 = "#e0e0d1"
        mygray3 = "#B8D1A7"

        style = ttk.Style()

        style.theme_create( "yummy", parent="alt", settings={
                "TNotebook": {"configure": {"tabmargins": [10, 10, 10, 0] } },
                "TNotebook.Tab": {
                    "configure": {"padding": [5, 1], "background": mygray ,"font" : Arial15},
                    "map":       {"background": [("selected", mygray2)],
                                  "expand": [("selected", [10, 10, 1, 0])] } } } )

        #Creating the space to plot on the canvas framework    
        self.fig = Figure(figsize=(15,7))
        self.a = self.fig.add_subplot(1, 1, 1)
        self.b = self.a
        self.name = []

        self.FW = Checkbutton(self.master)
        self.Sel_FW = BooleanVar(self.master)
        self.Sel_FW.set(False)
        
        self.Accum = Checkbutton(self.master)
        self.Sel_Acum = BooleanVar(self.master)
        self.Sel_Acum.set(False)

        self.PozosOpe = Checkbutton(self.master)
        self.Sel_PozosOpe = BooleanVar(self.master)
        self.Sel_PozosOpe.set(False)

        self.check_RXY = Checkbutton(self.master)
        self.Sel_RXY = BooleanVar(self.master)
        self.Sel_RXY.set(False)

        self.check_Chan = Checkbutton(self.master)
        self.Sel_Chan = BooleanVar(self.master)
        self.Sel_Chan.set(False)

        self.check_Res = Checkbutton(self.master)
        self.Sel_Res = BooleanVar(self.master)
        self.Sel_Res.set(False)

        self.check_Res2 = Checkbutton(self.master)
        self.Sel_Res2 = BooleanVar(self.master)
        self.Sel_Res2.set(False)

        self.check_Res3 = Checkbutton(self.master)
        self.Sel_Res3 = BooleanVar(self.master)
        self.Sel_Res3.set(False)            

        self.Checkbox_Field = Checkbutton(self.master)
        self.Checkbox_Well = Checkbutton(self.master)
        self.Seleccion_Field = BooleanVar(self.master)
        self.Seleccion_Well =BooleanVar(self.master)
        
        self.Checkbox_Oil = Checkbutton(self.master)
        self.Checkbox_Water = Checkbutton(self.master)
        self.Checkbox_Gas = Checkbutton(self.master)
        self.Seleccion_Oil = BooleanVar(self.master)
        self.Seleccion_Water = BooleanVar(self.master)
        self.Seleccion_Gas = BooleanVar(self.master)

        self.Seleccion_Oil.set(True)
        self.Seleccion_Water.set(True)
        self.Seleccion_Gas.set(True)

        self.Checkboxes = {}
        self.Seleccion={}
     
        
        #Defining self variables to use, related with the pandas dataframe used
        self.indexs = []
        self.PozosInteres = []
        self.CamposInteres = []
        self.sheetname = ''
        
        #Defining the images that will be used in the Notebook
        PemexLogo = tk.PhotoImage(file=os.path.join(os.getcwd(),'PEMEXLogo.gif'))
        MXLogo = tk.PhotoImage(file=os.path.join(os.getcwd(),'índice.gif'))
        CNHLogo = tk.PhotoImage(file=os.path.join(os.getcwd(),'CNHLogo.gif'))
        FMILogo = tk.PhotoImage(file=os.path.join(os.getcwd(),'FMILogo.gif'))
        OCDELogo = tk.PhotoImage(file=os.path.join(os.getcwd(),'OCDELogo.gif'))      

        #Master PanedWindow - Main window, windows workspace, backgrund windown  
        SearchWindow = tk.PanedWindow(self.master, orient=tk.HORIZONTAL, bd=1,
                                 sashwidth=2, sashpad=5, sashrelief=tk.RAISED,
                                 showhandle=False, bg=bgColor)
        SearchWindow.grid(row=0, column=0, sticky ="nsew")  #Displaying wht main windows
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)        
        SearchWindow.pack(fill=BOTH, expand=1)

        #PanedWindow containing the Mexicana search - Window that contains the search interface
        SearchWindowb = PanedWindow(SearchWindow, orient=tk.VERTICAL, bd=1,
                                 sashwidth=2, sashpad=5, sashrelief=tk.RAISED,
                                 showhandle=False, width=w/4, bg=bgColor)

        SearchWindow.add(SearchWindowb) # Adding the search window to the main window
        topframe = Frame(SearchWindowb, bg="white", height=h/2+offset, width=w/4)   #Creaing a frame to put the user search interface

        '''Size of images depending on the screen resolution'''
        if h == 617:
            TopframeImage = tk.PhotoImage(file=os.path.join(os.getcwd(),'logo_mss_small.gif'))             
        elif h == 720:
            TopframeImage = tk.PhotoImage(file=os.path.join(os.getcwd(),'logo_mss_small.gif')) 
        else:
            TopframeImage = tk.PhotoImage(file=os.path.join(os.getcwd(),'logo_mss_normal.gif'))             

        #Creating the space to display the Company logo 
        TopFrameMexicana = Label(topframe, wraplength = 230, fg="white",                                
                            image=TopframeImage, borderwidth=0,compound="center",highlightthickness = 0,
                            padx=0,pady=0)
        TopFrameMexicana.image = TopframeImage

        #Creating the text entry to introduce the search of interest
        self.SearchWord = StringVar()
        self.TextoBusqueda = Entry(topframe, width=self.butwidth2, textvariable=self.SearchWord, font = ("Helvetica", int(w/80)),
                              bg='white', fg='gray')

        self.Checkbox_Field = Checkbutton(topframe, text='Campos', font=Arial15, variable=self.Seleccion_Field,
                                                           onvalue = 1, offvalue = 0, bg='white', command=self.ClearCheckboxWell)
        self.Checkbox_Well = Checkbutton(topframe, text='Pozos', font=Arial15, variable=self.Seleccion_Well,
                                                           onvalue = 1, offvalue = 0, bg='white', command=self.ClearCheckboxField)

        #Creating the bottom to implement the desired search
        BuscarBot = Button(topframe, text='Buscar', font = helv18, height = self.butheight, width=self.butwidth, command=self.GetResults)
        self.TextoBusqueda.bind('<Return>', self.get)

        ActualizarBot = Button(topframe, text='Actualizar', font = helv18, height = self.butheight, width=self.butwidth, command=self.Update)
        self.TextoBusqueda.bind('<Return>', self.get)        

        #Displaying the text entry and bottom search to the search window interface
        TopFrameMexicana.grid(row=1, column=1, columnspan=2)                                         
        self.TextoBusqueda.grid(row=3, column=1, columnspan=2)
        self.Checkbox_Field.grid(row=4, column=1)
        self.Checkbox_Well.grid(row=4, column=2) 
        BuscarBot.grid(row=6, column=2, columnspan=2)
        ActualizarBot.grid(row=6, column=0, columnspan=2)
        
        #Defining the characteristics of the search window dependung on the screen resolution
        if h == 617:
            topframe.grid_rowconfigure(0, minsize=0)
            topframe.grid_rowconfigure(2, minsize=0)
            topframe.grid_columnconfigure(1, weight=1)
            topframe.grid_columnconfigure(0, minsize=0)
        if h == 720:
            topframe.grid_rowconfigure(0, minsize=h/200)
            topframe.grid_rowconfigure(2, minsize=0)
            topframe.grid_columnconfigure(1, weight=0)
            topframe.grid_columnconfigure(0, minsize=30)            
        else:
            topframe.grid_rowconfigure(0, minsize=h/120)
            topframe.grid_rowconfigure(2, minsize=h/40)
            topframe.grid_columnconfigure(1, weight=5)
            topframe.grid_columnconfigure(2, weight=5)
            topframe.grid_columnconfigure(0, minsize=0)

        #Defining the window to contain the search results and links of interest
        bottomframe = Frame(SearchWindowb, bg="#f5f5f0", height=h/2-offset, width=w/4)
        style.theme_use("yummy")                                                                        

        #Creating the space for the search results
        note = ttk.Notebook(bottomframe, width=int(w/4)-8, height=int(h/2)-offset)                          

        #Creating the space for the links of interest
        self.LinksTab = Frame(note)                                                                          
        self.LinksTab.grid_rowconfigure(0, minsize=20)                                                       
        self.LinksTab.grid_columnconfigure(0, minsize=20)
        self.LinksTab.grid_columnconfigure(2, minsize=20)   

        self.Checkbox_Oil = Checkbutton(self.LinksTab, text='ACEITE', font=Arial15, variable=self.Seleccion_Oil,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxOil)
        self.Checkbox_Water = Checkbutton(self.LinksTab, text='AGUA', font=Arial15, variable=self.Seleccion_Water,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxWater)
        self.Checkbox_Gas = Checkbutton(self.LinksTab, text='GAS', font=Arial15, variable=self.Seleccion_Gas,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxGas)

        self.Accum = Checkbutton(self.LinksTab, text='ACUM', font=Arial15, variable=self.Sel_Acum,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxACUM)

        self.PozosOpe = Checkbutton(self.LinksTab, text='POZOS', font=Arial15, variable=self.Sel_PozosOpe,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxPOZOS)

        self.check_RXY = Checkbutton(self.LinksTab, text='RXY', font=Arial15, variable=self.Sel_RXY,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxRGA)

        self.check_Chan = Checkbutton(self.LinksTab, text='CHAN', font=Arial15, variable=self.Sel_Chan,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxChan)

        self.check_Res = Checkbutton(self.LinksTab, text='ACEITE', font=Arial15, variable=self.Sel_Res,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxRes1)

        self.check_Res2 = Checkbutton(self.LinksTab, text='PCE', font=Arial15, variable=self.Sel_Res2,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxRes2)

        self.check_Res3 = Checkbutton(self.LinksTab, text='GAS', font=Arial15, variable=self.Sel_Res3,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxRes3)

        self.check_FW = Checkbutton(self.LinksTab, text='FW%', font=Arial15, variable=self.Sel_FW,
                                                           onvalue = 1, offvalue = 0, bg="#f5f5f0", command=self.ClearCheckboxFW)           
        
        '''Calling functions related to the links of interest'''
        HydroType = Label(self.LinksTab, text="Hydrocarburos:", font=Arial15) 
        Produccion = Label(self.LinksTab, text="Produccion:", font=self.Font)
        Reserv = Label(self.LinksTab, text="Reservas:", font=self.Font)        
        Otros = Label(self.LinksTab, text="Otros:", font=self.Font)
        HydroType.grid(row=1, column=0, columnspan=3, sticky ="W")
        Produccion.grid(row=5, column=0, columnspan=3, sticky ="W")
        Reserv.grid(row=8, column=0, columnspan=5, sticky ="W")
        Otros.grid(row=11, column=0, columnspan=5, sticky ="W")
        self.Checkbox_Oil.grid(row=3, column=1, sticky ="W")
        self.Checkbox_Water.grid(row=3, column=3, sticky ="W")
        self.Checkbox_Gas.grid(row=3, column=5, sticky ="W")
        self.LinksTab.grid_columnconfigure(2, minsize=13)
        self.LinksTab.grid_columnconfigure(4, minsize=13)
        self.LinksTab.grid_columnconfigure(6, minsize=13)
        self.LinksTab.grid_rowconfigure(2, minsize=13)
        self.LinksTab.grid_rowconfigure(4, minsize=25)
        self.Accum.grid(row=6, column=1, sticky ="W")
        self.check_FW.grid(row=7, column=1, sticky ="W")             
        self.PozosOpe.grid(row=13, column=1, sticky ="W")
        self.check_Res.grid(row=9, column=1, sticky ="W")
        self.check_Res2.grid(row=9, column=3, sticky ="W")
        self.check_Res3.grid(row=9, column=5, sticky ="W")        
        self.check_RXY.grid(row=6, column=3, sticky ="W")
        self.check_Chan.grid(row=6, column=5, sticky ="W")    
        
        #Defining the Frame with the search results
        self.ResultadosTab = Frame(note)

        #Displaying the results and links of itnerest windows
        note.add(self.ResultadosTab, text = "Resultados")
        note.add(self.LinksTab, text = "Opciones Grafica")
        note.pack(fill=BOTH, expand=1)

        '''Calling a function to print found results in the search of interest implemented'''
        self.PrintingResults(Arial15, h, w)

        #Creating a window to plot production data from the results of the search implemented
        SearchResults = PanedWindow(SearchWindow, orient=tk.HORIZONTAL, bd=1,
                                 sashwidth=2, sashpad=5, sashrelief=tk.RAISED,
                                 showhandle=True, width=w/4, bg=bgColor)

        #Configuring the characterists of the window created to plot the production data
        SearchResults.config(handlesize=10)
        SearchResults.config(sashwidth=5)
        SearchResults.config(sashrelief=tk.RAISED)

        #Adding the window to display the production data to the main window
        SearchWindow.add(SearchResults)

        #Creating an adding frame to add the canvas to plot the productiond data using matplotlib
        self.rightframe = Frame(SearchResults, bg="white", height=h/2, width=w/8)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.rightframe)
        SearchResults.add(self.rightframe)

        #Definign the functionality of a bottom to save the selected production data
        self.GuardarBot = Button(self.rightframe, text='Guardar', font = helv20, bg=mygray3, command=self.SaveResults)

        #Adding all created windows to the main workspace
        SearchWindow.grid(row=0, column=0, sticky ="nsew")
        SearchWindowb.add(topframe, stretch="always")
        SearchWindowb.add(bottomframe, stretch="always")
        SearchResults.add(self.rightframe, stretch="always")

    #**********************************************************************************************************************
    def clear_checkboxes(self, variables_to_clear=[], reset_oil_water_gas=False):
        """
        Clear a set of BooleanVars and optionally reset Oil, Water, Gas selections.
        
        Args:
            variables_to_clear (list): List of BooleanVar to set to False.
            reset_oil_water_gas (bool): Whether to reset Oil, Water, Gas to True.
        """
        for var in variables_to_clear:
            var.set(False)
        
        if reset_oil_water_gas:
            self.Seleccion_Oil.set(True)
            self.Seleccion_Water.set(True)
            self.Seleccion_Gas.set(True)
        
        self.plotting_wells()

    def ClearCheckboxFW(self):
        self.clear_checkboxes(
            [self.Sel_PozosOpe, self.Sel_RXY, self.Sel_Acum, self.Sel_Chan],
            reset_oil_water_gas=True
        )

    def ClearCheckboxRes1(self):
        self.clear_checkboxes(
            [self.Sel_PozosOpe, self.Sel_RXY, self.Sel_Acum, self.Sel_Res2, self.Sel_Res3, self.Sel_Chan, self.Sel_FW]
        )

    def ClearCheckboxRes2(self):
        self.clear_checkboxes(
            [self.Sel_PozosOpe, self.Sel_RXY, self.Sel_Acum, self.Sel_Res, self.Sel_Res3, self.Sel_Chan, self.Sel_FW]
        )

    def ClearCheckboxRes3(self):
        self.clear_checkboxes(
            [self.Sel_PozosOpe, self.Sel_RXY, self.Sel_Acum, self.Sel_Res, self.Sel_Res2, self.Sel_Chan, self.Sel_FW]
        )

    def ClearCheckboxChan(self):
        self.clear_checkboxes(
            [self.Sel_PozosOpe, self.Sel_RXY, self.Sel_Acum, self.Sel_Res, self.Sel_Res2, self.Sel_Res3, self.Sel_FW],
            reset_oil_water_gas=True
        )

    def ClearCheckboxACUM(self):
        self.clear_checkboxes(
            [self.Sel_PozosOpe, self.Sel_RXY, self.Sel_Chan, self.Sel_Res, self.Sel_Res2, self.Sel_Res3, self.Sel_FW]
        )

    def ClearCheckboxRGA(self):
        self.clear_checkboxes(
            [self.Sel_Acum, self.Sel_PozosOpe, self.Sel_Chan, self.Sel_Res, self.Sel_Res2, self.Sel_Res3, self.Sel_FW],
            reset_oil_water_gas=True
        )

    def ClearCheckboxPOZOS(self):
        self.clear_checkboxes(
            [self.Sel_Acum, self.Sel_RXY, self.Sel_Chan, self.Sel_Res, self.Sel_Res2, self.Sel_Res3, self.Sel_FW]
        )

    def ClearCheckboxOil(self):
        self.clear_checkboxes(
            [self.Sel_RXY, self.Sel_Chan, self.Sel_PozosOpe, self.Sel_FW, self.Sel_Res, self.Sel_Res2, self.Sel_Res3]
        )

    def ClearCheckboxWater(self):
        self.clear_checkboxes(
            [self.Sel_RXY, self.Sel_Chan, self.Sel_PozosOpe, self.Sel_FW, self.Sel_Res, self.Sel_Res2, self.Sel_Res3]
        )

    def ClearCheckboxGas(self):
        self.clear_checkboxes(
            [self.Sel_RXY, self.Sel_Chan, self.Sel_PozosOpe, self.Sel_FW, self.Sel_Res, self.Sel_Res2, self.Sel_Res3]
        )

    def ClearCheckboxField(self):
        self.Seleccion_Field.set(False)

    def ClearCheckboxWell(self):
        self.Seleccion_Well.set(False)
        

    '''*****************************************************************************************************************
    Functions
    *****************************************************************************************************************'''


    #**********************************************************************************************************************
        
    def Update(self):

        #Generating download links
        urlinks = [ 'https://sih.hidrocarburos.gob.mx/downloads/PRODUCCION_POZOS.zip?_='+'25'+datetime.now().strftime('%Y%m%d%H%M%S'),
                    'https://sih.hidrocarburos.gob.mx/downloads/PRODUCCION_CAMPOS.csv?_='+'25'+datetime.now().strftime('%Y%m%d%H%M%S'),
                    'https://sih.hidrocarburos.gob.mx/downloads/POZOS_OPERANDO_CAMPO.csv?_='+'25'+datetime.now().strftime('%Y%m%d%H%M%S'),
                    'https://sih.hidrocarburos.gob.mx/downloads/RESERVAS_CAMPO.csv?_='+'25'+datetime.now().strftime('%Y%m%d%H%M%S')]
                
        paths = ["POZOS", "CAMPOS", "POZOPERANDO", "RESERVAS"]
        names_files = ['Pozos.csv', 'Campos.csv', 'PozosOperando.csv', 'Reservas.csv']
        lim = [10,11, 5, 10]
                
        for n in range(len(paths)):

        # Hacer la solicitud GET
            r = requests.get(urlinks[n])

            # Revisar si la solicitud fue exitosa (status code 200)
            if r.status_code != 200:
                break
                            
            if 'zip' in urlinks[n]:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(os.path.join(os.getcwd(), "Data_SIH", paths[n]))
                path = os.path.join(os.getcwd(), "Data_SIH", paths[n], 'POZOS_COMPILADO.csv')    

            else:
                path = os.path.join(os.getcwd(), "Data_SIH", paths[n], names_files[n])                
                # Guardar el contenido como archivo CSV
                with open(path, "wb") as f:
                    f.write(r.content)

            df = pd.read_csv(path, skiprows=range(lim[n]), encoding='ISO-8859-1', index_col=False)
               

            if n == 0:
                df.Nombre_del_pozo = df.Nombre_del_pozo.str.upper()
                df.Cuenca = df.Cuenca.str.upper()
            elif n == 1:
                df.CAMPO_OFICIAL = df.CAMPO_OFICIAL.str.upper()
                df.CAMPO_SIH = df.CAMPO_SIH.str.upper()
            elif n == 2:
                df.CAMPO = df.CAMPO.str.upper()
                df.CUENCA = df.CUENCA.str.upper()
            elif n == 3:
                df.CAMPO_OFICIAL = df.CAMPO_OFICIAL.str.upper()
                df.CAMPO_SIH = df.CAMPO_SIH.str.upper()

                df_grp = df.groupby(['CAMPO_OFICIAL', 'CAMPO_SIH', 'UBICACION', 'CUENCA', 'FECHA', 'CATEGORIA'])[['PETROLEO_MMB', 'PETROLEO_CRUDO_EQUIVALENTE_MMBPCE', 'GAS_MMMPC']].sum()
                df_grp.reset_index(inplace=True)
                campos = df_grp.CAMPO_SIH.unique()

                for campo in  campos:
                    for col in ['PETROLEO_MMB', 'PETROLEO_CRUDO_EQUIVALENTE_MMBPCE', 'GAS_MMMPC']:
                        UnaP = df_grp[(df_grp.CAMPO_SIH==campo) & (df_grp.CATEGORIA=='1P')][col].values
                        DosP = df_grp[(df_grp.CAMPO_SIH==campo) & (df_grp.CATEGORIA=='2P')][col].values
                        TresP = df_grp[(df_grp.CAMPO_SIH==campo) & (df_grp.CATEGORIA=='3P')][col].values
                    
                        idxs = df_grp[(df_grp.CAMPO_SIH==campo) & (df_grp.CATEGORIA=='2P')].index
                        df_grp.loc[idxs, col] = DosP - UnaP
                        idxs = df_grp[(df_grp.CAMPO_SIH==campo) & (df_grp.CATEGORIA=='3P')].index
                        df_grp.loc[idxs, col] = TresP - DosP

                df_grp.loc[df_grp[df_grp.CATEGORIA=='1P'].index, 'CATEGORIA'] = 'PROBADAS'
                df_grp.loc[df_grp[df_grp.CATEGORIA=='2P'].index, 'CATEGORIA'] = 'PROBABLES'
                df_grp.loc[df_grp[df_grp.CATEGORIA=='3P'].index, 'CATEGORIA'] = 'POSIBLES'
                df = df_grp
                
            df.to_csv(os.path.join(os.getcwd(), 'Datos', names_files[n]), index=False)            

    #**********************************************************************************************************************
                
    def GetResults(self):

        '''
        Function to search for wells with names containing the specific word defined on the implemented search

        '''

        if self.Seleccion_Field.get() == False and self.Seleccion_Well.get() == False:
            messagebox.showerror("Error", "Seleccione si desea buscar produccion por campo o por pozo")
            self.Resultados.delete(0,'end')
            return 0
        
        #Changing the curor shape for a waiting image
        self.config(cursor="wait")

        if self.Seleccion_Well.get():
            
            #Try to implement a seach, if error, then create a dataframe that represent the data base to implement the search
            try:
                self.Pozos['Nombre_del_pozo']
            except:
                pathDataPozos = os.path.join(os.getcwd(), 'Datos','Pozos.csv')
                self.Pozos = pd.read_csv(pathDataPozos, low_memory=False)    

            #Cleaning the search results window
            self.Resultados.delete(0,'end')

            #Implementing the search
            Name = str.lower(self.SearchWord.get()).replace('-',' ').replace('_', ' ')
            Pozos2Look = []

            for pozo1 in self.Pozos.Nombre_del_pozo.unique():
                if Name in pozo1.lower().replace('-',' ').replace('_', ' ')[0:len(Name)]:
                    Pozos2Look.append(pozo1)                 
  
            Results2Look = Pozos2Look

            #Displaying results
            if len(Results2Look) < 1:
                self.Resultados.insert(0, 'NO HAY RESULTADOS')
            else:
                for pozo in list(set(Results2Look)):
                    self.Resultados.insert(0, pozo)

        if self.Seleccion_Field.get():

            pathDataCampos = os.path.join(os.getcwd(), 'Datos','Campos.csv')
            self.Campos = pd.read_csv(pathDataCampos, low_memory=False)
            
            pathDataPozosOpe = os.path.join(os.getcwd(), 'Datos','PozosOperando.csv')
            self.PozosNum = pd.read_csv(pathDataPozosOpe, low_memory=False)

            pathDataReservas = os.path.join(os.getcwd(), 'Datos','Reservas.csv')
            self.Reservas = pd.read_csv(pathDataReservas, low_memory=False)              

            #Cleaning the search results window
            self.Resultados.delete(0,'end')

            #Implementing the search
            Name = str.lower(self.SearchWord.get()).replace('-',' ').replace('_', ' ')
            Campos2Look = []

            for campo in self.Campos.CAMPO_SIH.unique():
                    if Name in campo.lower().replace('-',' ').replace('_', ' ')[0:len(Name)]:
                        Campos2Look.append(campo)                 

            Results2Look = Campos2Look

            #Displaying results
            if len(Results2Look) < 1:
                self.Resultados.insert(0, 'NO HAY RESULTADOS')
            else:
                for pozo in list(set(Results2Look)):
                    self.Resultados.insert(0, pozo)

        #Changing the cursos to a normal image
        self.config(cursor="")              

    #**********************************************************************************************************************

    def plotting_wells(self):

        '''
        Function plot the selected production data

        inputs:
        name -> name of the well to plot the production data

        '''

        #Looking for the screen resolution
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        def prodcols(x, y):
            return x*y

        def fw(x, y):
            if x >0 or y>0:
                res = (y)/(x+y)*100
            else:
                res = np.nan
            return res           

        #Adapting the plot depending on the screen resolution
        if h ==617:
            plt.rcParams.update({'font.size': 8})
            labelssize = 7
            rota = 90
        elif h ==720:
            plt.rcParams.update({'font.size': 9})
            labelssize = 9
            rota = 90
        else:
            plt.rcParams.update({'font.size': 13})
            labelssize = 14
            rota = 90

        if self.Seleccion_Well.get() == True:

            #Creating the data to plot
            self.PozosInteres = self.Pozos[self.Pozos['Nombre_del_pozo'] == str(self.name)]
            pozos = self.PozosInteres.Nombre_del_pozo.unique().tolist()
            self.PozosInteres = self.PozosInteres.reset_index(drop=True)
            self.sheetname = str(self.name)

            fechas = []
            dias = []
            self.check_Chan.grid(row=6, column=5, sticky ="W")
            for date in self.PozosInteres.Fecha:
                dias.append(pd.Period(pd.to_datetime(date).strftime('%d/%m/%Y')).days_in_month)
                fechas.append(pd.to_datetime(date[3:]).strftime('%m/%Y'))
                
            self.PozosInteres.Fecha = fechas
            self.PozosInteres["Dias_Mes"] = dias

            self.PozosInteres["Acum_Petróleo_(Mb)"] = self.PozosInteres.apply(lambda x: prodcols(x["Petróleo_(Mbd)"], x['Dias_Mes']), axis=1)
            self.PozosInteres["Acum_Petróleo_(Mb)"] = self.PozosInteres["Acum_Petróleo_(Mb)"].cumsum()
            self.PozosInteres["Acum_Agua_(Mb)"] = self.PozosInteres.apply(lambda x: prodcols(x["Agua_(Mbd)"], x['Dias_Mes']), axis=1)
            self.PozosInteres["Acum_Agua_(Mb)"] = self.PozosInteres["Acum_Agua_(Mb)"].cumsum()
            self.PozosInteres["Acum_Condensado_(Mb)"] = self.PozosInteres.apply(lambda x: prodcols(x["Condensado_(Mbd)"], x['Dias_Mes']), axis=1)
            self.PozosInteres["Acum_Condensado_(Mb)"] = self.PozosInteres["Acum_Condensado_(Mb)"].cumsum()
            self.PozosInteres["Acum_Gas_asociado_(MMpc)"] = self.PozosInteres.apply(lambda x: prodcols(x["Gas_asociado_(MMpcd)"], x['Dias_Mes']), axis=1)
            self.PozosInteres["Acum_Gas_asociado_(MMpc)"] = self.PozosInteres["Acum_Gas_asociado_(MMpc)"].cumsum()
            self.PozosInteres["Acum_Gas_no_asociado_(MMpc)"] = self.PozosInteres.apply(lambda x: prodcols(x["Gas_no_asociado_(MMpcd)"], x['Dias_Mes']), axis=1)
            self.PozosInteres["Acum_Gas_no_asociado_(MMpc)"] = self.PozosInteres["Acum_Gas_no_asociado_(MMpc)"].cumsum()
            self.PozosInteres["FW(%)"] = self.PozosInteres.apply(lambda x: fw(x["Petróleo_(Mbd)"], x['Agua_(Mbd)']), axis=1)            

            RGAs = []
            RAAs = []
            RAAacum = []
            DiasAcum = []
            Der = []
            Dacum = 0
            RAAcum = 0

            for i, prod in enumerate(self.PozosInteres["Petróleo_(Mbd)"]):
                if prod > 0:
                    RGAs.append((self.PozosInteres["Gas_asociado_(MMpcd)"].iloc[i]*1e6)/(prod*1e3))
                    RAAs.append((self.PozosInteres["Agua_(Mbd)"].iloc[i])/(prod))
                else:
                    RGAs.append(0)
                    RAAs.append(0)
                RAAcum += RAAs[i]
                Dacum += dias[i]
                RAAacum.append(RAAcum)
                DiasAcum.append(Dacum)
                if i == 0:
                    Der.append(RAAcum/Dacum)
                else:
                    Der.append((RAAacum[i] - RAAacum[i-1])/float(Dacum))
                    
            self.PozosInteres["RGA"] = RGAs
            self.PozosInteres["RAA"] = RAAs
            self.PozosInteres["RAA_Acum"] = RAAacum
            self.PozosInteres["RAA'"] = Der
            self.PozosInteres["Dias_Acum"] = DiasAcum            
            
            #Displaying the bottom to save the selected production data
            self.GuardarBot.pack(side = BOTTOM, fill = X )

            #Cleaning the figure axis to plot new production data
            self.a.clear()
            self.b.clear()
            Columns1 = []
            Columns2 = []
            Columns3 = []
            Columns4 = []
            Columns5 = []
            Columns6 = []
            Columns7 = []
            
            #Plotting selected production data
            #if str(self.name) in self.Pozos['Nombre_del_pozo'].unique().tolist():#
            if self.Sel_Acum.get() == False:
                LabelFigure1 = 'Produccion (MBD)'
                LabelFigure2 = 'Produccion (MMPCD)'                
                if self.Seleccion_Oil.get() == True:
                    Columns1 = Columns1 + ['Petróleo_(Mbd)', 'Condensado_(Mbd)']
                if self.Seleccion_Water.get() == True:
                    Columns1.append('Agua_(Mbd)')
                if self.Seleccion_Gas.get() == True:                
                    Columns2 = Columns2 +  ['Gas_asociado_(MMpcd)', 'Gas_no_asociado_(MMpcd)']
            else:
                LabelFigure1 = 'Produccion (MB)'
                LabelFigure2 = 'Produccion (MMPC)'                
                if self.Seleccion_Oil.get() == True:
                    Columns1 = Columns1 + ['Acum_Petróleo_(Mb)', 'Acum_Condensado_(Mb)']
                if self.Seleccion_Water.get() == True:
                    Columns1.append('Acum_Agua_(Mb)')
                if self.Seleccion_Gas.get() == True:                
                    Columns2 = Columns2 +  ['Acum_Gas_asociado_(MMpc)', 'Acum_Gas_no_asociado_(MMpc)']               

            if self.Sel_RXY.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = ['RAA', 'RGA']
                Columns5 = []                

            if self.Sel_Chan.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = []
                Columns5 = ['RAA_Acum', "RAA'"]

            if self.Sel_FW.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = []
                Columns5 = []
                Columns6 = []
                Columns7 = ["FW(%)"]                

            self.PozosOpe.grid_forget()
            self.check_Res.grid_forget()
            self.check_Res2.grid_forget()
            self.check_Res3.grid_forget()            

            self.a.clear()
            self.b.clear()

            if len(Columns1) > 0:
                if len(Columns1) == 3:
                    for col, color in zip(Columns1, ['saddlebrown', 'indigo', 'deepskyblue']):
                        self.PozosInteres.plot(x='Fecha', y=col, color=color, label=col, linestyle='dashed', marker="8", ax=self.a )
                elif len(Columns1) == 2:
                    for col, color in zip(Columns1, ['saddlebrown', 'indigo']):
                        self.PozosInteres.plot(x='Fecha', y=col, color=color, label=col, linestyle='dashed', marker="8", ax=self.a )
                else:
                    for col, color in zip(Columns1, ['deepskyblue']):
                        self.PozosInteres.plot(x='Fecha', y=col, color=color, label=col, linestyle='dashed', marker="8", ax=self.a )                    
                self.a.set_title(pozos[0])
                self.a.set_ylabel(LabelFigure1, fontsize=labelssize)            
                max1 = self.PozosInteres[Columns1].max().values.max()+.1
                self.a.set_ylim([0, max1])
            if len(Columns2) > 0:
                for col, color in zip(Columns2, ['darkorange', 'orangered']):
                    self.b = self.PozosInteres.plot(x='Fecha', y=col, color=color, label=col, linestyle='dashed', marker="^", ax=self.a, secondary_y=True)
                self.b.set_ylabel(LabelFigure2, fontsize=labelssize)      
                max2 = self.PozosInteres[Columns2].max().values.max()+.1
                self.b.set_ylim([0, max2])
            if (len(Columns1) > 0) or (len(Columns2) > 0):
                self.a.tick_params(axis='x', rotation=45)
                self.a.grid(True)
                self.b.grid(True)
                self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)

            if len(Columns4) > 0:
                self.a.clear()
                self.b.clear()

                self.PozosInteres[Columns4[0]].plot(color=['darkgreen'], linestyle='dashed', marker='x', ax=self.a)
                self.a.set_title(pozos[0])
                self.a.set_ylabel('RAA (m3/m3)', fontsize=labelssize)     
                max1 = self.PozosInteres[Columns4[0]].max() +.1
                self.a.set_ylim([0, max1])
                self.b = self.PozosInteres[Columns4[1]].plot(color=['firebrick'], linestyle='dashed', marker='^',ax=self.a,secondary_y=True)
                self.b.set_ylabel('RGA (ft3/B)', fontsize=labelssize)
                max2 = self.PozosInteres[Columns4[1]].max() +.1                
                self.b.set_ylim([0, max2])
                self.a.set_xticks(np.floor(np.linspace(0, self.PozosInteres.shape[0]-1, 20)))
                self.a.set_xticklabels(self.PozosInteres.Fecha.iloc[np.floor(np.linspace(0, self.PozosInteres.shape[0]-1, 20))],rotation=rota)                       
                self.a.grid(True)
                self.b.grid(True, linestyle='--')
                self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)               

            if len(Columns5) > 0:
                self.a.clear()
                self.b.clear()
                
                self.PozosInteres.plot(x="Dias_Acum", y=Columns5, color=['deepskyblue', 'firebrick'], linestyle=' ', marker='o', ax=self.a)
                self.a.set_yscale('log')
                self.a.set_title(pozos[0])
                self.a.set_xlabel('Dias', fontsize=labelssize)
                self.b.get_yaxis().set_visible(False)
                self.a.set_xscale('log')
                self.a.grid(True, which='both')
                self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)

            if len(Columns7) > 0:
                self.a.clear()
                self.b.clear()

                indexs = []
                if (len(self.PozosInteres[self.PozosInteres['FW(%)'] > 0].index.tolist()) > 0):
                    indexs.append(self.PozosInteres[self.PozosInteres['FW(%)'] >= 0].index.tolist()[0])

                if len(indexs) > 0:
                    indexs = range(list(set(indexs))[0],self.PozosInteres.shape[0])
                    self.PozosInteres.plot(x="Fecha", y=Columns7, color=['blue'], linestyle='dashed', marker='H', ax=self.a)
                    self.a.set_title(pozos[0])
                    self.a.set_ylabel('FW (%)', fontsize=labelssize)
                    self.a.set_xlabel('', fontsize=labelssize)    
                    max1 = self.PozosInteres[Columns7[0]].max() +5 
                    self.a.set_ylim([0, max1])                    
                    self.a.set_xticks(np.floor(np.linspace(indexs[0], self.PozosInteres.shape[0]-1, 20)))
                    self.a.set_xticklabels(self.PozosInteres.Fecha.iloc[np.floor(np.linspace(indexs[0], self.PozosInteres.shape[0]-1, 20))],rotation=rota)   
                    self.b.get_yaxis().set_visible(False)
                    self.a.grid(True, which='both')
                    self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)
                else:
                    df = pd.DataFrame(np.random.random(10)*.000001)
                    self.a =  df.plot(ax=self.a)
                    self.a.set_ylim([0, 1])                 
                
            if self.Sel_Acum.get() == False:                  
                self.a.legend(loc='upper left',framealpha=.5)
                self.b.legend(loc='upper right',framealpha=.5)
            else:
                self.a.legend(loc='upper left',framealpha=.5)
                self.b.legend(loc='upper center',framealpha=.5)             
            
        if self.Seleccion_Field.get() == True:

            #Creating the data to plot
            self.CamposInteres = self.Campos[self.Campos['CAMPO_SIH'] == str(self.name)]
            self.PozosNumInteres = self.PozosNum[self.PozosNum['CAMPO'] == str(self.name)]
            self.ReservasInteres = self.Reservas[self.Reservas['CAMPO_SIH'] == str(self.name)]
            self.ReservasInteres = self.ReservasInteres.reset_index(drop=True)
            campos = self.CamposInteres.CAMPO_SIH.unique().tolist()
            self.CamposInteres = self.CamposInteres.reset_index(drop=True)
            self.sheetname = str(self.name)
            self.PozosOpe.grid(row=13, column=1, sticky ="W")
            self.check_Res.grid(row=9, column=1, sticky ="W")
            self.check_Res2.grid(row=9, column=3, sticky ="W")
            self.check_Res3.grid(row=9, column=5, sticky ="W")            
            fechas = []

            for fecha in self.PozosNumInteres.FECHA:
                fechas.append(pd.to_datetime(fecha[3:]).strftime('%m/%Y'))
            self.PozosNumInteres.loc[:, 'FECHA'] = fechas
            self.PozosNumInteres.index = self.PozosNumInteres.FECHA

            fechas = []
            dias = []

            for date in self.CamposInteres.FECHA:
                dias.append(pd.Period(pd.to_datetime(date).strftime('%m/%Y')).days_in_month)
                fechas.append(pd.to_datetime(date).strftime('%m/%Y'))
                
            self.CamposInteres['DIAS_MES'] = dias
            self.CamposInteres.FECHA = fechas
            self.CamposInteres["ACUM_PETROLEO_MB"] = self.CamposInteres.apply(lambda x: prodcols(x["PETROLEO_MBD"], x['DIAS_MES']), axis=1)
            self.CamposInteres["ACUM_PETROLEO_MB"] = self.CamposInteres["ACUM_PETROLEO_MB"].cumsum()
            self.CamposInteres["ACUM_CONDENSADO_MB"] = self.CamposInteres.apply(lambda x: prodcols(x["CONDENSADO_MBD"], x['DIAS_MES']), axis=1)
            self.CamposInteres["ACUM_CONDENSADO_MB"] = self.CamposInteres["ACUM_CONDENSADO_MB"].cumsum()
            self.CamposInteres["ACUM_AGUA_MB"] = self.CamposInteres.apply(lambda x: prodcols(x["AGUA_MBD"], x['DIAS_MES']), axis=1)
            self.CamposInteres["ACUM_AGUA_MB"] = self.CamposInteres["ACUM_AGUA_MB"].cumsum()
            self.CamposInteres["ACUM_GAS_ASOC_MMPC"] = self.CamposInteres.apply(lambda x: prodcols(x["GAS_ASOC_MMPCD"], x['DIAS_MES']), axis=1)
            self.CamposInteres["ACUM_GAS_ASOC_MMPC"] = self.CamposInteres["ACUM_GAS_ASOC_MMPC"].cumsum()
            self.CamposInteres["ACUM_GAS_NASOC_MMPC"] = self.CamposInteres.apply(lambda x: prodcols(x["GAS_NASOC_MMPCD"], x['DIAS_MES']), axis=1)
            self.CamposInteres["ACUM_GAS_NASOC_MMPC"] = self.CamposInteres["ACUM_GAS_NASOC_MMPC"].cumsum()    
            self.CamposInteres["ACUM_NITROGENO_MMPC"] = self.CamposInteres.apply(lambda x: prodcols(x["NITROGENO_MMPCD"], x['DIAS_MES']), axis=1)
            self.CamposInteres["ACUM_NITROGENO_MMPC"] = self.CamposInteres["ACUM_NITROGENO_MMPC"].cumsum()
            self.CamposInteres["FW(%)"] = self.CamposInteres.apply(lambda x: fw(x["PETROLEO_MBD"], x['AGUA_MBD']), axis=1)              

            self.CamposInteres.index = self.CamposInteres.FECHA
            columnas = ["FECHA","POZOS DE PETRÓLEO Y GAS ASOCIADO", "POZOS DE GAS NO ASOCIADO"]
            self.CamposInteres=pd.merge(self.CamposInteres,self.PozosNumInteres[columnas], how='left', left_index=True, right_index=True)
            self.CamposInteres = self.CamposInteres.reset_index(drop=True)
            self.CamposInteres.rename(columns={'FECHA_x':'FECHA'}, inplace=True)
            del self.CamposInteres['FECHA_y']

            RGAs = []
            RAAs = []
            RAAacum = []
            DiasAcum = []
            Der = []
            Dacum = 0
            RAAcum = 0

            for i, prod in enumerate(self.CamposInteres["PETROLEO_MBD"]):
                if prod > 0:
                    RGAs.append((self.CamposInteres["GAS_ASOC_MMPCD"].iloc[i]*1e6)/(prod*1e3))
                    RAAs.append((self.CamposInteres["AGUA_MBD"].iloc[i])/(prod))
                else:
                    RGAs.append(0)
                    RAAs.append(0)
                RAAcum += prod
                Dacum += dias[i]
                RAAacum.append(RAAcum)
                DiasAcum.append(Dacum)
                if i == 0:
                    Der.append(RAAcum/Dacum)
                else:
                    Der.append((RAAacum[i] - RAAacum[i-1])/float(Dacum))
                    
            self.CamposInteres["RGA"] = RGAs
            self.CamposInteres["RAA"] = RAAs
            self.CamposInteres["RAA_Acum"] = RAAacum
            self.CamposInteres["RAA'"] = Der
            self.CamposInteres["DIAS_Acum"] = DiasAcum     
 
            #Displaying the bottom to save the selected production data
            self.GuardarBot.pack(side = BOTTOM, fill = X )
            
            #Cleaning the figure axis to plot new production data
            self.a.clear()
            self.b.clear()
            Columns1 = []
            Columns2 = []
            Columns3 = []
            Columns4 = []
            Columns5 = []
            Columns6 = []
            Columns7 = []

            #Plotting selected production data
            if self.Sel_Acum.get() == False:
                LabelFigure1 = 'Produccion (MBD)'
                LabelFigure2 = 'Produccion (MMPCD)'
                if self.Seleccion_Oil.get() == True:
                    Columns1 = Columns1 + ['PETROLEO_MBD','CONDENSADO_MBD']
                if self.Seleccion_Water.get() == True:
                    Columns1.append('AGUA_MBD')
                if self.Seleccion_Gas.get() == True:                
                    Columns2 = Columns2 +  ['GAS_ASOC_MMPCD', 'GAS_NASOC_MMPCD', 'NITROGENO_MMPCD']
            else:
                LabelFigure1 = 'Produccion (MB)'
                LabelFigure2 = 'Produccion (MMPC)'
                if self.Seleccion_Oil.get() == True:
                    Columns1 = Columns1 + ['ACUM_PETROLEO_MB','ACUM_CONDENSADO_MB']
                if self.Seleccion_Water.get() == True:
                    Columns1.append('ACUM_AGUA_MB')
                if self.Seleccion_Gas.get() == True:                
                    Columns2 = Columns2 +  ['ACUM_GAS_ASOC_MMPC', 'ACUM_GAS_NASOC_MMPC', 'ACUM_NITROGENO_MMPC']


            if self.Sel_PozosOpe.get() == True:                
                Columns1 = []
                Columns2 = []
                if sum(self.CamposInteres[self.CamposInteres.columns[-2:]].sum()) == 0:
                    messagebox.showerror("Advertencia", "No se tiene informacion sobre pozos productores para el campo seleccionado.")
                    Columns3 = []
                    df = pd.DataFrame(np.random.random(10)*.000001)
                    self.a =  df.plot(ax=self.a)
                    self.a.set_ylim([0, 1])
                else:
                    Columns3 = ["POZOS DE PETRÓLEO Y GAS ASOCIADO", "POZOS DE GAS NO ASOCIADO"]

            if self.Sel_RXY.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = ['RAA', 'RGA']
                COlumns5 = []
                COlumns6 = []

            if self.Sel_FW.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = []
                Columns5 = []
                Columns6 = []
                Columns7 = ["FW(%)"]                         

            if self.Sel_Res.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = []
                Columns5 = []                

                self.ReservasInteres = self.ReservasInteres.iloc[self.ReservasInteres[self.ReservasInteres['PETROLEO_MMB'] > 0].index.tolist()]
                self.ReservasInteres = self.ReservasInteres.reset_index(drop=True)
                
                tipo1 = [] #2p
                tipo2 = [] #1p
                tipo3 = [] #3p pos
                fecha = []
                campo = []
                cuenca = []
                ubicacion = []

                df = pd.DataFrame()
                
                for i, fecha in enumerate(self.ReservasInteres['FECHA'].unique()):
                    if "PROBABLES" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo1.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'PROBABLES']['PETROLEO_MMB'].tolist()[0])
                    else:
                        tipo1.append(np.nan)
                       
                    if "PROBADAS" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo2.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'PROBADAS']['PETROLEO_MMB'].tolist()[0])
                    else:
                        tipo2.append(np.nan)
                    
                    if "POSIBLES" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo3.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'POSIBLES']['PETROLEO_MMB'].tolist()[0])
                    else:
                        tipo3.append(np.nan)

                df["Fecha"] = self.ReservasInteres.FECHA.unique().tolist()
                df["Campo"] = campos[0]
                df["Categoria"] = "Petroleo"
                df["PROBADAS_MMB"] = tipo2
                df["PROBABLES_MMB"] = tipo1
                df["POSIBLES_MMB"] = tipo3
                df["Total_MMB"] = df[["PROBABLES_MMB", "PROBADAS_MMB", "POSIBLES_MMB"]].sum(axis = 1)

                self.ReservasInteres = df;


                Columns6 = ["PROBADAS_MMB", "PROBABLES_MMB", "POSIBLES_MMB"]                
                        
            if self.Sel_Res2.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = []
                Columns5 = []                

                self.ReservasInteres = self.ReservasInteres.iloc[self.ReservasInteres[self.ReservasInteres['PETROLEO_CRUDO_EQUIVALENTE_MMBPCE'] > 0].index.tolist()]
                self.ReservasInteres = self.ReservasInteres.reset_index(drop=True)
                
                tipo1 = [] #2p
                tipo2 = [] #1p
                tipo3 = [] #3p pos
                fecha = []
                campo = []
                cuenca = []
                ubicacion = []

                df = pd.DataFrame()
                
                for i, fecha in enumerate(self.ReservasInteres['FECHA'].unique()):
                    if "PROBABLES" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo1.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'PROBABLES']['PETROLEO_CRUDO_EQUIVALENTE_MMBPCE'].tolist()[0])
                    else:
                        tipo1.append(np.nan)
                       
                    if "PROBADAS" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo2.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'PROBADAS']['PETROLEO_CRUDO_EQUIVALENTE_MMBPCE'].tolist()[0])
                    else:
                        tipo2.append(np.nan)
                    
                    if "POSIBLES" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo3.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'POSIBLES']['PETROLEO_CRUDO_EQUIVALENTE_MMBPCE'].tolist()[0])
                    else:
                        tipo3.append(np.nan)

                df["Fecha"] = self.ReservasInteres.FECHA.unique().tolist()
                df["Campo"] = campos[0]
                df["Categoria"] = "PCE"
                df["PROBADAS_MMBPCE"] = tipo2
                df["PROBABLES_MMBPCE"] = tipo1
                df["POSIBLES_MMBPCE"] = tipo3
                df["Total_MMBPCE"] = df[["PROBADAS_MMBPCE", "PROBABLES_MMBPCE", "POSIBLES_MMBPCE"]].sum(axis = 1)


                self.ReservasInteres = df;

                Columns6 = ["PROBADAS_MMBPCE", "PROBABLES_MMBPCE", "POSIBLES_MMBPCE"]                     

            if self.Sel_Res3.get() == True:
                Columns1 = []
                Columns2 = []
                Columns3 = []
                Columns4 = []
                Columns5 = []                

                self.ReservasInteres = self.ReservasInteres.iloc[self.ReservasInteres[self.ReservasInteres['GAS_MMMPC'] > 0].index.tolist()]
                self.ReservasInteres = self.ReservasInteres.reset_index(drop=True)
                
                tipo1 = [] #2p
                tipo2 = [] #1p
                tipo3 = [] #3p pos
                fecha = []
                campo = []
                cuenca = []
                ubicacion = []

                df = pd.DataFrame()
                
                for i, fecha in enumerate(self.ReservasInteres['FECHA'].unique()):
                    if "PROBABLES" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo1.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'PROBABLES']['GAS_MMMPC'].tolist()[0])
                    else:
                        tipo1.append(np.nan)
                       
                    if "PROBADAS" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo2.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'PROBADAS']['GAS_MMMPC'].tolist()[0])
                    else:
                        tipo2.append(np.nan)
                    
                    if "POSIBLES" in self.ReservasInteres[self.ReservasInteres.FECHA == fecha]['CATEGORIA'].tolist():
                        tipo3.append(self.ReservasInteres[self.ReservasInteres.FECHA == fecha][self.ReservasInteres.CATEGORIA == 'POSIBLES']['GAS_MMMPC'].tolist()[0])
                    else:
                        tipo3.append(np.nan)

                df["Fecha"] = self.ReservasInteres.FECHA.unique().tolist()
                df["Campo"] = campos[0]
                df["Categoria"] = "Gas"
                df["PROBADAS_MMMPC"] = tipo2
                df["PROBABLES_MMMPC"] = tipo1
                df["POSIBLES_MMMPC"] = tipo3
                df["Total_MMMPC"] = df[["PROBADAS_MMMPC", "PROBABLES_MMMPC", "POSIBLES_MMMPC"]].sum(axis = 1)

                self.ReservasInteres = df;

                Columns6 = ["PROBADAS_MMMPC", "PROBABLES_MMMPC", "POSIBLES_MMMPC"]          

            self.check_Chan.grid_forget()

            if len(Columns1) > 0:
                if len(Columns1) == 3:
                    self.CamposInteres[Columns1].plot(color=['saddlebrown', 'indigo', 'deepskyblue'], linestyle='dashed', marker="8", ax=self.a, label="Oil MBD")
                elif len(Columns1) == 2:
                    self.CamposInteres[Columns1].plot(color=['saddlebrown', 'indigo'], linestyle='dashed', marker='8', ax=self.a)
                else:
                    self.CamposInteres[Columns1].plot(color=['deepskyblue'], linestyle='dashed', marker="8", ax=self.a)
                self.a.set_title(campos[0])
                self.a.set_ylabel(LabelFigure1, fontsize=labelssize)            
                max1 = self.CamposInteres[Columns1].max().values.max()+.1
                self.a.set_ylim([0, max1])
            if len(Columns2) > 0:                
                self.b = self.CamposInteres[Columns2].plot(color=['darkorange', 'orangered', 'hotpink'], linestyle='dashed', marker='^',ax=self.a,secondary_y=True)
                self.b.set_ylabel(LabelFigure2, fontsize=labelssize)      
                max2 = self.CamposInteres[Columns2].max().values.max()+.1
                self.b.set_ylim([0, max2])
            if (len(Columns1)) > 0 or (len(Columns2) > 0):
                self.a.set_xticks(np.floor(np.linspace(0, self.CamposInteres.shape[0]-1, 20)))
                self.a.set_xticklabels(self.CamposInteres.FECHA.iloc[np.floor(np.linspace(0, self.CamposInteres.shape[0]-1, 20))],rotation=rota)                       
                self.a.grid(True)
                self.b.grid(True, linestyle='--')
                self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)

            if len(Columns3) > 0:
                self.a.clear()
                self.b.clear()

                self.CamposInteres[Columns3].plot(color=['red', 'blue'], linestyle='dashed', marker='8', ax=self.a)
                self.a.set_title(campos[0])
                self.a.set_ylabel('Num. de Pozos Produciendo', fontsize=labelssize)            
                max1 = self.CamposInteres[Columns3].max().values.max()+.1
                self.a.set_ylim([0, max1])
                self.b.set_ylim([0, max1])
                self.a.set_xticks(np.floor(np.linspace(0, self.CamposInteres.shape[0]-1, 20)))
                self.a.set_xticklabels(self.CamposInteres.FECHA.iloc[np.floor(np.linspace(0, self.CamposInteres.shape[0]-1, 20))],rotation=rota)                       
                self.a.grid(True)

            if len(Columns4) > 0:
                self.a.clear()
                self.b.clear()        

                self.CamposInteres[Columns4[0]].plot(color=['darkgreen'], linestyle='dashed', marker='x', ax=self.a)
                self.a.set_title(campos[0])
                self.a.set_ylabel('RAA (m3/m3)', fontsize=labelssize)     
                max1 = self.CamposInteres[Columns4[0]].max() +.1
                self.a.set_ylim([0, max1])
                self.b = self.CamposInteres[Columns4[1]].plot(color=['firebrick'], linestyle='dashed', marker='^',ax=self.a,secondary_y=True)
                self.b.set_ylabel('RGA (ft3/B)', fontsize=labelssize)
                max2 = self.CamposInteres[Columns4[1]].max() +.1                
                self.b.set_ylim([0, max2])
                self.a.set_xticks(np.floor(np.linspace(0, self.CamposInteres.shape[0]-1, 20)))
                self.a.set_xticklabels(self.CamposInteres.FECHA.iloc[np.floor(np.linspace(0, self.CamposInteres.shape[0]-1, 20))],rotation=rota)                       
                self.a.grid(True)
                self.b.grid(True, linestyle='--')
                self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)         

            if len(Columns5) > 0:
                self.a.clear()
                self.b.clear()
                
                self.CamposInteres.plot(x="DIAS_Acum", y=Columns5, color=['deepskyblue', 'firebrick'], linestyle=' ', marker='o', ax=self.a)
                self.a.set_yscale('log')
                self.a.set_title(campos[0])
                self.a.set_xlabel('Dias', fontsize=labelssize)
                self.b.get_yaxis().set_visible(False)
                self.a.grid(True, which='both')
                self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)

            if len(Columns6) > 0:
                self.a.clear()
                self.b.clear()

                if self.Sel_Res.get() == True:
                    label = 'Total_MMB'
                    etiqueta = 'MMB'
                elif self.Sel_Res2.get() == True:
                    label = 'Total_MMBPCE'
                    etiqueta = 'MMBPCE'
                elif self.Sel_Res3.get() == True:
                    label = 'Total_MMMPC'
                    etiqueta = 'MMMPC'

                if self.ReservasInteres[label].max() > 0:
                    self.ReservasInteres.plot(x="Fecha", y=Columns6, color=['royalblue', 'darkorange', 'deepskyblue',   ], kind='bar', stacked=True, ax=self.a)
                    self.a.set_title(campos[0])
                    self.a.set_ylabel(etiqueta, fontsize=labelssize)
                    self.a.set_xlabel('', fontsize=labelssize)
                    max1 = self.ReservasInteres[label].max()
                    if max1 <=1:
                        max1 = max1 + .05
                    elif max1 <= 20:
                        max1 = max1 + 1;
                    elif max1 <= 99:
                        max1 += 5
                    else:
                        max1 += 10
                    self.a.set_ylim([0, max1])
                    self.b.get_yaxis().set_visible(False)
                    self.a.grid(True, linestyle='--')
                    self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)                       
                else:
                    fig= plt.figure()

            if len(Columns7) > 0:
                self.a.clear()
                self.b.clear()

                indexs = []
                if (len(self.CamposInteres[self.CamposInteres['FW(%)'] > 0].index.tolist()) > 0):
                    indexs.append(self.CamposInteres[self.CamposInteres['FW(%)'] >= 0].index.tolist()[0])

                if len(indexs) > 0:
                    indexs = range(list(set(indexs))[0], self.CamposInteres.shape[0])
                    self.CamposInteres.plot(x="FECHA", y=Columns7, color=['blue'], linestyle='dashed', marker='H', ax=self.a)
                    self.a.set_title(campos[0])
                    self.a.set_ylabel('FW (%)', fontsize=labelssize)
                    self.a.set_xlabel('', fontsize=labelssize)    
                    max1 = self.CamposInteres[Columns7[0]].max() +5 
                    self.a.set_ylim([0, max1])                    
                    self.a.set_xticks(np.floor(np.linspace(indexs[0], self.CamposInteres.shape[0]-1, 20)))
                    self.a.set_xticklabels(self.CamposInteres.FECHA.iloc[np.floor(np.linspace(indexs[0], self.CamposInteres.shape[0]-1, 20))],rotation=rota)   
                    self.b.get_yaxis().set_visible(False)
                    self.a.grid(True, which='both')
                    self.fig.subplots_adjust(hspace=0.5, bottom = 0.15)
                else:
                    df = pd.DataFrame(np.random.random(10)*.000001)
                    self.a =  df.plot(ax=self.a)
                    self.a.set_ylim([0, 1])                    
                
            if self.Sel_PozosOpe.get() == True:
                self.a.legend(loc='upper left',framealpha=.5)
            elif self.Sel_Res.get() == True or self.Sel_Res2.get() == True or self.Sel_Res3.get() == True:
                self.a.legend(framealpha=.5)                
            else:
                if self.Sel_Acum.get() == False:                
                    self.a.legend(loc='upper left',framealpha=.5)
                    self.b.legend(loc='upper right',framealpha=.5)
                else:
                    self.a.legend(loc='upper left',framealpha=.5)
                    self.b.legend(loc='upper center',framealpha=.5)                
            
        #Displaying the plotted secleted data
        self.canvas.get_tk_widget().pack(side = RIGHT, fill = Y )
        self.canvas.draw()

    #**********************************************************************************************************************
        
    def PrintingResults(self, font1, h, w):

        '''
        Function display the search results

        inputs:
        font1 -> Font size and style to display the search results
        h -> Height of the window resolution
        w -> Width of the window resolution

        '''

        #Creating scrollbars to navigate through the search results
        scrollbar = Scrollbar(self.ResultadosTab, width=20)
        scrollbar.pack( side = RIGHT, fill = Y )
        self.Resultados = Listbox(self.ResultadosTab, font=font1, selectbackground="#008000", highlightcolor="#001a00", height=int(h/2)+10)

        #Creaating search results
        found_files = self.FoundResults
        found_files.sort()
        for a_file in found_files:
            self.Resultados.insert(0, a_file)

        #Displaying the search results and the created scrollbar      
        self.Resultados.pack(fill=BOTH, expand=YES)
        scrollbar.config( command = self.Resultados.yview )

        #Internal function
        def onselect(event):

            '''
            Function to plot production data based on the selected serach results

            inputs:
            event -> Event binded to the search results
            '''
            Resultados = event.widget
            if len(Resultados.curselection()) > 0:
                index = int(Resultados.curselection()[0])
                self.name = Resultados.get(index)
                self.TextoBusqueda.delete(0,END)
                self.TextoBusqueda.insert(0,self.name)            
                
                #self.TextoBusqueda.insert(0,value)
                self.plotting_wells()

            if self.Seleccion_Field.get() == True:

                #self.TextoBusqueda.insert(0,value)
                self.plotting_wells()         

        #Binding the action of selected a search results item with the plotting of production data
        self.Resultados.bind('<<ListboxSelect>>', onselect)


    #**********************************************************************************************************************
        
    def get(self, event):

        '''
        Function implement the desired search when the <return> key is pressed

        input:
        event -> Waiting for the event of pressing the <return> key

        '''

        #Word to search
        self.SearchWord = event.widget
        #Implementing the search
        self.GetResults()

    #**********************************************************************************************************************

    def SaveResults(self):
        '''
        Function to save the selected production data
        '''

        # Calling the file manager to select the name and location of the file to save
        file_name = asksaveasfilename(defaultextension='.xlsx')
        
        # Saving the data from pandas to excel
        if file_name:
            writer = ExcelWriter(file_name)
            
            if self.Seleccion_Field.get() == True:
                if self.Sel_Res.get() == True or self.Sel_Res2.get() == True or self.Sel_Res3.get() == True:
                    self.ReservasInteres.to_excel(writer, self.sheetname, index=False)
                else:
                    self.CamposInteres.to_excel(writer, self.sheetname, index=False)
            else:
                self.PozosInteres.to_excel(writer, self.sheetname, index=False)

            writer.close()  # <-- usar close() en lugar de save()

           


'''*****************************************************************************************************************
Main
*****************************************************************************************************************'''

#Main

if __name__ == "__main__":

    #Creating an object based on the MexicanaGUI class
    app = MexicanaGUI()
    #Creating the GUI
    app.mainloop()

'''*****************************************************************************************************************
Fin
*****************************************************************************************************************'''
