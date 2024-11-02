import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def select_input_files():
    input_file_paths = filedialog.askopenfilenames(
        title="Select Files (.lst)", filetypes=[("List Files", "*.lst")]
    )
    if input_file_paths:
        update_file_selection(input_file_paths)
    else:
        reset_file_selection()


def update_file_selection(file_paths):
    files_list = "\n".join(file_paths)
    input_label.config(text=f"Selected files:\n{files_list}")
    convert_button.config(state="normal")
    convert_button.file_paths = file_paths


def reset_file_selection():
    input_label.config(text="No files selected")
    convert_button.config(state="disabled")


def convert_to_json():
    output_folder = filedialog.askdirectory(title="Select a folder to save JSON files")
    if not output_folder:
        return

    success_files = []

    for input_file_path in convert_button.file_paths:
        output_file_path = convert_file(input_file_path, output_folder)
        if output_file_path:
            success_files.append(output_file_path)

    finalize_conversion(success_files, output_folder)


def convert_file(input_file_path, output_folder):
    try:
        with open(input_file_path, "r") as input_file:
            data = [{"hostname": line.strip()} for line in input_file]

        output_file_name = (
            os.path.splitext(os.path.basename(input_file_path))[0] + ".json"
        )
        output_file_path = os.path.join(output_folder, output_file_name)

        with open(output_file_path, "w") as output_file:
            json.dump(data, output_file, indent=2)

        return output_file_path
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert {input_file_path}: {e}")
        return None


def finalize_conversion(success_files, output_folder):
    if success_files:
        messagebox.showinfo(
            "Success",
            "Conversion completed! Results saved in:\n" + "\n".join(success_files),
        )
        status_label.config(
            text="Success: Conversion completed!", style="Status.TLabel"
        )
        open_folder_button.config(
            state="normal", command=lambda: open_folder(output_folder)
        )
    else:
        status_label.config(text="Error during conversion.", style="Status.TLabel")


def open_folder(folder_path):
    os.startfile(folder_path)


root = tk.Tk()
root.title("LST to JSON Converter")
root.geometry("500x300")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

frame = ttk.Frame(root, padding="10")
frame.pack(pady=10)

select_button = ttk.Button(
    frame, text="Select Files (.lst)", command=select_input_files
)
select_button.grid(row=0, column=0, padx=5, pady=(0, 5))

input_label = ttk.Label(frame, text="No files selected", width=50, anchor="center")
input_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

convert_button = ttk.Button(
    root, text="Convert to JSON", command=convert_to_json, state="disabled"
)
convert_button.pack(pady=10)

status_label = ttk.Label(root, text="", style="Status.TLabel", background="#f0f0f0")
status_label.pack(pady=5)

open_folder_button = ttk.Button(
    root, text="Open Folder with Files", command=lambda: None, state="disabled"
)
open_folder_button.pack(pady=5)

style = ttk.Style()
style.configure("Status.TLabel", foreground="green", background="#f0f0f0")

root.mainloop()
