import os
import glob

def get_recent_files(directory: str, num_files: int):
    # Get a list of all files in the directory
    files = glob.glob(os.path.join(directory, '*'))

    print(files)

    # Sort files by modification time in descending order
    files.sort(key=os.path.getmtime, reverse=True)

    # Return the top `num_files` recent files
    return files[:num_files]

def merge_markdown_files(input_files, output_file):
    """
    Merge multiple Markdown files into one.

    :param input_files: List of file paths to the Markdown files to merge.
    :param output_file: Path to the output file.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in input_files:
            with open(file, 'r', encoding='utf-8') as infile:
                # Read content of each file
                content = infile.read()
                # Write content to the output file
                outfile.write(content)
                # Add a separator (optional, for readability)
                outfile.write("\n\n---\n\n")  # Markdown-style horizontal rule

input_files = get_recent_files(directory='reports', num_files=5)
merge_markdown_files(input_files=input_files, output_file='reports/merged_report.md')