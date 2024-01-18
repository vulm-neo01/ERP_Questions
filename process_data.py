import csv

def process_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        header = reader.fieldnames
        header.append('correct_answer')

        rows = []
        for row in reader:
            correct_answers = [option for option in ['A', 'B', 'C', 'D'] if 'x' in row[option].lower()]
            row['correct_answer'] = ', '.join(correct_answers)

            # Loại bỏ dấu ngoặc vuông và chữ "x" từ các đáp án
            for option in ['A', 'B', 'C', 'D']:
                row[option] = row[option].replace('[', '').replace(']', '').lstrip('x').lstrip().rstrip()

            rows.append(row)

    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

# Thực hiện xử lý và ghi vào file mới
process_data('data.csv', 'processed_data.csv')
