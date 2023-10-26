import os
import sys
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

mod_path = Path(__file__).parent
output_relative_path = '../output'
output_file_path = (mod_path / output_relative_path).resolve()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_all_files(root: Path):
    for item in root.iterdir():
        yield item
        if item.is_dir():
            yield from get_all_files(item)

def upload_files():
    files = get_all_files(output_file_path)
    index = 1

    for fl in files:
        file_name = str(fl).partition('output\\')[2]
        if fl.is_file():
            file_name = file_name.replace('\\', '/')
            print(f"{index}: Uploading {file_name}")
            index += 1
            try:
                with open(str(fl), 'rb') as f:
                    supabase.storage.from_("wp-content").upload(file=f, path=file_name)
            except Exception as er:
                print(f"Error uploading {file_name}, Error: {er}")

upload_files()
