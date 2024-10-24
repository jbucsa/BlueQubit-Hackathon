# Define the function to update the QASM file
def update_qasm_file(input_path, output_path):
    # Read the original QASM file
    with open(input_path, 'r') as file:
        qasm_content = file.read()

    # Replace classical register definition and any occurrences of classical 'q' with 'c'
    updated_qasm_content = qasm_content.replace('creg q[', 'creg c[')

    # Save the updated QASM content to a new file
    with open(output_path, 'w') as file:
        file.write(updated_qasm_content)

# Define input and output file paths
input_qasm_path = 'BlueQubit-Hackathon/data/RAW/circuit_1_30q.qasm'
output_qasm_path = 'BlueQubit-Hackathon/data/processed/circuit_1_30q.qasm'

# Run the update function
update_qasm_file(input_qasm_path, output_qasm_path)
