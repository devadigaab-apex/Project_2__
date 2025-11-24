import sys
import random
import gzip
from collections import defaultdict
import matplotlib.pyplot as plt

ref_probab=defaultdict(int)
counts=defaultdict(int)
input_file=sys.argv[1]
rescaled_counts=defaultdict(int)

#reference probality dictionary creation
for line in sys.stdin:
    l=int(line.strip().split()[0])
    probab=float(line.strip().split()[1])
    ref_probab[l]=probab


f1=gzip.open(input_file,"rt")
#fragment length counts dictionary creation
for i in f1:
    start=int(i.strip().split()[1])
    stop=int(i.strip().split()[2])
    length=stop-start
    counts[length]+=1

f1.close()

#calculating what is the minimum we can allow
min_bar=float('inf')
for i,j in ref_probab.items():
    if j>0:
        frag_actual_count=counts.get(i,0)
        if frag_actual_count>0:
            allowed=frag_actual_count/j
            if allowed<min_bar:
                min_bar=allowed
keep={}
for i, j in counts.items():
    if i in ref_probab and counts[i]>0:
        req_count=min_bar*ref_probab[i]
        probability=req_count/counts[i]
        keep[i]=min(1.0,probability)
    else:
        keep[i]=0.0


f1=gzip.open(input_file,"rt")
f_output=open("Rescaled","w")

#Rescaling done below
for line in f1:
    start=int(line.strip().split()[1])
    stop=int(line.strip().split()[2])
    recal_length=int(stop)-int(start)
    p=keep.get(recal_length,0.0)

    if random.random()<p:
        f_output.write(line)
        rescaled_counts[recal_length]+=1

print("Rescaling done!!")

f1.close()
f_output.close()

print("Generating plot...")

# Get all unique lengths to sort the X-axis
all_lengths = sorted(list(set(counts.keys()) | set(ref_probab.keys())))

# Prepare Y-axis data
y_input = [counts[l] for l in all_lengths]          # The Gray Bars (Original)
y_output = [rescaled_counts[l] for l in all_lengths] # The Blue Bars (Result)

# Calculate "Ideal" line for comparison
# We scale the percentages to match the total number of lines we actually output
total_output_lines = sum(rescaled_counts.values())
y_target = [ref_probab[l] * total_output_lines for l in all_lengths]

# Create Plot
plt.figure(figsize=(12, 6))

# 1. Plot Original Input (Gray area)
plt.fill_between(all_lengths, y_input, color='gray', alpha=0.3, label='Original Input')

# 2. Plot Actual Result (Blue line/dots)
plt.plot(all_lengths, y_output, label='Rescaled Output', color='blue', linewidth=2)

# 3. Plot Ideal Target (Red dashed line)
plt.plot(all_lengths, y_target, label='Ideal Target Shape', color='red', linestyle='--')

plt.title(f"Rescaling Result (Total Kept: {total_output_lines})")
plt.xlabel("Fragment Length")
plt.ylabel("Count")
plt.legend()
plt.grid(True, alpha=0.3)

# Save the plot to a file
plt.savefig("rescale_check.png")
print("Plot saved as 'rescale_check.png'")
