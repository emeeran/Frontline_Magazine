#!/usr/bin/env python3
"""
Frontline Magazine GUI
A simple tkinter-based graphical interface for the Frontline Magazine scraper
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import threading
import os
import sys
from pathlib import Path

class FrontlineMagazineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Frontline Magazine Article Scraper")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set up output directory
        self.output_dir = Path.home() / "FrontlineMagazine"
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up paths
        self.install_dir = Path("/usr/share/frontline-magazine")
        self.venv_python = self.install_dir / "venv" / "bin" / "python"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Frontline Magazine Article Scraper", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar(value=str(self.output_dir))
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=40)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_dir).grid(row=1, column=2, pady=5)
        
        # Action buttons frame
        action_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        action_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        action_frame.columnconfigure(0, weight=1)
        
        # Magazine titles button
        ttk.Button(action_frame, text="Extract Magazine Issue Titles", 
                  command=self.extract_titles, width=30).grid(row=0, column=0, pady=5)
        ttk.Label(action_frame, text="Generates HTML summary of current magazine issue", 
                 font=("Arial", 9), foreground="gray").grid(row=1, column=0, pady=(0, 10))
        
        # Article URL frame
        url_frame = ttk.Frame(action_frame)
        url_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="Article URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Article extraction buttons
        button_frame = ttk.Frame(action_frame)
        button_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(button_frame, text="Extract as Markdown", 
                  command=self.extract_markdown).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Extract as HTML", 
                  command=self.extract_html).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Extract as PDF", 
                  command=self.extract_pdf).grid(row=0, column=2, padx=5)
        
        # Output text area
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, width=70)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Initial log message
        self.log_message("Frontline Magazine GUI started successfully!")
        self.log_message(f"Output directory: {self.output_dir}")
        
    def browse_output_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir)
        if directory:
            self.output_var.set(directory)
            self.output_dir = Path(directory)
            
    def log_message(self, message):
        self.output_text.insert(tk.END, f"[{self.get_timestamp()}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def run_command(self, script_name, description, url=None):
        def worker():
            try:
                self.status_var.set(f"Running: {description}")
                self.progress.start()
                
                # Change to output directory
                original_dir = os.getcwd()
                os.chdir(self.output_dir)
                
                script_path = self.install_dir / script_name
                cmd = [str(self.venv_python), str(script_path)]
                
                self.log_message(f"Starting: {description}")
                
                if url:
                    # For scripts that need URL input, use subprocess with input
                    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate(input=url + "\n")
                else:
                    # For scripts that don't need input
                    process = subprocess.run(cmd, capture_output=True, text=True)
                    stdout, stderr = process.stdout, process.stderr
                
                # Restore original directory
                os.chdir(original_dir)
                
                if process.returncode == 0:
                    self.log_message(f"✓ {description} completed successfully!")
                    if stdout.strip():
                        self.log_message(f"Output: {stdout.strip()}")
                    
                    # Show success message with file location
                    messagebox.showinfo("Success", 
                                      f"{description} completed!\n\n"
                                      f"Files saved to:\n{self.output_dir}")
                else:
                    self.log_message(f"✗ {description} failed!")
                    if stderr.strip():
                        self.log_message(f"Error: {stderr.strip()}")
                    messagebox.showerror("Error", f"{description} failed!\n\n{stderr}")
                    
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            finally:
                self.progress.stop()
                self.status_var.set("Ready")
                
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
    def extract_titles(self):
        self.run_command("fetch_titles_html.py", "Extract Magazine Titles")
        
    def extract_markdown(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter an article URL first!")
            return
        if not url.startswith("http"):
            messagebox.showwarning("Warning", "Please enter a valid URL starting with http:// or https://")
            return
        self.run_command("fetch_article_md.py", "Extract Article as Markdown", url)
        
    def extract_html(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter an article URL first!")
            return
        if not url.startswith("http"):
            messagebox.showwarning("Warning", "Please enter a valid URL starting with http:// or https://")
            return
        self.run_command("fetch_article_html.py", "Extract Article as HTML", url)
        
    def extract_pdf(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter an article URL first!")
            return
        if not url.startswith("http"):
            messagebox.showwarning("Warning", "Please enter a valid URL starting with http:// or https://")
            return
        self.run_command("fetch_article_pdf.py", "Extract Article as PDF", url)

def main():
    # Check if running in installed environment
    install_dir = Path("/usr/share/frontline-magazine")
    if not install_dir.exists():
        messagebox.showerror("Error", 
                           "Frontline Magazine is not properly installed.\n"
                           "Please install the .deb package first.")
        sys.exit(1)
        
    root = tk.Tk()
    app = FrontlineMagazineGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI closed by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
