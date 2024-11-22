from importlib.metadata import files
from tkinter import*
from tkinter import filedialog as fd
from tkinter import ttk
import  requests
from bottle import response


def upload():
    filepath=fd.askopenfilename() # путь к файлу
    if filepath:
        files={"file": open(filepath, "rb")}
        response=requests.post("https://www.file.io/", files=files)
        if response.status_code==200:
            link=response.json()["link"]
            entry.insert(0, link)


window=Tk()
window.title("сохранение файлов в облаке")
window.geometry("400x200")

button=ttk.Button(text="загрузить файл", command=upload)
button.pack()

entry=ttk.Entry()
entry.pack()

window.mainloop()




