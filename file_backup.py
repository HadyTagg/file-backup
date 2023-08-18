# LIBRARY IMPORTS
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import datetime
import shutil
import os


# GETS THE SOURCE FILE LOCATION
def browse_file():
    file_location = filedialog.askopenfilename()
    chosen_input_label.config(text=file_location, fg='red')


# GETS THE ARCHIVE DIRECTORY LOCATION
def browse_directory():
    dir_location = filedialog.askdirectory()
    chosen_directory_label.config(text=dir_location, fg='blue')


# STARTS THE BACKUP LOOP
def activate_button_press():
    take_backup()
    root.withdraw()
    messagebox.showinfo('Archiving...', 'File backup will run in the background until the server session terminates '
                                        'or you exit the software.')


# FUNCTION CALLED REPEATEDLY TO TAKE THE ACTUAL BACKUP. CONVERTS THE BACKUP TIME INTERVAL ENTERED FROM HOURS TO MS
def take_backup():
    backup_time_interval_in_milliseconds = backup_time_interval_scale.get() * 60 * 60 * 1000
    root.after(int(backup_time_interval_in_milliseconds), take_backup)

    source = chosen_input_label.cget('text')
    destination = chosen_directory_label.cget('text')
    file_name_and_extension = os.path.split(source)[1]
    shutil.copy(source, destination + '/' + datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ' ' +
                file_name_and_extension)


# CHECKS IF ACTIVATE BUTTON SHOULD BE ACTIVE OR DISABLED. CHECKS EVERY 0.25 SECONDS
def activate_button_checker():
    root.after(250, activate_button_checker)

    if chosen_input_label.cget('text') != '' and chosen_directory_label.cget('text') != '':
        activate_button.config(state=NORMAL, bg='light green')

    else:
        activate_button.config(state=DISABLED, bg='SystemButtonFace')


# MAIN WINDOW
root = Tk()
root.title('File Backup')
root.iconbitmap(r"icon.ico")

pad_y_default = 3

# MAIN WINDOW WIDGETS
input_label = Label(root, text='Select a File to Backup', fg='red')
input_label.pack(pady=pad_y_default)

input_browse_button = Button(root, text='Browse', command=browse_file, activebackground='light green', fg='red')
input_browse_button.pack(pady=pad_y_default)

chosen_input_label = Label(root, text='')
chosen_input_label.pack(pady=pad_y_default)

output_location_label = Label(root, text='Select an Archive Location', fg='blue')
output_location_label.pack(pady=pad_y_default)

archive_dir_button = Button(root, text='Browse', command=browse_directory, activebackground='light green', fg='blue')
archive_dir_button.pack(pady=pad_y_default)

chosen_directory_label = Label(root, text='')
chosen_directory_label.pack(pady=pad_y_default)

backup_time_interval_label = Label(root, text='Backup Every (Hours)')
backup_time_interval_label.pack()

backup_time_interval_scale = Scale(root, orient=HORIZONTAL, to=24, from_=0.5, length=250, width=15,
                                   activebackground='light green', troughcolor='White', sliderlength=30, resolution=0.5)
backup_time_interval_scale.pack(pady=pad_y_default)

activate_button = Button(root, text='Activate', command=activate_button_press)
activate_button.pack(pady=pad_y_default, side=BOTTOM)

activate_button_checker()

root.mainloop()
