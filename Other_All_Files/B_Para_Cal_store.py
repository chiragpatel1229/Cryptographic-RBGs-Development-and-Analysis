from Tests_NIST import burstiness_para
import os


Burstiness_values = []
Location_to_store = "1000 Hashes and List of messages"          # put the folder name to store the results

for i in range(1, 2):                                           # Loop through each file

    file_name = f"hash_{i}.txt"                                 # Set up a file name
    main_path = "C:/Users/Chirag Patel/OneDrive/CRYPTOGRAPHY/Cryptography_Python/"
    file_path = os.path.join(main_path, Location_to_store, file_name)

    with open(file_path, "r") as file:                          # Read the file and extract the hashed sequence
        sequence = file.read()

    binary_list = [int(bit) for bit in sequence.strip()]        # Convert the sequence to a list of binary digits

    burst = burstiness_para.B_Cal(sequence)                     # Calculate burstiness using burstiness_para.B_Cal
    print(burst)
#     Burstiness_values.append((file_name, burst))
#
# output_file = "burstiness_output.txt"       # Save burstiness values to a text file
# with open(output_file, "w") as output:
#     for file_name, burst in Burstiness_values:
#         output.write(f"{file_name}: {burst}\n")
