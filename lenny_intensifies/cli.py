from pathlib import Path
import typer
from PIL import Image

from lenny_intensifies.lenny import generate_lenny_gif

app = typer.Typer()
@app.command()
def generate(face_file: Path, out_file: Path = Path('./out.gif'), colour: bool = True):
    face = Image.open(face_file)
    frames, duration = generate_lenny_gif(face, colour)
    frames[0].save(out_file, save_all=True, append_images=frames[1:], duration=duration)

if __name__ == '__main__':
    app()
