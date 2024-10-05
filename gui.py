import tkinter as tk
from tkinter import scrolledtext

class ChatApplication:
    def _init_(self, root):
        self.root = root
        self.root.title("Chat Application")
        
        # Create chat window
        self.chat_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chat_window.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.chat_window.config(state=tk.DISABLED)
        
        # Create message entry box
        self.message_var = tk.StringVar()
        self.message_entry = tk.Entry(self.root, textvariable=self.message_var)
        self.message_entry.pack(padx=20, pady=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)
        
        # Create send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=20, pady=10)
        
    def send_message(self, event=None):
        message = self.message_var.get()
        if message:
            self.display_message("You", message)
            self.message_var.set("")
    
    def display_message(self, sender, message):
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"{sender}: {message}\n")
        self.chat_window.yview(tk.END)
        self.chat_window.config(state=tk.DISABLED)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication()
    root.geometry("400x500")
    root.mainloop()