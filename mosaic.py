"""Image mosaic generation utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable

from PIL import Image, ImageStat

BASE_DIR = Path(__file__).resolve().parent
static_path = BASE_DIR / "sourceimgs2"
real_path = BASE_DIR / "sourceimgs1"
DEFAULT_OUTPUT = BASE_DIR / "finalproduct.jpg"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
ProgressCallback = Callable[[int, int], None]


def color_distance(color1: Iterable[float], color2: Iterable[float]) -> float:
    """Return Euclidean distance between two RGB colors."""
    values1 = tuple(color1)
    values2 = tuple(color2)
    if len(values1) < 3 or len(values2) < 3:
        raise ValueError("Colors must contain at least three channels.")
    return sum((values1[index] - values2[index]) ** 2 for index in range(3)) ** 0.5


def _image_paths(source_directory: Path) -> list[Path]:
    if not source_directory.is_dir():
        raise FileNotFoundError(f"Source image directory does not exist: {source_directory}")
    return sorted(
        path
        for path in source_directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def _average_color(image: Image.Image) -> tuple[float, float, float]:
    statistics = ImageStat.Stat(image.convert("RGB").resize((1, 1)))
    return tuple(statistics.mean[:3])


def generate(
    tgtpath: str | Path,
    rows: int,
    cols: int,
    srcpath: str | Path,
    output_path: str | Path = DEFAULT_OUTPUT,
    progress_callback: ProgressCallback | None = None,
) -> Path:
    """Create a photo mosaic and return the path to the generated image."""
    if rows < 1 or cols < 1:
        raise ValueError("Rows and columns must both be greater than zero.")

    target_path = Path(tgtpath)
    source_directory = Path(srcpath)
    output = Path(output_path)
    if not target_path.is_file():
        raise FileNotFoundError(f"Target image does not exist: {target_path}")

    source_paths = _image_paths(source_directory)
    if not source_paths:
        raise ValueError(f"No supported images found in {source_directory}")

    with Image.open(target_path) as target_file:
        target = target_file.convert("RGB")
    source_images: list[Image.Image] = []
    try:
        for path in source_paths:
            with Image.open(path) as source_file:
                source_images.append(source_file.convert("RGB").copy())

        source_averages = [_average_color(image) for image in source_images]
        product = Image.new("RGB", target.size)
        total_cells = rows * cols
        completed_cells = 0

        for row in range(rows):
            top = target.height * row // rows
            bottom = target.height * (row + 1) // rows
            for col in range(cols):
                left = target.width * col // cols
                right = target.width * (col + 1) // cols
                box = (left, top, right, bottom)
                cell = target.crop(box)
                cell_average = _average_color(cell)
                closest_index = min(
                    range(len(source_averages)),
                    key=lambda index: color_distance(cell_average, source_averages[index]),
                )
                tile = source_images[closest_index].resize(
                    (right - left, bottom - top), Image.Resampling.LANCZOS
                )
                product.paste(tile, box)
                completed_cells += 1
                if progress_callback is not None:
                    progress_callback(completed_cells, total_cells)

        output.parent.mkdir(parents=True, exist_ok=True)
        product.save(output, format="JPEG", quality=95)
        return output
    finally:
        for image in source_images:
            image.close()


def _run_cli() -> None:
    print("Welcome to the image mosaic generator.")
    try:
        rows = int(input("How many rows do you want in the product image? "))
        cols = int(input("How many columns do you want in the product image? "))
        response = input("Choose a target image (1, 2, 3, or 4; Q to quit): ").strip().lower()
        if response == "q":
            return
        if response not in {"1", "2", "3", "4"}:
            raise ValueError("Target must be 1, 2, 3, or 4.")
        result = generate(BASE_DIR / f"target{response}.jpg", rows, cols, static_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"Unable to generate mosaic: {error}")
        return
    print(f"Mosaic saved to {result}")


if __name__ == "__main__":
    _run_cli()
