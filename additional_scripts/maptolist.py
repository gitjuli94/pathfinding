
# Input and output files
input_file_path = 'additional_scripts/Moscow_0_256.map'
output_file_path = 'additional_scripts/output.txt'


def process_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as input_file:
            lines = input_file.readlines()

        result_array = []
        for line in lines:
            # Process the line to remove spaces and convert characters
            result_line = []
            for char in line:
                if char not in [" ", "\n"]:
                    if char == '.':
                        result_line.append("0")
                    elif char == '@':
                        result_line.append("1")
            result_array.append(result_line)

        # Write the processed map to the output file
        with open(output_file_path, 'w') as output_file:
            for line in result_array:
                output_file.write("[" + ",".join(line) + "]," + "\n")

        print(f"Map Processed, array written to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: File not found - {input_file_path}")
    except Exception as e:
        print(f"Error: {e}")


process_file(input_file_path, output_file_path)
