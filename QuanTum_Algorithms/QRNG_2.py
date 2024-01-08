""""
To generate Random sequences using the Simulators instead the actual Quantum Device to 
avoid the errors and noice may occur during the process.

This code specifically written to executes on IBM Quantum Lab Platform.

"""""


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, IBMQ
from qiskit.tools.monitor import job_monitor

IBMQ.enable_account("30906764f6179a00a2dd23113069d9fe07cd14f6e934675760f0eb3e401ecca40dcabcb4991ac016af09c3277662da96f6ec9dbc9e98ae74dad5575d3d233a54")
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')     # Get the provider with the default values as given above
backend = provider.get_backend('simulator_extended_stabilizer')             # select the backend device or simulator

q = QuantumRegister(63, 'q')                            # set Quantum Register with up-to 63 qubits
c = ClassicalRegister(63, 'c')                          # set Classical Register with up-to 63 qubits

circuit = QuantumCircuit(q, c)                          # Create Quantum Circuit using the Quantum and Classical Registers

circuit.h(q)                                            # Apply hadamard gate on all qubits

circuit.measure(q, c)                                   # Measures each qubit and save the result in Classical bits

binary_sequence_1 = ""                                  # empty string to save the binary sequence
binary_sequence_2 = ""

for i in range(5):
    job = execute(circuit, backend,shots=100)          # execute the Q-circuit on the simulator or Q-device which returns an object

    print(f'Executing Job...\n {job_monitor(job)}\n')  # Check the Status in real time

    result = job.result()                              # returns a dictionary from an object

    counts = result.get_counts()                       # number of times - unique binary sequences

    binary_sequence_1 += list(counts.keys())[0]        # select the unique binary sequence by its index here it's [0]
    binary_sequence_2 += list(counts.keys())[1]        # select the unique binary sequence by its index here it's [0]

binary_sequence_1 = binary_sequence_1[:256]            # Consider only required sequence length
binary_sequence_2 = binary_sequence_2[:256]

# print the binary sequence
print('seq_1 ', binary_sequence_1, '\n', 'seq_2', binary_sequence_2, '\n')
print(binary_sequence_1 == binary_sequence_2, '\n')
print('1', len(binary_sequence_1), '\n2', len(binary_sequence_2))
