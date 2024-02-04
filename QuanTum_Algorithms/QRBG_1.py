""""
To generate Random sequences using the Simulators instead the actual Quantum Device to 
avoid the errors and noice may occur during the process.

This code specifically written to execute on IBM Quantum Lab Platform.

this is an option to avoid warning: (https://github.com/Qiskit/qiskit-ibm-provider/blob/main/README.md)

from qiskit_ibm_provider import IBMProvider
IBMProvider.save_account(token='MY_API_TOKEN')

"""""

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, transpile
from qiskit.tools.monitor import job_monitor
from qiskit_ibm_provider import IBMProvider


provider = IBMProvider("966bbf0869e7e72d9db993ddcf646794695d32a38f8e9f0d76eb6553533d1c650d58cfcf1ae079eb9077a59d1accaa76e038db084ccee20555d81b384f0f6568")
# print(provider.backends())                              # Check the available backends
backend = provider.get_backend('simulator_mps')           # select the backend device or simulator
a = provider.backends(filters=lambda x: x.configuration().num_qubits >= 2 and 'cz' in x.configuration().basis_gates)
print(a)

q = QuantumRegister(75, 'q')                            # set Quantum Register with up-to 63 qubits
c = ClassicalRegister(75, 'c')                          # set Classical Register with up-to 63 qubits

circuit = QuantumCircuit(q, c)                          # Create Quantum Circuit using the Quantum and Classical Registers

circuit.h(q)                                            # Apply hadamard gate on all qubits

circuit.measure(q, c)                                   # Measures each qubit and save the result in Classical bits

# tcirc = transpile(circuit, backend)

binary_sequence = ""                                    # empty string to save the binary sequence

for i in range(2):
    job = execute(circuit, backend, shots=100)            # execute the Q-circuit on the simulator or Q-device which returns an object

    print(f'Executing Job...\n {job_monitor(job)}\n')  # Check the Status in real time

    result = job.result()                              # returns a dictionary from an object

    counts = result.get_counts()                       # number of times - unique binary sequences

    binary_sequence += list(counts.keys())[0]          # select the unique binary sequence by its index here it's [0]

# binary_sequence = binary_sequence[:256]
# print the final binary sequence
print('RESULT: ', binary_sequence, '\n')
print(len(binary_sequence))

