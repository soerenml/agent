import os
import glob


def merge_markdown_files(
        directory: str,
        num_files: int,
        output_file: str):
    """
    Merges the content of the most recently modified markdown files in a directory into a single output file.

    Args:
        directory (str): The path to the directory containing markdown files.
        num_files (int): The number of most recent files to merge.
        output_file (str): The path to the output file where the merged content will be saved.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified directory does not exist.
        IOError: If there is an error reading from or writing to the files.

    Example:
        merge_markdown_files('/path/to/markdown/files', 5, '/path/to/output/merged.md')
    """

    files = glob.glob(os.path.join(directory, '*'))

    # Sort files by modification time in descending order
    files.sort(key=os.path.getmtime, reverse=True)

    # Return the top `num_files` recent files
    files = files[:num_files]

    # Open the files and merge their content
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in files:
            with open(file, 'r', encoding='utf-8') as infile:
                # Read content of each file
                content = infile.read()
                # Write content to the output file
                outfile.write(content)
                # Add a separator (optional, for readability)
                outfile.write("\n\n---\n\n")  # Markdown-style horizontal rule