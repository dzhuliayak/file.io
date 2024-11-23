from tkinter import*
from tkinter import filedialog as fd
from tkinter import  messagebox as mb
from tkinter import ttk
import  requests
import pyperclip
import json
import os

from setuptools.command.build_ext import link_shared_object

history_file="upload_history.json"


def save_history(file_path, link):
    history=[]
    if os.path.exists(history_file): # проверяем существует ли файл
        with open(history_file, "r") as f:# открываем
            history=json.load(f)#загружаем
    history.append({"file_path": os.path.basename(file_path), "download_link": link})
    with open(history_file, "w") as f:
        json.dump(history,f,indent=4)


def upload():
    try:
        filepath=fd.askopenfilename() # путь к файлу
        if filepath:
            with open(filepath, "rb") as f:
                files={"file": f}
                response=requests.post("https://file.io", files=files)
                response.raise_for_status()# для проверки ошибок
                link=response.json()["link"]
                entry.delete(0, END)
                entry.insert(0, link)
                pyperclip.copy(link)
                save_history(filepath, link)
                mb.showinfo("ссыдка скопирована", f"ссылка {link} успешно скопирована в буфер обмена")
    except Exception as e:
        mb.showerror("ошибка", f"произошла ошибка:{e}")


def show_history():
    if not os.path.exists(history_file):
        mb.showinfo("история","история загрузок пуста")
        return

    history_window=Toplevel(window)
    history_window.title("история загружена")


    files_listbox=Listbox(history_window, width=50, height=20)
    files_listbox.grid(row=0, column=0, padx=(10,0), pady=10)

    links_listbox = Listbox(history_window, width=50, height=20)
    links_listbox.grid(row=0, column=1, padx=(0, 10), pady=10)

    with open(history_file, "r") as f:
        history=json.load(f)
        for item in history:
            files_listbox.insert(END, item["file_path"])
            links_listbox.insert(END, item["download_link"])


window=Tk()
window.title("сохранение файлов в облаке")
window.geometry("400x200")

button=ttk.Button(text="загрузить файл", command=upload)
button.pack()

entry=ttk.Entry()
entry.pack()

history_button=ttk.Button(text="показать историю", command=show_history)
history_button.pack()

window.mainloop()
