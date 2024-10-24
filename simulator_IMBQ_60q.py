import os
from dotenv import load_dotenv
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import RemoveResetInZeroState
from qiskit_ibm_provider import IBMProvider, least_busy

# Load environment variables from .env file
load_dotenv()

# Access the API token
API_TOKEN = os.getenv("API_TOKEN")

# Initialize the IBMProvider with your API token
provider = IBMProvider(token=API_TOKEN)

# Get the least busy backend that supports the required number of qubits
backend = least_busy(provider.backends(filters=lambda x: 
                                      x.configuration().n_qubits >= 60 and 
                                      not x.configuration().simulator and 
                                      x.status().operational == True))

# Load the QASM file
with open('BlueQubit-Hackathon/data/RAW/circuit_3_60q.qasm', 'r') as file:
    qasm_content = file.read()

# Parse the QASM file and create a quantum circuit
qasm_circuit = QuantumCircuit.from_qasm_str(qasm_content)

# Use a Pass Manager to optimize the circuit further (e.g., remove unnecessary resets)
pass_manager = PassManager([RemoveResetInZeroState()])
# Run the pass manager on the circuit
qasm_circuit = pass_manager.run(qasm_circuit)


# Transpile the circuit with high optimization level
compiled_circuit = transpile(qasm_circuit, backend, optimization_level=3) 

# Execute the circuit on the backend
job = backend.run(compiled_circuit, shots=1024)
result = job.result()

# Get the counts (the frequency of each measured bitstring)
counts = result.get_counts()

# Plot the result histogram
plot_histogram(counts)

# Identify the hidden bitstring (the one with the highest probability)
hidden_bitstring = max(counts, key=counts.get)
print("Hidden bitstring:", hidden_bitstring)
