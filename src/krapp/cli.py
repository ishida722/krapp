import typer

app = typer.Typer()


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
    from krapp.txt2md import Txt2MdConverter

    converter = Txt2MdConverter()
    result = converter.convert_txt_to_md(input_folder, output_folder)
    typer.echo(
        f"Converted {len(result.processed_files)} files from {input_folder} to {output_folder}."
    )


@app.command()
def create_db(
    db_path: str = typer.Option(
        help="Path to the SQLite database file",
    ),
    folder_path: str = typer.Option(
        help="Path to the folder containing .md files",
    ),
):
    """
    Create a SQLite database from .md files in the specified folder.
    """
    from krapp.date_extractor import DateExtractor
    from krapp.text_db_manager import TextDBManager

    date_extractor = DateExtractor()
    db = TextDBManager(
        db_path=db_path, folder_path=folder_path, date_extractor=date_extractor
    )
    db.process_folder()
    db.close()
    typer.echo(f"Database created at {db_path} from files in {folder_path}.")


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


if __name__ == "__main__":
    app()
