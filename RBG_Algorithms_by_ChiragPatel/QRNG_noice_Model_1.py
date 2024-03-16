import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# Import from Qiskit Aer noise module
from qiskit_aer.noise import (
    NoiseModel,
    QuantumError,
    ReadoutError,
    depolarizing_error,
    pauli_error,
    thermal_relaxation_error,
)
# ======================================================================================================================
from qiskit_ibm_runtime import QiskitRuntimeService

# Ref: https://docs.quantum.ibm.com/verify/building_noise_models#noise-model-examples
"""To test this algorithm Please use the jupiter notebook on IMB portal -> https://lab.quantum.ibm.com 

https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html
UPDATE: batched_shots_gpu_max_qubits (int): This option sets the maximum number of qubits for enabling the batched_shots_gpu option. 
If the number of active circuit qubits is greater than this value batching of simulation shots will not be used. (Default: 16).
Now to design a circuit for aer simulator the maximum bit size is fixed to max 16 qubits for accuracy and precision purpose in the new update.
"""

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")
noise_model = NoiseModel.from_backend(backend)

# ======================================================================================================================
# System Specification
n_qubits = 16
circ = QuantumCircuit(n_qubits)

# Applying Hadamard gate to all qubits
for qubit in range(n_qubits):
    circ.h(qubit)

# Measure all qubits
circ.measure_all()
# print(circ)

# ======================================================================================================================
'''Noise model 1
# Noise Example 1: Basic bit-flip error noise model
# Lets consider a simple toy noise model example common in quantum information theory research:

# When applying a single qubit gate, flip the state of the qubit with probability p_gate1.
# When applying a 2-qubit gate apply single-qubit errors to each qubit.
# When resetting a qubit reset to 1 instead of 0 with probability p_reset.
# When measuring a qubit, flip the state of the qubit with probability p_meas.
'''
 
# Example error probabilities
p_reset = 0.03
p_meas = 0.1
p_gate1 = 0.05

# QuantumError objects
error_reset = pauli_error([('X', p_reset), ('I', 1 - p_reset)])
error_meas = pauli_error([('X', p_meas), ('I', 1 - p_meas)])
error_gate1 = pauli_error([('X', p_gate1), ('I', 1 - p_gate1)])
error_gate2 = error_gate1.tensor(error_gate1)

# Add errors to noise model
noise_bit_flip = NoiseModel()
noise_bit_flip.add_all_qubit_quantum_error(error_reset, "reset")
noise_bit_flip.add_all_qubit_quantum_error(error_meas, "measure")
noise_bit_flip.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"])
noise_bit_flip.add_all_qubit_quantum_error(error_gate2, ["cx"])

print(noise_bit_flip)

# ======================================================================================================================

# Create noisy simulator backend
sim_noise = AerSimulator(noise_model=noise_bit_flip)

# Transpile circuit for noisy basis gates
passmanager = generate_preset_pass_manager(optimization_level=3, backend=sim_noise)
circ_b_noise = passmanager.run(circ)

# Initialize an empty string to store the binary sequence
binary_sequence = ''

# Number of times to run the circuit to get 512 bits
num_runs = 512 // n_qubits

for _ in range(num_runs):
    # Run and get counts
    result_bit_flip = sim_noise.run(circ_b_noise).result()
    counts_bit_flip = result_bit_flip.get_counts(0)

    # Get the most frequent bitstring
    most_frequent_bitstring = max(counts_bit_flip, key=counts_bit_flip.get)
    binary_sequence += most_frequent_bitstring

print('RESULT: ', binary_sequence, '\n')
print(len(binary_sequence))


# ======================================================================================================================
'''Noise model 2'''
# thermal relaxation method T1 and T2 values for qubits 0-3
n_bits = 4
T1s = np.random.normal(50e3, 10e3, n_bits)  # Sampled from normal distribution mean 50 microsecond
T2s = np.random.normal(70e3, 10e3, n_bits)  # Sampled from normal distribution mean 50 microsecond

# Truncate random T2s <= T1s
T2s = np.array([min(T2s[j], 2 * T1s[j]) for j in range(n_bits)])

# Instruction times (in nanoseconds)
time_u1 = 0  # virtual gate
time_u2 = 50  # (single X90 pulse)
time_u3 = 100  # (two X90 pulses)
time_cx = 300
time_reset = 1000  # 1 microsecond
time_measure = 1000  # 1 microsecond

# QuantumError objects
errors_reset = [thermal_relaxation_error(t1, t2, time_reset)
                for t1, t2 in zip(T1s, T2s)]
errors_measure = [thermal_relaxation_error(t1, t2, time_measure)
                  for t1, t2 in zip(T1s, T2s)]
errors_u1 = [thermal_relaxation_error(t1, t2, time_u1)
             for t1, t2 in zip(T1s, T2s)]
errors_u2 = [thermal_relaxation_error(t1, t2, time_u2)
             for t1, t2 in zip(T1s, T2s)]
errors_u3 = [thermal_relaxation_error(t1, t2, time_u3)
             for t1, t2 in zip(T1s, T2s)]
errors_cx = [[thermal_relaxation_error(t1a, t2a, time_cx).expand(
    thermal_relaxation_error(t1b, t2b, time_cx))
    for t1a, t2a in zip(T1s, T2s)]
    for t1b, t2b in zip(T1s, T2s)]

# Add errors to noise model
noise_thermal = NoiseModel()
for j in range(n_bits):
    noise_thermal.add_quantum_error(errors_reset[j], "reset", [j])
    noise_thermal.add_quantum_error(errors_measure[j], "measure", [j])
    noise_thermal.add_quantum_error(errors_u1[j], "u1", [j])
    noise_thermal.add_quantum_error(errors_u2[j], "u2", [j])
    noise_thermal.add_quantum_error(errors_u3[j], "u3", [j])
    for k in range(n_bits):
        noise_thermal.add_quantum_error(errors_cx[j][k], "cx", [j, k])

print(noise_thermal)

# ======================================================================================================================

# Run the noisy simulation
sim_thermal = AerSimulator(noise_model=noise_thermal)

# Transpile circuit for noisy basis gates
passmanager = generate_preset_pass_manager(optimization_level=3, backend=sim_thermal)
circ_tthermal = passmanager.run(circ)

# Initialize an empty string to store the binary sequence
binary_sequence = ''

# Number of times to run the circuit to get 512 bits
num_runs = 512 // n_qubits

for _ in range(num_runs):
    # Run and get counts
    result_thermal = sim_thermal.run(circ_tthermal).result()
    counts_thermal = result_thermal.get_counts(0)

    # Get the most frequent bitstring
    most_frequent_bitstring = max(counts_thermal, key=counts_thermal.get)
    binary_sequence += most_frequent_bitstring

print('RESULT: ', binary_sequence, '\n')
print(len(binary_sequence))


# ======================================================================================================================

