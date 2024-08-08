import subprocess
import os
import sys

def get_last_value_from_file(file_path, column):
    """Reads the last value of the specified column from the file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if not lines:
            raise ValueError("The file is empty.")
        last_line = lines[-1]
        value = last_line.split()[column - 1]  # Convert column to 0-based index
    return value

def remove_last_line_from_file(file_path):
    """Removes the last line from the specified file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    if not lines:
        raise ValueError("The file is empty.")
    with open(file_path, 'w') as file:
        file.writelines(lines[:-1])

def scan_for_unique_resid(current_resid, cutoff_distance, used_resids):
    """Scan over a range of cutoff distances to find a unique residue."""
    step = cutoff_distance / 2
    distances = [cutoff_distance - step, cutoff_distance + step]
    for dist in distances:
        subprocess.run(['python3', 'weights_source_resid_dj.py', current_resid, str(dist)])
        # Check if the output file 'average_coupling_values.txt' exists
        if not os.path.exists('average_coupling_values.txt'):
            continue
        # Run the dj_algo.py script to find the highest coupling residue
        subprocess.run(['python3', 'dj_algo.py', '1'])  # Always start with rank 1
        if not os.path.exists('output_path.txt'):
            continue
        # Get the last value of the 2nd column from 'output_path.txt'
        d = get_last_value_from_file('output_path.txt', 2)
        if d not in used_resids:
            return d, dist
    return None, cutoff_distance

def find_unique_resid(current_resid, cutoff_distance, used_resids):
    """Find a unique coupling residue starting from the highest rank."""
    rank = 1
    while True:
        subprocess.run(['python3', 'weights_source_resid_dj.py', current_resid, str(cutoff_distance)])
        # Check if the output file 'average_coupling_values.txt' exists
        if not os.path.exists('average_coupling_values.txt'):
            return None
        subprocess.run(['python3', 'dj_algo.py', str(rank)])
        if not os.path.exists('output_path.txt'):
            return None
        # Get the nth highest coupling residue
        d = get_last_value_from_file('output_path.txt', 2)
        if d not in used_resids:
            return d
        rank += 1  # Move to the next highest residue

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 dj_main.py <resid> <cutoff distance>")
        sys.exit(1)

    a = sys.argv[1]
    b = float(sys.argv[2])
    c = set()
    c.add(a)

    iterations = 0
    max_iterations = 20

    while iterations < max_iterations:
        # Run the weights_source_resid_dj.py script
        subprocess.run(['python3', 'weights_source_resid_dj.py', a, str(b)])

        # Check if the output file 'average_coupling_value.txt' exists
        if not os.path.exists('average_coupling_values.txt'):
            raise FileNotFoundError("The file 'average_coupling_values.txt' was not created.")

        # Run the dj_algo.py script with rank 1
        subprocess.run(['python3', 'dj_algo.py', '1'])

        # Check if the output file 'output_path.txt' exists
        if not os.path.exists('output_path.txt'):
            raise FileNotFoundError("The file 'output_path.txt' was not created.")

        # Get the last value of the 2nd column from 'output_path.txt'
        d = get_last_value_from_file('output_path.txt', 2)

        # Check if the value of 'd' is in set 'c'
        if d not in c:
            a = d  # Update 'a' to 'd'
            c.add(a)
        else:
            d, b = scan_for_unique_resid(a, b, c)
            if d is None:
                d = find_unique_resid(a, b, c)  # Start from the highest unique residue
                if d is None:
                    break  # If no unique residue found, break the loop
            a = d  # Update 'a' to the unique residue found
            c.add(a)

        iterations += 1  # Increment the iteration counter

if __name__ == "__main__":
    main()

#.....................................................................................................
# import subprocess
# import os

# def get_last_value_from_file(file_path, column):
#     """Reads the last value of the specified column from the file."""
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         if not lines:
#             raise ValueError("The file is empty.")
#         last_line = lines[-1]
#         value = last_line.split()[column - 1]  # Convert column to 0-based index
#     return value

# def remove_last_line_from_file(file_path):
#     """Removes the last line from the specified file."""
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#     if not lines:
#         raise ValueError("The file is empty.")
#     with open(file_path, 'w') as file:
#         file.writelines(lines[:-1])

# def scan_for_unique_resid(current_resid, cutoff_distance, used_resids):
#     """Scan over a range of cutoff distances to find a unique residue."""
#     step = cutoff_distance / 2
#     distances = [cutoff_distance - step, cutoff_distance + step]
#     for dist in distances:
#         subprocess.run(['python3', 'weights_source_resid_dj.py', current_resid, str(dist)])
#         # Check if the output file 'average_coupling_values.txt' exists
#         if not os.path.exists('average_coupling_values.txt'):
#             continue
#         # Run the dj_algo.py script to find the highest coupling residue
#         subprocess.run(['python3', 'dj_algo.py', '1'])  # Always start with rank 1
#         if not os.path.exists('output_path.txt'):
#             continue
#         # Get the last value of the 2nd column from 'output_path.txt'
#         d = get_last_value_from_file('output_path.txt', 2)
#         if d not in used_resids:
#             return d, dist
#     return None, cutoff_distance

# def find_unique_resid(current_resid, cutoff_distance, used_resids):
#     """Find a unique coupling residue starting from the highest rank."""
#     rank = 1
#     while True:
#         subprocess.run(['python3', 'weights_source_resid_dj.py', current_resid, str(cutoff_distance)])
#         # Check if the output file 'average_coupling_values.txt' exists
#         if not os.path.exists('average_coupling_values.txt'):
#             return None
#         subprocess.run(['python3', 'dj_algo.py', str(rank)])
#         if not os.path.exists('output_path.txt'):
#             return None
#         # Get the nth highest coupling residue
#         d = get_last_value_from_file('output_path.txt', 2)
#         if d not in used_resids:
#             return d
#         rank += 1  # Move to the next highest residue

# def main():
#     a = input("Enter resid: ")
#     b = float(input("Enter cutoff distance: "))
#     c = set()
#     c.add(a)

#     iterations = 0
#     max_iterations = 20

#     while iterations < max_iterations:
#         # Run the weights_source_resid_dj.py script
#         subprocess.run(['python3', 'weights_source_resid_dj.py', a, str(b)])

#         # Check if the output file 'average_coupling_value.txt' exists
#         if not os.path.exists('average_coupling_values.txt'):
#             raise FileNotFoundError("The file 'average_coupling_values.txt' was not created.")

#         # Run the dj_algo.py script with rank 1
#         subprocess.run(['python3', 'dj_algo.py', '1'])

#         # Check if the output file 'output_path.txt' exists
#         if not os.path.exists('output_path.txt'):
#             raise FileNotFoundError("The file 'output_path.txt' was not created.")

#         # Get the last value of the 2nd column from 'output_path.txt'
#         d = get_last_value_from_file('output_path.txt', 2)

#         # Check if the value of 'd' is in set 'c'
#         if d not in c:
#             a = d  # Update 'a' to 'd'
#             c.add(a)
#         else:
#             d, b = scan_for_unique_resid(a, b, c)
#             if d is None:
#                 d = find_unique_resid(a, b, c)  # Start from the highest unique residue
#                 if d is None:
#                     break  # If no unique residue found, break the loop
#             a = d  # Update 'a' to the unique residue found
#             c.add(a)

#         iterations += 1  # Increment the iteration counter

# if __name__ == "__main__":
#     main()