import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# Import from Qiskit Aer noise module
from qiskit_aer.noise import (NoiseModel, thermal_relaxation_error)
# ======================================================================================================================
# from qiskit_ibm_runtime import QiskitRuntimeService

# Ref: https://docs.quantum.ibm.com/verify/building_noise_models#noise-model-examples
"""To test this algorithm Please use the jupiter notebook on IMB portal -> https://lab.quantum.ibm.com 

https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html
UPDATE: batched_shots_gpu_max_qubits (int): This option sets the maximum number of qubits for enabling the batched_shots_gpu option. 
If the number of active circuit qubits is greater than this value batching of simulation shots will not be used. (Default: 16).
Now to design a circuit for aer simulator the maximum bit size is fixed to max 16 qubits for accuracy and precision purpose in the new update.
"""

# service = QiskitRuntimeService()
# backend = service.backend("ibm_brisbane")
# noise_model = NoiseModel.from_backend(backend)

# ======================================================================================================================
# System Specification
n_qubits = 24
circ = QuantumCircuit(n_qubits)

# Applying Hadamard gate to all qubits
for qubit in range(n_qubits):
    circ.h(qubit)

# Measure all qubits
circ.measure_all()
# print(circ)

# ======================================================================================================================
'''Noise model 2'''
# thermal relaxation method T1 and T2 values for qubits 0-3

# Generate T1 and T2 values for all qubits
T1s = np.random.normal(50e3, 10e3, n_qubits)  # Sampled from normal distribution mean 50 microseconds
T2s = np.random.normal(70e3, 10e3, n_qubits)  # Sampled from normal distribution mean 70 microseconds

# Ensure T2s are not greater than 2*T1s
T2s = np.array([min(T2s[j], 2 * T1s[j]) for j in range(n_qubits)])

# Define gate times
time_u1 = 0  # virtual gate
time_u2 = 50  # single X90 pulse
time_u3 = 100  # two X90 pulses
time_cx = 300
time_reset = 1000  # 1 microsecond
time_measure = 1000  # 1 microsecond

# Create thermal relaxation errors for each type of gate apply it to each qubit
errors_reset = [thermal_relaxation_error(T1s[j], T2s[j], time_reset) for j in range(n_qubits)]
errors_measure = [thermal_relaxation_error(T1s[j], T2s[j], time_measure) for j in range(n_qubits)]
errors_u1 = [thermal_relaxation_error(T1s[j], T2s[j], time_u1) for j in range(n_qubits)]
errors_u2 = [thermal_relaxation_error(T1s[j], T2s[j], time_u2) for j in range(n_qubits)]
errors_u3 = [thermal_relaxation_error(T1s[j], T2s[j], time_u3) for j in range(n_qubits)]
errors_cx = [[thermal_relaxation_error(T1s[j], T2s[j], time_cx).expand(
    thermal_relaxation_error(T1s[k], T2s[k], time_cx))
    for k in range(n_qubits)] for j in range(n_qubits)]

# Add errors to the noise model
noise_thermal = NoiseModel()
for j in range(n_qubits):
    noise_thermal.add_quantum_error(errors_reset[j], 'reset', [j])
    noise_thermal.add_quantum_error(errors_measure[j], 'measure', [j])
    noise_thermal.add_quantum_error(errors_u1[j], 'u1', [j])
    noise_thermal.add_quantum_error(errors_u2[j], 'u2', [j])
    noise_thermal.add_quantum_error(errors_u3[j], 'u3', [j])
    for k in range(n_qubits):
        noise_thermal.add_quantum_error(errors_cx[j][k], 'cx', [j, k])

print(noise_thermal)

# =========================================================================================
# Create noisy simulator backend
sim_noise = AerSimulator()

# Initialize all buffers for all the sequences
create_seq = [''] * 100

for i in range(43):   # range will multiply with the No. qubits and creates a length of sequence
    passmanager = generate_preset_pass_manager(optimization_level=3, backend=sim_noise)
    circ_thermal = passmanager.run(circ)
    # shots will decide the number of sequences as the keys dictionaries are based on it
    result_thermal = sim_noise.run(circ_thermal, noise_model=noise_thermal, shots=101).result()
    counts_thermal = result_thermal.get_counts()
    print(i)
    keys = list(counts_thermal.keys())
    for j in range(len(create_seq)):
        if j < len(keys):
            create_seq[j] += keys[j]

# Print all the buffers
# for i, buffer in enumerate(buffers):
#     print(f'seq_{i+1} ', buffer, '\n')
#     print(f'{i+1}', len(buffer), '\n')

# Save all the buffers to a text file
with open('QRNG.txt', 'w') as f:
    for i, buffer in enumerate(create_seq):
        f.write(buffer + '\n')