import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

class CustomButton(tk.Button):
    def __init__(self, frame, text, command=None, *args, **kwargs):
        border_color = kwargs.pop('border_color', '#1a1919')
        border_width = kwargs.pop('border_width', 2)

        super().__init__(frame, text=text, borderwidth=border_width, relief='solid', bg='#1a1919',
                         highlightbackground=border_color, highlightthickness=border_width, *args, **kwargs)

        self.command = command
        self.config(command=self.on_click)

    def on_click(self):
        if self.command is not None:
            self.command()

def check_subdomain(subdomain, result_text):
    try:
        result_text.insert(tk.END, f"Checking subdomain: {subdomain}\n")
        result_text.see(tk.END)
        result_text.update_idletasks()
        subprocess.run(['curl', '--head', '--silent', '--output', '/dev/null', '--max-time', '5', f'http://{subdomain}'], check=True)
        result_text.insert(tk.END, f"Subdomain {subdomain} is reachable via HTTP.\n\n")
        result_text.see(tk.END)
        result_text.update_idletasks()
        return True
    except subprocess.CalledProcessError:
        result_text.insert(tk.END, f"Subdomain {subdomain} is not reachable via HTTP.\n\n")
        result_text.see(tk.END)
        result_text.update_idletasks()
        return False

def check_https_subdomain(subdomain, result_text):
    try:
        result_text.insert(tk.END, f"Checking subdomain: {subdomain}\n")
        result_text.see(tk.END)
        result_text.update_idletasks()
        subprocess.run(['curl', '--head', '--silent', '--output', '/dev/null', '--max-time', '5', f'https://{subdomain}'], check=True)
        result_text.insert(tk.END, f"Subdomain {subdomain} is reachable via HTTPS.\n\n")
        result_text.see(tk.END)
        result_text.update_idletasks()
        return True
    except subprocess.CalledProcessError:
        result_text.insert(tk.END, f"Subdomain {subdomain} is not reachable via HTTPS.\n\n")
        result_text.see(tk.END)
        result_text.update_idletasks()
        return False

def save_alive_subdomains(subdomains, output_file):
    with open(output_file, 'w') as file:
        for subdomain in subdomains:
            file.write(subdomain + '\n')

def process_subdomains():
    subdomain_file = subdomain_entry.get()
    output_file = output_entry.get()

    reachable_subdomains = []
    not_reachable_subdomains = []

    with open(subdomain_file, 'r') as file:
        for line in file:
            subdomain = line.strip()
            if check_subdomain(subdomain, result_text) or check_https_subdomain(subdomain, result_text):
                reachable_subdomains.append(subdomain)
            else:
                not_reachable_subdomains.append(subdomain)

    reachables_label.config(text="SCAN COMPLETED")
    for subdomain in reachable_subdomains:
        result_text.insert(tk.END, subdomain + "\n")
        result_text.tag_configure("reachable", foreground="green")
        result_text.tag_add("reachable", "end - 1 line linestart", "end - 1 line lineend")

    save_option = messagebox.askyesno("Scan Completed", "Do you want to save alive subdomains to a file?")
    if save_option:
        save_alive_subdomains(reachable_subdomains, output_file)
        messagebox.showinfo("File Saved Successfully")

def change_color(widget):
    widget.config(bg="white", fg="#1a1919")

def browse_subdomain_file():
    filename = filedialog.askopenfilename()
    subdomain_entry.delete(0, tk.END)
    subdomain_entry.insert(0, filename)
    change_color(subdomain_entry)  # Change color of the entry widget

def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filename)
    change_color(output_entry)  # Change color of the entry widget

def start_processing():
    process_thread = threading.Thread(target=process_subdomains)
    process_thread.start()

root = tk.Tk()
root.title("SUBSTS")
root.config(bg="#1f1f1f")

# Change font to bold
font_bold = ('Helvetica', 12, 'bold')

frame = tk.Frame(root, bg="#1a1919")
frame.pack(padx=1, pady=1)

subdomain_label = tk.Label(frame, text="Subdomain File:", font=font_bold, fg="#c9cbd6", bg="#1a1919")
subdomain_label.grid(row=0, column=0, padx=10,sticky="w")

subdomain_entry = tk.Entry(frame, width=30, relief='solid', borderwidth=1, bg="#ffffff")
subdomain_entry.grid(row=0, column=1,  padx=8, pady=8)

subdomain_button = tk.Button(frame, text="Browse", font=font_bold,fg="#000000",bg="#c9cbd6" ,command=browse_subdomain_file)
subdomain_button.grid(row=0, column=2, padx=0, pady=8)

output_label = tk.Label(frame, text="Output File:", font=font_bold, fg="#c9cbd6", bg="#1a1919")
output_label.grid(row=1, column=0,padx=10, sticky="w")

output_entry = tk.Entry(frame, width=30, relief='solid', borderwidth=1,bg="#ffffff")
output_entry.grid(row=1, column=1, padx=8, pady=8)

output_button = tk.Button(frame, text="Browse", font=font_bold, command=browse_output_file ,fg="#000000", bg="#c9cbd6" , borderwidth=1 , highlightthickness = 1 )
output_button.grid(row=1, column=2, padx=8, pady=8)

process_button = tk.Button(frame, text="Process Subdomains", font=font_bold ,fg="#000000", bg="#c9cbd6" ,borderwidth=1 , height=1 , command=start_processing)
process_button.grid(row=2, columnspan=3, pady=8)

result_frame = tk.Frame(root, bg="#1a1919" )
result_frame.pack(padx=8, pady=8)

reachables_label = tk.Label(result_frame, text="REAL TIME PANNEL", font=font_bold, bg="#1a1919",fg="#c9cbd6" ,highlightbackground="#16c946")
reachables_label.pack(padx=8, pady=8)

result_text = tk.Text(result_frame, bg="white", height=19, width=67)
result_text.pack()

root.mainloop()
