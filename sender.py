import glob
import requests
import os
import sys
import shutil
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import (Progress, SpinnerColumn, BarColumn, TextColumn,
                           TimeRemainingColumn, TransferSpeedColumn)
from time import sleep

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class ProgressFile:
    def __init__(self, filename, progress, task_id):
        self._file = open(filename, 'rb')
        self.filename = filename
        self.filesize = os.path.getsize(filename)
        self.progress = progress
        self.task_id = task_id
        self._read_bytes = 0

    def read(self, chunk_size=-1):
        data = self._file.read(chunk_size)
        if not data:
            return data
        self._read_bytes += len(data)
        self.progress.update(self.task_id, completed=self._read_bytes)
        return data

    def __getattr__(self, attr):
        return getattr(self._file, attr)

    def __del__(self):
        if not self._file.closed:
            self._file.close()

def send_file(bot_token, chat_id, filename):
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'

    try:
        file_size = os.path.getsize(filename)
        console.print(f"[green]File size: {file_size / (1024 * 1024):.2f} MB[/green]")
        
        def build_multipart_data(file_obj):
            """Builds the multipart data for the request."""
            return {
                'document': (os.path.basename(filename), file_obj),
                'chat_id': (None, chat_id),
            }

        progress = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            TransferSpeedColumn(),
            "•",
            TextColumn("{task.completed}/{task.total} bytes"),
            console=console,
        )

        with progress:
            task_id = progress.add_task("[cyan]Uploading...", total=file_size)
            progress_file = ProgressFile(filename, progress, task_id)

            multipart_data = build_multipart_data(progress_file)

            response = requests.post(url, files=multipart_data)

        if response.ok:
            console.print("[bold green]\nFile sent successfully![/bold green]")
        else:
            console.print(f"[bold red]\nFailed to send file. Error: {response.text}[/bold red]")

    except FileNotFoundError:
        console.print(f'[bold red]File "{filename}" not found.[/bold red]')
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def main():
    clear_screen()
    console.print("[bold cyan]Welcome to the Advanced Telegram File Sender[/bold cyan]\n")

    try:
        bot_token = Prompt.ask("[bold yellow]Enter your Telegram Bot Token[/bold yellow]").strip()
        chat_id = Prompt.ask("[bold yellow]Enter the Chat ID to send the file to[/bold yellow]").strip()
    except KeyboardInterrupt:
        console.print("\n[bold red]Operation cancelled by user. Exiting...[/bold red]")
        sys.exit()

    while True:
        try:
            filename = Prompt.ask("\n[bold yellow]Enter the file or folder name (use *.ext for bulk send):[/bold yellow]").strip()
            if not filename:
                console.print("[bold red]File name cannot be empty. Please try again.[/bold red]")
                continue

            if filename.startswith("*"):
                # Advanced pattern match
                extension = filename.replace("*", "").strip()
                if not extension:
                    console.print("[bold red]Invalid pattern provided. Example: *.txt[/bold red]")
                    continue

                files_to_send = glob.glob(f"*{extension}")
                if not files_to_send:
                    console.print(f"[bold red]No files with extension '{extension}' found in the current directory.[/bold red]")
                    continue

                console.print(f"[bold green]Found {len(files_to_send)} file(s) to send:[/bold green] {', '.join(files_to_send)}")
                for file_path in files_to_send:
                    send_file(bot_token, chat_id, file_path)
                    sleep(1)  # Optional small delay between sends

            else:
                zip_created = False

                if os.path.isdir(filename):
                    zip_basename = os.path.basename(filename.rstrip(os.sep))
                    zip_file = zip_basename + '.zip'
                    zip_filepath = os.path.abspath(zip_file)
                    console.print(f"[blue]Zipping directory '{filename}' into '{zip_file}'...[/blue]")
                    try:
                        shutil.make_archive(zip_basename, 'zip', filename)
                        zip_created = True
                        filename = zip_filepath
                    except Exception as e:
                        console.print(f"[bold red]Failed to zip directory: {e}[/bold red]")
                        continue
                elif not os.path.isfile(filename):
                    console.print(f'[bold red]The file or directory "{filename}" does not exist.[/bold red]')
                    continue
                else:
                    console.print(f"[blue]Processing '{filename}'...[/blue]")
                    sleep(1)

                send_file(bot_token, chat_id, filename)

                if zip_created:
                    try:
                        os.remove(filename)
                        console.print(f"[green]Deleted temporary zip file '{filename}'.[/green]")
                    except Exception as e:
                        console.print(f"[bold red]Failed to delete temporary zip file: {e}[/bold red]")

            choice = Prompt.ask(
                "\n[bold magenta]Do you want to send another file or folder?[/bold magenta] [bold yellow](y/n)[/bold yellow]",
                default="n"
            ).strip().lower()

            if choice != 'y':
                console.print("\n[bold cyan]:) Have a nice day and see you later![/bold cyan]")
                break

        except KeyboardInterrupt:
            console.print("\n[bold cyan]:) Have a nice day and see you later![/bold cyan]")
            sys.exit()


if __name__ == "__main__":
    main()
