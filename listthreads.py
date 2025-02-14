import os
import re

def list_forum_content(directory='forum_content'):
    """List all files in the specified directory, converting underscores to slashes and removing page-0-9*.json."""
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # Set to hold formatted file paths
    formatted_files = set()

    # Regex pattern to match 'page-0-9*.json'
    pattern = re.compile(r'page-\d+\.json$')

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        # Check if the file ends with .json
        if filename.endswith('.json'):
            # Remove the page-0-9*.json part using regex
            base_name = pattern.sub('', filename)
            # Convert underscores to slashes
            formatted_name = base_name.replace('_', '/')
            # Remove the .json extension
            formatted_name = formatted_name.replace('.json', '')  # Remove .json extension
            formatted_files.add(formatted_name)  # Add to set

    # Sort the formatted file paths
    sorted_files = sorted(formatted_files)

    # Print the formatted file paths
    for file in sorted_files:
        print(file)
    print(f"Total unique threads: {len(sorted_files)}")

if __name__ == "__main__":
    list_forum_content()
