import os
import tkinter as tk
from tkinter import filedialog
import csv
import time

def select_directory():
    """Open a dialog to select a directory and return the selected path."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()

def get_text_files(directory):
    """List all text files in the given directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        list: A list of filenames (str) that end with '.txt'.
    """
    return [file for file in os.listdir(directory) if file.endswith(('.txt', '.csv'))]

def split_list(data, chunk_size):
    """Split a list into smaller lists of a specified size.

    Args:
        data (list): The original list.
        chunk_size (int): The size of each chunk.

    Returns:
        list: A list of smaller lists.
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def save_chunks(directory, original_filename, chunks):
    """Save each chunk of data to a new file with a numbered suffix.

    Args:
        directory (str): Directory to save the files in.
        original_filename (str): Original filename to modify.
        chunks (list): List of smaller lists to save.

    Returns:
        None
    """
    name, extension = os.path.splitext(original_filename)
    extension = ".csv"
    if name .endswith(".csv"):
        extension = ""

    for i, chunk in enumerate(chunks):
        new_filename = f"{i + 1}_{name}{extension}"
        filepath = os.path.join(directory, new_filename)

        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(chunk)

def process_file(directory, filename):
    """Read and process a text file, converting it to a DataFrame.

    Args:
        directory (str): The directory containing the file.
        text_file (str): The filename to process.

    Returns:
        DataFrame: A pandas DataFrame containing the processed file data.
    """
    if filename.endswith(".txt"):
        data = []
        with open(os.path.join(directory, filename), 'r') as file:
            for line in file:
                processed_line = [item for sublist in
                                  [elem.split(',') for elem in
                                   line.strip().split('\t')] for
                                  item in sublist]
                data.append(processed_line)
            if len(data) > 256:
                print("Splitting", filename)
                chunks = split_list(data, 256)
                save_chunks(directory, filename, chunks)
    else:
        with open(os.path.join(directory, filename), mode='r', newline='',
              encoding='utf-8') as file:
            data = list(csv.reader(file))

            if len(data) > 256:
                print("Splitting", filename)
                chunks = split_list(data, 256)
                save_chunks(directory, filename, chunks)
    return

def main():
    directory = select_directory()
    filelist = get_text_files(directory)
    for filename in filelist:
        process_file(directory, filename)
    print("Finished splitting files")
    print("Closing automatically..")
    time.sleep(2)

if __name__ == "__main__":
    main()