from tkinter import*
from tkinter import filedialog as fd
from tkinter import  messagebox as mb
from tkinter import ttk
import  requests


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
    except Exception as e:
        mb.showerror("ошибка", f"произошла ошибка:{e}")

window=Tk()
window.title("сохранение файлов в облаке")
window.geometry("400x200")

button=ttk.Button(text="загрузить файл", command=upload)
button.pack()

entry=ttk.Entry()
entry.pack()

window.mainloop()




