from Tests_NIST import burstiness_para

Burstiness_values = []
for i in range(1, 1001):  # Loop through each file

    file_name = f"hash_{i}.txt"  # Set up a file name

    with open(file_name, "r") as file:  # Read the file and extract the hashed sequence
        sequence = file.read()

    binary_list = [int(bit) for bit in sequence.strip()]   # Convert the sequence to a list of binary digits

    # Calculate burstiness using burstiness_para.B_Cal
    burst = burstiness_para.B_Cal(sequence)
    # print(burst)
    Burstiness_values.append((file_name, burst))

output_file = "burstiness_output.txt"       # Save burstiness values to a text file name
with open(output_file, "w") as output:
    for file_name, burst in Burstiness_values:
        output.write(f"{file_name}: {burst}\n")





# # Read values from the file
# Burstiness_values = []
# with open("burstiness_output.txt", "r") as input_file:
#     for line in input_file:
#         _, burst = line.split(':')
#         Burstiness_values.append(float(burst))
#
# # Plotting the burstiness values
# files = range(1, 1001)  # Assuming 1000 files
# plt.bar(files, Burstiness_values)
# plt.xlabel('Files')
# plt.ylabel('Burstiness Values')
# plt.title('Burstiness Values for Each File')
# plt.show()
