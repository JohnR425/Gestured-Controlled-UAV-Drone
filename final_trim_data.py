import os

### This script cleans up data to ensure every line is formatted properly and there is a consistent number of lines across all data.

DATA_LENGTH = 100
gesture_names = ["neutral", "up", "down", "left", "right", "forwards", "backwards", "flip", "land"]

updated_files = []

def contains_substrings(string, substrings):
    return any(sub in string for sub in substrings)

if __name__ == "__main__":
    os.chdir("data")
    for filename in os.listdir(os.getcwd()):
            if filename.endswith('.txt') and contains_substrings(filename, gesture_names):
                file_path = os.path.join(os.getcwd(), filename)
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                #Remove incomplete lines
                for line in lines:
                    if len(line.split()) != 6:
                        lines.remove(line)
                        updated_files.append(filename)

                # Count the number of lines
                num_lines = len(lines)  

                if num_lines > DATA_LENGTH:
                    # Trim the file to the first `length` # of lines
                    lines = lines[:DATA_LENGTH]
                    if updated_files.count(filename) == 0:
                        updated_files.append(filename)
                elif num_lines < DATA_LENGTH:
                    # Repeat the last line until the file has `length` # of lines
                    last_line = lines[-1] if lines else '\n'  # Default to newline if file is empty
                    while len(lines) < DATA_LENGTH:
                        lines.append(last_line)
                    if updated_files.count(filename) == 0:
                        updated_files.append(filename)
                
                # Write the adjusted lines back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(lines)

    print(f"Processed files: {updated_files}")