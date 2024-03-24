import webbrowser
import time
import random
import tkinter as tk
from tkinter import filedialog
from ttkthemes import ThemedStyle

class SubdomainLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subdomain Loader")
        self.style = ThemedStyle(self.root)
        self.style.set_theme("black")  # Use the Equilux theme

        self.filename = tk.StringVar()

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # File Path Entry
        label_frame = tk.Frame(self.root, padx=10, pady=10)
        label_frame.pack(fill=tk.X)

        tk.Label(label_frame, text="Enter the file path:", font=("Helvetica", 12), padx=1, pady=1).pack(side=tk.LEFT)

        entry_frame = tk.Frame(self.root , padx=10, pady=10)
        entry_frame.pack(fill=tk.X)

        entry = tk.Entry(entry_frame, textvariable=self.filename, font=("Helvetica", 12), width=40)
        entry.pack(side=tk.LEFT, padx=(0, 10))

        browse_button = tk.Button(entry_frame, text="Browse", command=self.browse_file, font=("Helvetica", 12))
        browse_button.pack(side=tk.RIGHT)

        # Load Button
        tk.Button(self.root, text="Load Subdomains", command=self.load_subdomains, font=("Helvetica", 12), padx=9, pady=10).pack(pady=10)

        # Output Text
        text_frame = tk.Frame(self.root, padx=9, pady=10)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(text_frame, height=7, width=50, font=("Helvetica", 12))
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.filename.set(file_path)

    def load_subdomains(self):
        filename = self.filename.get()
        try:
            with open(filename, 'r') as file:
                subdomains = [line.strip() for line in file]

            # Shuffle the subdomains to randomize groupings
            random.shuffle(subdomains)

            self.output_text.insert(tk.END, "Loading subdomains...\n")

            # Load subdomains
            self.load_subdomains_gui(subdomains)

        except FileNotFoundError:
            self.output_text.insert(tk.END, "File not found. Please enter a valid file path.\n")

    def load_subdomains_gui(self, subdomains, group_size=2):
        total_subdomains = len(subdomains)

        if total_subdomains <= 50:
            self.output_text.insert(tk.END, "Loading all subdomains...\n")
            self.root.update()

            for subdomain in subdomains:
                webbrowser.open_new_tab("http://" + subdomain)
                time.sleep(3)  # Adjust the delay as needed to avoid overloading the browser
        else:
            self.output_text.insert(tk.END, "Loading subdomains in groups of {}...\n".format(group_size))
            self.root.update()

            num_groups = total_subdomains // group_size + (1 if total_subdomains % group_size != 0 else 0)
            groups = [subdomains[i:i + group_size] for i in range(0, total_subdomains, group_size)]

            for i, group in enumerate(groups):
                self.output_text.insert(tk.END, "Loading group {}...\n".format(i + 1))
                self.root.update()

                for subdomain in group:
                    webbrowser.open_new_tab("http://" + subdomain)
                    time.sleep(1)  # Adjust the delay as needed to avoid overloading the browser

                if i < num_groups - 1:
                    permission = self.ask_user_continue()
                    if permission != 'yes':
                        self.output_text.insert(tk.END, "Loading stopped\n")
                        self.root.update()
                        break
            else:  # Executed when the loop completes without breaking
                # Message after completing all subdomains
                self.output_text.insert(tk.END, "All subdomains loaded successfully.\n")
                self.root.update()

    def ask_user_continue(self):
        self.continue_var = tk.StringVar()
        self.continue_var.set('')

        # Create a new top-level window for the Yes/No buttons
        continue_window = tk.Toplevel(self.root)
        continue_window.transient(self.root)  # Set as transient to stay on top

        label = tk.Label(continue_window, text="Load next group?", font=("Helvetica", 12))
        label.pack()

        # Yes Button
        yes_button = tk.Button(continue_window, text="Yes", command=lambda: self.set_continue_var('yes'), font=("Helvetica", 12), padx=10, pady=5)
        yes_button.pack(side=tk.LEFT, padx=30, pady=10)

        # No Button
        no_button = tk.Button(continue_window, text="No", command=lambda: self.set_continue_var('no'), font=("Helvetica", 12), padx=10, pady=5)
        no_button.pack(side=tk.RIGHT, padx=30, pady=10)

        # Wait for user input
        self.root.wait_variable(self.continue_var)

        # Close the top-level window
        continue_window.destroy()

        return self.continue_var.get()

    def set_continue_var(self, value):
        self.continue_var.set(value)

    def pause_loading(self):
        self.output_text.insert(tk.END, "Loading paused.\n")
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = SubdomainLoaderApp(root)
    root.mainloop()
