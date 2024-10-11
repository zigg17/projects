import os
import shutil
import ffmpeg
from tkinter import filedialog

vid_input = filedialog.askdirectory(title="Select a Directory")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

main_folder_name = input("Enter the folder name: ")
subfolders = ["vid-folder", "out-folder"]

main_folder_path = os.path.join(desktop_path, main_folder_name)
os.makedirs(main_folder_path, exist_ok=True)

for subfolder in subfolders:
    subfolder_path = os.path.join(main_folder_path, subfolder)
    os.makedirs(subfolder_path, exist_ok=True)

def convert_mov_to_gif(filename):
    if filename.endswith(".mov") or filename.endswith(".mp4"):
        input_file_path = os.path.join(vid_input, filename)
        base_filename = os.path.splitext(filename)[0]
        output_file_path = os.path.join(os.path.join(main_folder_path, 'out-folder'), f"{base_filename}.gif")
        (
            ffmpeg
            .input(input_file_path)
            .output(output_file_path, vf="fps=8", preset="fast")
            .run()
        )

        print(f"Converted {input_file_path} to {output_file_path}")
        mov_folder_path = os.path.join(main_folder_path, 'vid-folder', filename)
        shutil.move(input_file_path, mov_folder_path)
        print(f"Moved {input_file_path} to {mov_folder_path}")

mov_files = [f for f in os.listdir(vid_input) if f.endswith(".mov") or f.endswith(".mp4")]

for filename in mov_files:
    convert_mov_to_gif(filename)

shutil.rmtree(vid_input)
print(f"Deleted the original mov input directory: {vid_input}")