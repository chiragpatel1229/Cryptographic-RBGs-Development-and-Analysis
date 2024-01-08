""""
To generate Random sequences using the Simulators instead the actual Quantum Device to 
avoid the errors and noice may occur during the process.

This code specifically written to execute on IBM Quantum Lab Platform.

this is an option to avoid warning: (https://github.com/Qiskit/qiskit-ibm-provider/blob/main/README.md)

from qiskit_ibm_provider import IBMProvider
IBMProvider.save_account(token='MY_API_TOKEN')

"""""

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, IBMQ
from qiskit.tools.monitor import job_monitor


IBMQ.enable_account("30906764f6179a00a2dd23113069d9fe07cd14f6e934675760f0eb3e401ecca40dcabcb4991ac016af09c3277662da96f6ec9dbc9e98ae74dad5575d3d233a54")
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')   # Get the provider with the default values as given above
backend = provider.get_backend('simulator_extended_stabilizer')           # select the backend device or simulator

q = QuantumRegister(63, 'q')                            # set Quantum Register with up-to 63 qubits
c = ClassicalRegister(63, 'c')                          # set Classical Register with up-to 63 qubits

circuit = QuantumCircuit(q, c)                          # Create Quantum Circuit using the Quantum and Classical Registers

circuit.h(q)                                            # Apply hadamard gate on all qubits

circuit.measure(q, c)                                   # Measures each qubit and save the result in Classical bits

binary_sequence = ""                                    # empty string to save the binary sequence

for i in range(5):
    job = execute(circuit, backend,shots=50)            # execute the Q-circuit on the simulator or Q-device which returns an object

    print(f'Executing Job...\n {job_monitor(job)}\n')  # Check the Status in real time

    result = job.result()                              # returns a dictionary from an object

    counts = result.get_counts()                       # number of times - unique binary sequences

    binary_sequence += list(counts.keys())[0]          # select the unique binary sequence by its index here it's [0]

binary_sequence = binary_sequence[:256]
# print the final binary sequence
print('RESULT: ', binary_sequence, '\n')
print(len(binary_sequence))

