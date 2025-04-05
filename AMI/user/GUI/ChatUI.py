import tkinter as tk

window = tk.Tk()

window.title('AI Chat app')
# Create text area for displaying messages

chat_output = tk.Text(window)

chat_output.pack()
# Create an input field

user_input = tk.Entry(window)

user_input.pack()
# Create a send button

send_button = tk.Button(window, text='Send')

send_button.pack()


# Function to handle sending messages

def send_message():
    message = user_input.get()
    chat_output.insert(tk.END, f'You: {message}n')


user_input.delete(0, tk.END)
send_button.config(command=send_message)
# Start the GUI application

window.mainloop()
