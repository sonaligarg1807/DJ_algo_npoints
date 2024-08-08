#!/bin/bash
#$ -cwd
#$ -pe nproc 1
#$ -N dijkstra
#$ -e error.log
#$ -o output.log

# Check if the input file is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <input_gro_file>"
  exit 1
fi

input_gro_file=$1
output_resid_file="random_resids.txt"
cutoff_distance=0.5

# Extract 1000 random unique resids from the input_gro_file, skipping the first two header lines
tail -n +3 "$input_gro_file" | awk '{print $1}' | grep -o '^[0-9]\+' | sort -u | shuf -n 1000 > "$output_resid_file"

# Paths and directories
BASE_DIR="/data/sgarg/test_crystal_plane/5_namd_ham/5test_dj"
SOURCE_SCRIPT_DIR="$BASE_DIR"
SUBDIR_BASE="$BASE_DIR/result"

# Create necessary subdirectories and copy files
while read -r resid; do
    # Create subdirectory named result_<resid> for the residue
    resid_dir="${SUBDIR_BASE}_${resid}"
    mkdir -p "$resid_dir"

    # Copy necessary files to the subdirectory
    cp "$SOURCE_SCRIPT_DIR/dj_main.py" "$resid_dir"
    cp "$SOURCE_SCRIPT_DIR/dj_algo.py" "$resid_dir"
    cp "$SOURCE_SCRIPT_DIR/weights_source_resid_dj.py" "$resid_dir"
    cp "$SOURCE_SCRIPT_DIR/extract_molecules_dj.py" "$resid_dir"
    cp "$SOURCE_SCRIPT_DIR/pentacene-hole.spec" "$resid_dir"
    cp "$SOURCE_SCRIPT_DIR/test.sh" "$resid_dir"
    cp -r "$SOURCE_SCRIPT_DIR/input_files" "$resid_dir"

    # Run dj_main.py in the background for each subdirectory
    (cd "$resid_dir" && python3 dj_main.py "$resid" "$cutoff_distance" > "output.log" 2>&1) &
done < "$output_resid_file"

# Wait for all background jobs to complete
wait

echo "All calculations completed."