import csv

def read_csv_to_tuples(path: str) -> list[tuple]:
    with open(path, newline='', encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            rows.append((int(row['userId']), int(row['id']), row['title'], row['body']))
    return rows