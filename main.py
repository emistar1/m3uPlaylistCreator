import tkinter as tk
from tkinter import filedialog, messagebox
import os

tk_root = tk.Tk()
tk_root.title("M0 playlist generator")
tk_root.geometry("1200x500")

label = tk.Label(tk_root, text="Select files to add to the playlist:")
label.pack(pady=10)

# store the full paths here; the listbox will show basenames only
selected_paths = []

# Dropdown to choose playlist format
format_var = tk.StringVar(value="Normal M3U file")
format_frame = tk.Frame(tk_root)
format_frame.pack(pady=5)
format_label = tk.Label(format_frame, text="Playlist format:")
format_label.pack(side=tk.LEFT, padx=(0, 8))
format_menu = tk.OptionMenu(format_frame, format_var, "Normal M3U file", "M0 M3U file")
format_menu.pack(side=tk.LEFT)

def open_file_explorer():
	# Restrict to standard music types: mp3 and flac
	file_paths = filedialog.askopenfilenames(
		title="Select music files",
		filetypes=(
			("FLAC files", "*.flac"),
			("MP3 files", "*.mp3"),
		),
	)
	if not file_paths:
		return

	# Filter to only .mp3 and .flac (case-insensitive)
	allowed_exts = {".mp3", ".flac"}
	filtered = [p for p in file_paths if os.path.splitext(p)[1].lower() in allowed_exts]
	skipped = [p for p in file_paths if p not in filtered]

	if skipped:
		messagebox.showwarning("Skipped files", "Some selected files were ignored (only .mp3 and .flac are allowed).")

	# keep full paths in `selected_paths` but show basenames in the listbox
	global selected_paths
	if filtered:
		selected_paths = filtered
		listbox.delete(0, tk.END)
		for path in filtered:
			listbox.insert(tk.END, os.path.basename(path))
	else:
		selected_paths = []
		listbox.delete(0, tk.END)

open_button = tk.Button(tk_root, text="Open File Explorer", command=open_file_explorer)
open_button.pack(pady=5)

frame = tk.Frame(tk_root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=120, height=10)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

def get_selected_filenames():
	# return the stored full paths 
	return list(selected_paths)

def save_playlist():
	paths = get_selected_filenames()
	if not paths:
		messagebox.showinfo("No files", "No files selected to save.")
		return
	save_path = filedialog.asksaveasfilename(
		defaultextension=".m3u",
		filetypes=(("M3U playlist", "*.m3u"), ("All files", "*.*")),
		initialfile="playlist.m3u",
		title="Save playlist as",
	)
	if not save_path:
		return
	try:
		def to_m0_path(pth: str) -> str:
			# Use only the last folder and filename, prefix with A:/
			abs_p = os.path.abspath(pth)
			parent = os.path.basename(os.path.dirname(abs_p))
			fname = os.path.basename(abs_p)
			return f"A:/{parent}/{fname}"

		with open(save_path, "w", encoding="utf-8") as f:
			f.write("#EXTM3U\n")
			if format_var.get() == "M0 M3U file":
				for p in paths:
					f.write(to_m0_path(p) + "\n")
			else:
				for p in paths:
					f.write(p + "\n")
		messagebox.showinfo("Saved",f"Playlist saved to:\n{save_path}")
	except Exception as e:
		messagebox.showerror("Error",f" to save playlist:\n{e}")

save_button = tk.Button(tk_root, text="Save Playlist (.m3u)", command=save_playlist)
save_button.pack(pady=5)

tk_root.mainloop()