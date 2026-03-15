from pathlib import Path

import requests

DATASETS = {
    "green_tripdata_2025-10.parquet": "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet",
}


def download_file(url: str, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists():
        print(f"Skipping {target_path.name} (already exists)")
        return

    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with target_path.open("wb") as out:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    out.write(chunk)
    print(f"Downloaded {target_path.name}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    raw_dir = base_dir / "data" / "raw"

    for filename, url in DATASETS.items():
        download_file(url, raw_dir / filename)

    print(f"All files are available in: {raw_dir}")

