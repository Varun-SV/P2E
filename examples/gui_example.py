"""
Simple GUI example using tkinter.
This demonstrates building a windowed application with P2E.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class SimpleApp:
    """A simple GUI application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("P2E GUI Example")
        self.root.geometry("400x300")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Welcome to P2E!",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="This is a simple GUI built with P2E",
            font=("Arial", 10)
        )
        desc_label.pack(pady=5)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=20, fill=tk.X)
        
        ttk.Label(input_frame, text="Your name:").pack(side=tk.LEFT, padx=5)
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.name_var, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        # Button
        greet_btn = ttk.Button(
            main_frame,
            text="Greet Me!",
            command=self.show_greeting
        )
        greet_btn.pack(pady=10)
        
        # About button
        about_btn = ttk.Button(
            main_frame,
            text="About P2E",
            command=self.show_about
        )
        about_btn.pack(pady=5)
    
    def show_greeting(self):
        """Show a greeting message."""
        name = self.name_var.get().strip()
        if name:
            messagebox.showinfo("Greeting", f"Hello, {name}!\n\nBuilt with P2E ❤️")
        else:
            messagebox.showwarning("Warning", "Please enter your name!")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
P2E - Python to EXE Converter

A modern tool for building Python executables.

Repository:
https://github.com/Varun-SV/P2E

This GUI was built with P2E!
        """
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
