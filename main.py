from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import speech_recognition as sr
import pyautogui
import pyttsx3


def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)


def openFile():
    global file
    file = askopenfilename(defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                      ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close()


def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                 filetypes=[("All Files", "*.*"),
                                            ("Text Documents", "*.txt")])
        if file == "":
            file = None

        else:
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - Notepad")
            print("File Saved")
    else:
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def quitApp():
    root.destroy()


def cut():
    TextArea.event_generate(("<<Cut>>"))


def copy():
    TextArea.event_generate(("<<Copy>>"))


def paste():
    TextArea.event_generate(("<<Paste>>"))


def sound():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')

        pyautogui.press('space', interval=0.2)
        pyautogui.typewrite(query)

        if "why" in query:
            pyautogui.typewrite('?')
        elif "how" in query:
            pyautogui.typewrite('?')
        else:
            pyautogui.typewrite('.')

    except Exception as e:
        print("Say that again please...")
        return "None"

    return query


def aloud():
    engine = pyttsx3.init()
    s = TextArea.get(1.0, END)
    engine.setProperty('rate', 150)
    engine.say(s)
    engine.runAndWait()


def about():
    showinfo("Notepad", "Notepad by Aayush")


if __name__ == '__main__':
    root = Tk()
    root.title("Untitled - Notepad")
    root.wm_iconbitmap("")
    root.geometry("644x788")

    TextArea = Text(root, font="Monaco 18")
    TextArea.config(background="coral")
    file = None
    TextArea.pack(expand=True, fill=BOTH)

    MenuBar = Menu(root)

    FileMenu = Menu(MenuBar, tearoff=0)

    FileMenu.add_command(label="New", command=newFile)

    FileMenu.add_command(label="Open", command=openFile)

    FileMenu.add_command(label="Save", command=saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=quitApp)
    MenuBar.add_cascade(label="File", menu=FileMenu)

    EditMenu = Menu(MenuBar, tearoff=0)

    EditMenu.add_command(label="Cut", command=cut)
    EditMenu.add_command(label="Copy", command=copy)
    EditMenu.add_command(label="Paste", command=paste)
    EditMenu.add_command(label="Mic", command=sound)
    EditMenu.add_command(label="Read", command=aloud)

    MenuBar.add_cascade(label="Edit", menu=EditMenu)

    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="About Notepad", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    root.config(menu=MenuBar)

    Scroll = Scrollbar(TextArea)
    Scroll.pack(side=RIGHT, fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

    root.mainloop()
