import os
import re


def find_markdown_files(root_dir):
    """Find all index.md files in the directory tree."""
    index_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "index.md":
                index_files.append(os.path.join(dirpath, filename))
    return index_files


def extract_grade_from_file(md_file):
    """Extract the grade from the given markdown file."""
    grade_pattern = re.compile(r"\*\*School's overall airborne virus protection grade \(0-5\)\*\*: (\d+)")
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            for line in f:
                match = grade_pattern.search(line)
                if match:
                    return match.group(1)
    except IsADirectoryError:
        return None
    return None


def process_index_file(index_file):
    """Process each index.md file to update lines with grades."""
    updated_lines = []
    pattern = re.compile(r"^(\s*-\s*\[.*?\]\((.*?)\))")
    with open(index_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                link_text = match.group(1)
                linked_file = match.group(2)
                linked_file_path = os.path.join(os.path.dirname(index_file), linked_file)
                if os.path.isfile(linked_file_path):
                    grade = extract_grade_from_file(linked_file_path)
                    if grade:
                        updated_line = f"{link_text} grade {grade}\n"
                        updated_lines.append(updated_line)
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

    with open(index_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)


def main(root_dir):
    """Main function to process all index.md files."""
    index_files = find_markdown_files(root_dir)
    for index_file in index_files:
        process_index_file(index_file)
    print("Processing complete.")


if __name__ == "__main__":
    root_directory = "./"  # Change this to the root directory where the markdown files are located
    main(root_directory)
