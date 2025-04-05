import tkinter as tk
import os
import subprocess

window = tk.Tk()

window.title('AI Chat App')
Users = tk.Text(window)
Users.pack()

Button_new_friend = tk.Button(window, text='New friend', command=lambda: subprocess.Popen('./ChatUI.py'))
Button_new_friend.pack()
window.mainloop()