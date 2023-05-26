import os
import shutil
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox


mappings = {
    'Documents': ['pdf', 'doc', 'docx', 'txt', 'csv', 'xlsx', 'zip', 'rar'],
    'Pictures': ['png', 'jpg', 'jpeg', 'gif', 'psd', 'ico'],
    'Videos': ['mp4', 'avi', 'flv', 'wmv'],
    'Music': ['mp3', 'wav', 'ogg'],
}

move_history = []
selected_directory = None


def move_file_with_progress(src, dst, pbar):
    shutil.move(src, dst)
    pbar.update()


def organize_files():
    global selected_directory
    if selected_directory is None:
        return
    summary = {"Documents": False, "Pictures": False, "Videos": False, "Music": False}
    files_to_move = []

    for filename in os.listdir(selected_directory):
        file_path = os.path.join(selected_directory, filename)
        if os.path.isfile(file_path):
            extension = filename.split('.')[-1]
            for folder, extensions in mappings.items():
                if extension.lower() in extensions:
                    dest_folder = os.path.join(os.path.expanduser('~'), folder)

                    if not os.path.isdir(dest_folder):
                        os.makedirs(dest_folder)

                    new_path = os.path.join(dest_folder, filename)
                    move_history.append((new_path, file_path))
                    files_to_move.append((file_path, new_path))
                    summary[folder] = True
                    break

    progress = ttk.Progressbar(window, length=500, mode='determinate', maximum=len(files_to_move))
    progress.place(relx=0.5, rely=0.5, anchor="center")

    def threaded_file_move():
        for src, dst in files_to_move:
            shutil.move(src, dst)
            progress['value'] += 1
            window.update_idletasks()
        progress.destroy()

    Thread(target=threaded_file_move).start()

    summary_text = ""
    for folder, moved in summary.items():
        if moved:
            summary_text += f"The {folder.lower()} files are located in {os.path.join(os.path.expanduser('~'), folder)}\n"
    if summary_text:
        tk.messagebox.showinfo(title="File Organizer", message=summary_text)


def undo():
    summary = {"Documents": False, "Pictures": False, "Videos": False, "Music": False}
    while move_history:
        new_path, old_path = move_history.pop()

        if os.path.isfile(new_path):
            shutil.move(new_path, old_path)
            folder = old_path.split(os.path.sep)[-2]
            summary[folder] = True

    summary_text = ""
    for folder, moved in summary.items():
        if moved:
            summary_text += f"The {folder.lower()} files were moved back to the original location.\n"
    if summary_text:
        tk.messagebox.showinfo(title="File Organizer", message=summary_text)


def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory()
    selected_label['text'] = f"Selected Directory:\n{selected_directory}"


def create_gradient(width, height):
    base = Image.new('RGB', (width, height), '#2C3E50')
    top = Image.new('RGB', (width, height), '#4CA1AF')
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend(list(int(255 * (x / width)) for x in range(width)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


window = tk.Tk()
window.title("File Organizer | Created By: Siym")
window.geometry("700x700")

gradient = create_gradient(700, 700)
background_image = ImageTk.PhotoImage(gradient)

window.background_image = background_image
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

center_frame = tk.Frame(window, bg='#2d2d2a')
center_frame.place(relx=0.5, rely=0.4,
                   anchor="center")

title_label = tk.Label(window, text="File Organizer", fg="white", bg="#2d2d2a", font=("Arial", 24, "bold"))
title_label.place(relx=0.5, rely=0.1, anchor="center")

select_button = tk.Button(center_frame, text="Select Directory", command=select_directory, bg='#c0b7b1',
                          font=("Arial", 16))
select_button.grid(sticky='ew')

selected_label = tk.Label(center_frame, text="No directory selected", wraplength=600, font=("Arial", 16))
selected_label.grid(sticky='ew')

button_frame = tk.Frame(window)
button_frame.place(relx=0.5, rely=0.6,
                   anchor="center")

organize_button = tk.Button(button_frame, text="Organize", command=organize_files, font=("Arial", 9))
organize_button.grid(row=0, column=0, padx=(0, 51.5))

undo_button = tk.Button(button_frame, text="Undo", command=undo, font=("Arial", 9))
undo_button.grid(row=0, column=1, padx=(51.5, 0))

footer_frame = tk.Frame(window, bg='#2C3E50')
footer_frame.place(relx=0.5, rely=1, anchor="s")

footer_label_font = ('Arial', 10)
footer_label = tk.Label(footer_frame, text="© Khandakar Sayeem. All Rights Reserved. 2023", font=footer_label_font,
                        bg='#2C3E50', fg="white")
footer_label.pack(pady=10)

center_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

window.mainloop()
