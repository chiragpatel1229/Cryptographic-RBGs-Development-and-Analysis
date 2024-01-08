import matplotlib.pyplot as plt

# This code creates M-Sequences for the given list of sequence_lengths
# It will create graphs of ACF for all the sequences, it can merge the ACF graphs for comparison
# It will give an insight of the generated sequence Balance by calculating the number of 0s and 1s in it

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================

primitive_polynomial = [5, 2]  # Enter the polynomial as a list of integers

sequence_lengths = [31, 127]  # [x, y, z, ...] provide one or more sequence lengths in a list

initial_state = [1, 0, 1, 0, 1]  # Enter the USER desired initial state

show_graphs = True  # Set to True to display the graphs, False to suppress them

# this parameter is only useful when show_graphs = True!
merge_plots_option = False  # Set to True to merge all ACF plots, False to show separate plots

# ===================================== USER INPUTS ================================================================
# ===================================== USER INPUTS ================================================================


def generate_m_sequence(polynomial, lengths, state):

    if not isinstance(lengths, list):   # Make sure lengths is a list even a single length
        lengths = [lengths]

    poly = f"{sum([2**i for i in polynomial]) | 1:b}"   # Convert the polynomial list to an integer

    num_bits = len(poly) - 1    # the number of bits needed to represent the polynomial

    # Extract the feedback stages from the polynomial
    feedback_stages = [int(stage) for stage in poly[:].zfill(num_bits)]

    m_sequences = []    # List to store the generated m-sequence

    for length in lengths:

        shift_register = state[:]   # Set the shift register with the given initial state
        m_seq = []

        for _ in range(length):

            output_bit = shift_register[-1]     # Capture the output bit

            # Calculate the feedback bit using XOR operation
            feedback_bit = sum([feedback_stages[i] * shift_register[-i-1] for i in range(num_bits)]) % 2
            shift_register = [feedback_bit] + shift_register[:-1]   # add new bit and remove the last
            m_seq.append(output_bit)    # Append the output bit to the m-sequence

        m_sequences.append(m_seq)

    return m_sequences, poly


def calculate_acf(c, v):
    m = len(c)
    s = 0
    for mu in range(m):
        i = (mu + v) % m    # Modulo operation for "wrap around" effect
        s += c[i] * c[mu]
    return s / m


# Generate the m-sequence using the user selected parameters
M_sequences, b_poly = generate_m_sequence(primitive_polynomial, sequence_lengths, initial_state)

print("Primitive Polynomial = ", primitive_polynomial, "\n")    # Print the parameters
print("Polynomial - Binary  = ", b_poly, "\n")
print("Initial State        = ", initial_state, "\n")   # Print the parameters

# Print the m-sequences and check the balance
for seq_index, seq in enumerate(M_sequences):
    num_zeros = seq.count(0)
    num_ones = seq.count(1)
    print(f"m-sequence {seq_index + 1} of length {sequence_lengths[seq_index]}: {seq}")
    print(f"Sequence Balance: 0s = {num_zeros}, 1s = {num_ones}\n")

    # Plot each bit as a line graph for the m-sequence
    plt.figure()
    plt.bar(range(len(seq)), seq, width=0.6, align='edge')
    plt.title(f'Line Graph of m-sequence {seq_index + 1}')
    plt.xlabel('Bit Index')
    plt.ylabel('Bit Value')
    plt.grid()
    if show_graphs:
        plt.show(block=False)

        # Pause for a short time to allow the plot to display before proceeding to the next one
        plt.pause(0.1)

# Keep the plots open until manually closed by the user
if show_graphs:
    plt.show()

# Plot the auto_correlation function for each m-sequence
if merge_plots_option:
    # Create a single plot for all m-sequences
    if show_graphs:
        plt.figure()

        for seq_index, m_sequence in enumerate(M_sequences):
            modified_sequence = [(-1)**bit for bit in m_sequence]

            v_list = list(range(31))
            acf_list = [calculate_acf(modified_sequence, v) for v in v_list]

            plt.bar(v_list, acf_list, width=0.4, align='edge', label=f'ACF of m-sequence {seq_index + 1}')

        plt.title('Auto-correlation Function of M-Sequences')
        plt.xlabel('Shift Value')
        plt.ylabel('ACF Value')
        plt.grid()
        plt.ylim(bottom=0.20)
        plt.legend()

        # Display the plot without blocking code execution
        plt.show()
else:
    # Create separate plots for each m-sequence
    for seq_index, m_sequence in enumerate(M_sequences):
        modified_sequence = [(-1)**bit for bit in m_sequence]

        v_list = list(range(31))
        acf_list = []

        for v in v_list:
            acf = calculate_acf(modified_sequence, v)
            acf_list.append(acf)

        plt.figure()
        plt.bar(v_list, acf_list, width=0.4, align='edge', label=f'ACF of m-sequence {seq_index + 1}')
        plt.title(f'Auto_correlation Function of M-Sequence {seq_index + 1}')
        plt.xlabel('Shift Value')
        plt.ylabel('ACF Value')
        plt.grid()
        plt.ylim(bottom=-0.3)
        plt.legend()
        if show_graphs:
            # Display the plot without blocking code execution
            plt.show(block=False)

            # Pause for a short time to allow the plot to display before proceeding to the next one
            plt.pause(0.1)

# Keep the plots open until manually closed by the user
if show_graphs:
    plt.show()

