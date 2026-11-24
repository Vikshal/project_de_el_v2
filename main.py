from pathlib import Path
from extract import extract, save_to_csv
from read_csv import read_csv_to_tuples
from load_to_db import load

csv_path = Path(__file__).resolve().parent / "extract_to_csv.csv"
URL = 'https://jsonplaceholder.typicode.com/posts'

def main_launch() -> None:
    df = extract(URL)

    save_to_csv(df, str(csv_path))

    values = read_csv_to_tuples(str(csv_path))
    print(f"Прочитано строк из CSV: {len(values)}")

    load(values)

if __name__ == '__main__':
    main_launch()