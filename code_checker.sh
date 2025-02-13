#!/bin/zsh

# Initialize variables
typeset -F total_score=0
typeset -i file_count=0

print "Running pylint on Python files in root directory..."
print "------------------------------------------------"

# Find all .py files in root directory only
for file in *.py(.N); do
    # Skip files in __pycache__
    [[ $file == *"__pycache__"* ]] && continue
    
    print "Checking $file..."
    # Run pylint and capture the output
    output=$(pylint $file)
    
    # Display the output
    print $output
    print "------------------------------------------------"
    
    # Extract the score
    score=$(print $output | grep "Your code has been rated at" | grep -o '[0-9.]*' | head -1)
    
    if [[ -n $score ]]; then
        (( total_score += score ))
        (( file_count++ ))
    fi
done

# Calculate and display average score
if (( file_count > 0 )); then
    average=$(( total_score / file_count ))
    percentage=$(( (total_score / file_count) * 10 ))
    printf "Average score across %d files: %.2f/10 (%.1f%%)\n" $file_count $average $percentage
else
    print "No Python files found in root directory"
fi
