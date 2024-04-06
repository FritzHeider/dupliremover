import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import datetime
import logging
import re

# Set up logging
logging.basicConfig(filename='duplicate_remover.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def remove_duplicates(input_file, output_file, encoding, regex_pattern):
    line_counts = {}
    output_lines = []
    progress_bar['maximum'] = 100

    try:
        with open(input_file, 'r', encoding=encoding) as file:
            lines = file.readlines()

        total_lines = len(lines)
        regex = re.compile(regex_pattern)
        for index, line in enumerate(lines):
            normalized_line = regex.sub('', line.strip().lower())
            if normalized_line in line_counts:
                line_counts[normalized_line] += 1
            else:
                line_counts[normalized_line] = 1
                output_lines.append(line)
            progress_bar['value'] = (index / total_lines) * 100
            root.update_idletasks()

        with open(output_file, 'w', encoding=encoding) as file:
            for line in output_lines:
                file.write(line)

        logging.info(f"Duplicates removed. Cleaned file saved as: {output_file}")

    except Exception as e:
        logging.error("Failed to process file due to: " + str(e))
        messagebox.showerror("Error", str(e))

def select_file():
    encoding = simpledialog.askstring("Input", "Enter the file encoding (default is utf-8):", initialvalue="utf-8")
    regex_pattern = simpledialog.askstring("Regular Expression", "Enter regex pattern to ignore in lines (default is empty):", initialvalue="")
    root.filename = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt")])
    if root.filename:
        custom_name = simpledialog.askstring("Output Filename", "Enter a custom name for the output file (leave blank for default):")
        if not custom_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_file_path = root.filename.replace('.txt', f'_cleaned_{timestamp}.txt')
        else:
            output_file_path = f"{custom_name}.txt"

        remove_duplicates(root.filename, output_file_path, encoding, regex_pattern)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Duplicate Line Remover")

    # Adding a progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length 400)
    progress_bar.pack(pady=20)

    tk.Button(root, text="Select File", command=select_file).pack(pady=20)
    root.mainloop()
