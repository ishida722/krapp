from pathlib import Path

import typer

from krapp.config_manager import ConfigManager
from krapp.date_extractor import DateExtractor
from krapp.diary_organizer import DiaryOrganizer
from krapp.text_db_manager import TextDBManager
from krapp.txt2md import Txt2MdConverter
from krapp.yaml_frontmatter_parser import YamlFrontmatterParser

app = typer.Typer()
BASE_PATH_CONFIG = "texts.dir"


@app.command()
def txt2md(
    input_folder: str = typer.Option(
        help="Path to the input folder containing .txt files",
    ),
    output_folder: str = typer.Option(
        help="Path to the output folder for .md files",
    ),
):
    """
    Convert .txt files in the input folder to .md files in the output folder.
    """

    converter = Txt2MdConverter()
    result = converter.convert_txt_to_md(input_folder, output_folder)
    typer.echo(
        f"Converted {len(result.processed_files)} files from {input_folder} to {output_folder}."
    )


def _get_folder_path(folder_path: str, config_manager=None) -> Path:
    if config_manager is None:
        config_manager = ConfigManager()
    base_path = config_manager.get_config(BASE_PATH_CONFIG)
    if folder_path is not None:
        return Path(folder_path)
    base_path = config_manager.get_config(BASE_PATH_CONFIG)
    if base_path is None:
        raise Exception()
    return Path(base_path)


@app.command()
def create_db(
    db_path: str = typer.Option(
        help="Path to the SQLite database file", default="./texts.db"
    ),
    folder_path: str = typer.Option(
        help="Path to the folder containing .md files", default=None
    ),
):
    """
    Create a SQLite database from .md files in the specified folder.
    """
    date_extractor = DateExtractor()
    yaml_parser = YamlFrontmatterParser()
    db = TextDBManager(
        db_path=db_path,
        folder_path=_get_folder_path(folder_path),
        date_extractor=date_extractor,
        yaml_parser=yaml_parser,
    )
    # フォルダをスキャンしてDB構築
    db.process_folder()
    db.close()
    typer.echo(
        f"Database created at {db_path} from files in {_get_folder_path(folder_path)}."
    )


@app.command()
def run_app():
    """
    Run the Streamlit app.
    """
    import subprocess

    # Set the command line arguments for Streamlit
    # create_db(
    #     db_path=None,
    #     folder_path="/Users/ishida/Documents/Texts/",
    # )
    subprocess.run(
        ["streamlit", "run", "src/krapp/streamlit_app.py"],
        check=True,
    )


@app.command()
def set_config(key: str, value: str):
    """
    Set a configuration key-value pair.
    """
    cm = ConfigManager()
    cm.load_config()
    cm.set_config(key, value)
    cm.save_config()


@app.command()
def show_config():
    """
    Show the current configuration.
    """
    cm = ConfigManager()
    for key, value in cm.config.items():
        typer.echo(f"{key}: {value}")


@app.command()
def org_diary(
    input_folder: str = typer.Option(
        help="Path to the input folder containing .txt files",
    ),
    output_folder: str = typer.Option(
        help="Path to the output folder for .md files",
        default=None,
    ),
    remove: bool = typer.Option(
        help="Remove the original .md files after conversion",
        default=False,
    ),
):
    if output_folder is None:
        output_folder = input_folder

    organizer = DiaryOrganizer(date_extractor=DateExtractor())
    for file in Path(input_folder).rglob("*.md"):
        try:
            organizer.organize_diary(
                input_md_file=file, output_folder=output_folder, remove=remove
            )
        except ValueError:
            typer.echo(f"Failed to copy {file} to {output_folder}. ")
            continue
        typer.echo(f"Copy {file} to {output_folder}. ")


if __name__ == "__main__":
    app()
