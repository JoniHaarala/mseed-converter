# Copyright 2023 Jonatan Haarala. All Rights Reserved.
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from time import perf_counter, sleep
from numpy import amax
import threading

# personal package
from read_mseed import *


def openfile():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select x-axis file",
                                          filetypes=(("MSEED files", "*.ms;*.mseed;*.msd"),
                                                     ("Text files", "*.txt"),
                                                     ("all files", "*.*")))
    # Change label contents
    x.set(filename)
    print(x.get())


def browsexfiles():
    filename = filedialog.askopenfilename(initialdir="*/Documents",
                                          title="Select x-axis file",
                                          filetypes=(("MSEED files", "*.ms;*.mseed;*.msd"),
                                                     ("Text files", "*.txt"),
                                                     ("all files", "*.*")))
    # Change label contents
    x.set(filename)
    print(x.get())


def browseyfiles():
    filename = filedialog.askopenfilename(initialdir="*/Documents",
                                          title="Select y-axis file",
                                          filetypes=(("MSEED files", "*.ms;*.mseed;*.msd"),
                                                     ("Text files", "*.txt"),
                                                     ("all files", "*.*")))
    # Change label contents
    y.set(filename)
    print(y.get())


def browsezfiles():
    filename = filedialog.askopenfilename(initialdir="*/Documents",
                                          title="Select z-axis file",
                                          filetypes=(("MSEED files", "*.ms;*.mseed;*.msd"),
                                                     ("Text files", "*.txt"),
                                                     ("all files", "*.*")))

    # Change label contents
    z.set(filename)
    print(z.get())


def savefiles():
    mkdir = filedialog.askdirectory(title="Seleccionar ruta...", initialdir="/")
    if mkdir:  # user selected dir
        getdata = show_data(x.get(), y.get(), z.get())
        getheader = read_metadata(x.get(), 11100)
        create_file(getdata, getheader, x.get(), mkdir)
        messagebox.showinfo(title="save", message="File saved successfully")

    else:  # user cancel the file browser window
        print("No destination directory chosen")
    monitor.configure(text="File saved: " + mkdir)


def saveasfiles():
    fichero = filedialog.asksaveasfilename(title="Guardar un fichero",
                                           filetypes=[("txt file", ".txt")],
                                           defaultextension=".txt")
    if fichero:  # user selected file
        print(ask)
        getdata = show_data(x.get(), y.get(), z.get())
        getheader = read_metadata(x.get(), 11100)

        pathlen = len(fichero.split('/'))
        newpath = fichero.split('/')[:pathlen - 1]
        newname = ''
        for i in newpath:
            newname += i + '/'

        create_file(getdata, getheader, x.get(), newname)
        messagebox.showinfo(title="save", message="File saved successfully")
    else:  # user cancel the file browser window
        print("No destination directory chosen")
    monitor.configure(text="File saved: " + fichero)


def convertdata():
    ##
    # Elapsed time with theards: 0.0010978000 seconds.
    # Elapsed time without theards: 5.9615271000 seconds.
    ##
    startT = perf_counter()

    newdata = show_data(x.get(), y.get(), z.get())

    header = read_metadata(x.get(), 11100)
    for value in header:
        mylist.insert(END, f"{value}")

    gettotaldata = header[11].split(' ')[2]
    for i in range(int(gettotaldata) - 1):
        mylist.insert(END, newdata[i])
        # mylist2.insert(END, f'{thread1[i]}')
        # mylist3.insert(END, f'{thread2[i]}')
        # mylist4.insert(END, f'{thread3[i]}')

    print("Data converted successfully")

    endT = perf_counter()
    print("Elapsed time: %0.6f seconds." % (endT - startT))


def multi_plot():
    plot_seismograms(x.get(), y.get(), z.get())


if __name__ == '__main__':
    # esMax = 11100
    # read_mseed.create_file(x, y, z, header, ejex)

    # Create the root window
    root = Tk()
    # Set root title
    root.title('mseed2ascii converter v1.4')
    # Set root size
    root.geometry("600x800")
    root.resizable(0, 0)
    # Set root background color
    root.config(background="white")

    # Para las coordenadas EW
    x = StringVar()
    # Para las coordenadas NS
    y = StringVar()
    # Para las coordenadas Z
    z = StringVar()

    # Menu section config
    menubar = Menu(root)
    root.config(menu=menubar)

    # Sub menus config
    # filemenu
    filemenu = Menu(menubar, tearoff=0)
    # filemenu.add_command(label="Abrir", command=openfile)
    filemenu.add_command(label="Guardar", command=savefiles)
    filemenu.add_command(label="Guardar como...", command=saveasfiles)
    filemenu.add_command(label="Cerrar")
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)

    # Helpmenu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Ayuda")
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de...")

    menubar.add_cascade(label="Archivo", menu=filemenu)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)

    #
    # Main program setup
    #
    setupframe = Frame(root, padx=5, pady=10)
    setupframe.pack(fill="both")
    # Create a File Explorer label
    xaxisframe = Frame(setupframe)
    yaxisframe = Frame(setupframe)
    zaxisframe = Frame(setupframe)
    xaxisframe.pack()
    yaxisframe.pack()
    zaxisframe.pack()

    Label(xaxisframe, text="x-axis path:", fg="blue").grid(row=0, column=0)
    Entry(xaxisframe, justify="center", textvariable=x, width=50, state="disabled").grid(row=0, column=1)
    Button(xaxisframe, text="Buscar", command=browsexfiles).grid(row=0, column=2)

    Label(yaxisframe, text="y-axis path:", fg="blue").grid(row=1, column=0)
    Entry(yaxisframe, justify="center", textvariable=y, width=50, state="disabled").grid(row=1, column=1)
    Button(yaxisframe, text="Buscar", command=browseyfiles).grid(row=1, column=2)

    Label(zaxisframe, text="z-axis path:", fg="blue").grid(row=2, column=0)
    Entry(zaxisframe, justify="center", textvariable=z, width=50, state="disabled").grid(row=2, column=1)
    Button(zaxisframe, text="Buscar", command=browsezfiles).grid(row=2, column=2)

    Button(setupframe, text="convertir", command=convertdata, padx=5, pady=5).pack()

    # Tab menu section
    tabcontrol = ttk.Notebook(root)

    tab1 = Frame(tabcontrol)
    tab2 = Frame(tabcontrol)
    tab3 = Frame(tabcontrol)
    tab4 = Frame(tabcontrol)

    tabcontrol.add(tab1, text='geopy file')
    tabcontrol.add(tab2, text='plotting data')
    tabcontrol.add(tab3, text='Eje Y')
    tabcontrol.add(tab4, text='Eje Z')
    tabcontrol.pack(expand=1, fill="both")

    scroll1 = Scrollbar(tab1)
    scroll1.pack(side=RIGHT, fill=BOTH)
    mylist = Listbox(tab1, yscrollcommand=scroll1.set, height=100)
    mylist.pack(fill=BOTH, padx=10)
    scroll1.config(command=mylist.yview)

    Button(tab2, text="Plot all Channels", command=multi_plot).pack(fill=BOTH, padx=10, pady=4)
    Button(tab2, text="Buscar", command='').pack(fill=BOTH, padx=10, pady=4)
    Button(tab2, text="Buscar", command='').pack(fill=BOTH, padx=10, pady=4)

    monitor = Label(root, text='mseed2ascii converter v1.4', justify='left', padx=10, pady=5, background='white')
    monitor.pack(side="left")

    # Let the root wait for any events
    root.mainloop()
