import os
import json

def display_tree(directory, prefix="", file=None, depth=0, current_depth=0, exclude=None):
    try:
        # Stop if the current depth exceeds the maximum allowed depth
        if current_depth > depth:
            return

        # Write the folder name without a trailing slash
        file.write(prefix + os.path.basename(directory) + "\n")
        prefix += "    "

        # List the contents of the current directory
        for idx, item in enumerate(os.listdir(directory)):
            # Skip excluded folders/files
            if exclude and item in exclude:
                continue

            path = os.path.join(directory, item)
            is_last = idx == len(os.listdir(directory)) - 1

            if os.path.isdir(path):
                display_tree(
                    path,
                    prefix + ("└── " if is_last else "├── "),
                    file,
                    depth=depth,
                    current_depth=current_depth + 1,
                    exclude=exclude
                )
            else:
                file.write(prefix + ("└── " if is_last else "├── ") + item + "\n")
    except PermissionError:
        file.write(prefix + "[ACCESS DENIED] " + os.path.basename(directory) + "\n")

if __name__ == "__main__":
    # Load configuration from config.json
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    root_directory = config.get("directory", ".")
    initial_prefix = config.get("prefix", "")
    output_file = config.get("output_file", "output.txt")
    max_depth = config.get("depth", 1)  # Default depth is 1
    exclude_list = config.get("exclude", [])  # Default to empty list if not provided

    # Write the folder structure to the specified output file in UTF-8 encoding
    with open(output_file, "w", encoding="utf-8") as file:
        display_tree(root_directory, initial_prefix, file, depth=max_depth, exclude=exclude_list)

    print(f"Folder structure up to depth {max_depth} has been written to {output_file}, excluding {exclude_list}")
