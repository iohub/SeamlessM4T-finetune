
import sys
import json


in_filename = sys.argv[1]
max_length = int(sys.argv[2])

valid_lines = []

with open(in_filename, 'r') as file:
    for line in file:
        try:
            data = json.loads(line.strip())
            if len(data['target']['units']) < max_length:
                valid_lines.append(line)
            else:
                print('drop sample')
        except Exception as e:
            print(e)


with open(in_filename, 'w') as file:
    for line in valid_lines:
        file.write(line)
