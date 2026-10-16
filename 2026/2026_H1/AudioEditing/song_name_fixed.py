import os
import re


def to_snake_case(name):
    """
    Converts a string into a clean snake_case version.
    Example: " My Song & Title (Remix) " -> "my_song_and_title_remix"
    """
    # 1. Strip leading/trailing whitespace
    name = name.strip()

    # 2. Replace special characters like '&' with 'and'
    name = name.replace("&", "and")

    # 3. Keep only letters, numbers, and spaces
    name = re.sub(r"[^a-zA-Z0-9 ]", "", name)

    # 4. Convert to lowercase
    name = name.lower()

    # 5. Replace spaces with underscores
    name = name.replace(" ", "_")

    # 6. Replace multiple underscores with a single one
    name = re.sub(r"_+", "_", name)

    return name


def rename_files_in_folder(folder_path="input"):
    """
    Renames files in the specified folder based on the pattern:
    "XXX - Desired Name - YYY.mp3" -> "desired_name.mp3"
    """

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at '{folder_path}'")
        print("Please create an 'input' folder and put your files inside it.")
        return

    print(f"Scanning files in '{folder_path}'...\n")

    renamed_count = 0
    skipped_count = 0

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        old_filepath = os.path.join(folder_path, filename)

        # Skip if it's a directory
        if not os.path.isfile(old_filepath):
            continue

        # Split the filename into the name part and the extension
        name_part, extension = os.path.splitext(filename)

        # Find the first hyphen
        first_hyphen_index = name_part.find("-")

        # Find the last hyphen
        last_hyphen_index = name_part.rfind("-")

        # Check if we have at least two hyphens to extract from
        if first_hyphen_index != -1 and last_hyphen_index > first_hyphen_index:
            # Extract the text between the first and last hyphens
            extracted_name = name_part[first_hyphen_index + 1 : last_hyphen_index]

            # Convert to snake_case
            new_name_part = to_snake_case(extracted_name)

            # If the resulting name is empty, skip it
            if not new_name_part:
                print(f"Skipping '{filename}': No valid name found between hyphens.")
                skipped_count += 1
                continue

            # Create the new filename and filepath
            new_filename = f"{new_name_part}{extension}"
            new_filepath = os.path.join(folder_path, new_filename)

            # Check if a file with the new name already exists
            if os.path.exists(new_filepath):
                print(f"Skipping '{filename}': Target '{new_filename}' already exists.")
                skipped_count += 1
                continue

            # Perform the rename
            try:
                os.rename(old_filepath, new_filepath)
                print(f'Renamed: "{filename}"  ->  "{new_filename}"')
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming '{filename}': {e}")
                skipped_count += 1

        else:
            # Did not match the pattern "..." - "..." - "..."
            print(f"Skipping '{filename}': Does not match expected format.")
            skipped_count += 1

    print("\n--- Done ---")
    print(f"Renamed: {renamed_count} files")
    print(f"Skipped: {skipped_count} files")


# --- Main execution ---
if __name__ == "__main__":
    rename_files_in_folder()
    input("\nPress Enter to exit.")  # Keeps window open on Windows
