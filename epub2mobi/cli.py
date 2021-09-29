import os
import enum
import time
import pathlib
from concurrent.futures import ThreadPoolExecutor

import click
from loguru import logger
from rich.console import Console

from .convert import is_epub, epub2mobi


console = Console(record=True)


@enum.unique
class Status(enum.Enum):
    PENDING = "[cyan][PENDING][/cyan]"
    RUNNING = "[purple][RUNNING][/purple]"
    SUCCESSFUL = "[green][DONE][/green]"
    WARNING = "[yellow][WARNING][/yellow]"
    ERROR = "[red][ERROR][/red]"

    def __str__(self):
        return self.value


class Task:

    def __init__(self, filename, index=0, status=Status.PENDING):
        self.filename = filename
        self.index = index
        self.status = status

    def __str__(self):
        return "  • [white]#{}[/white] [bold blue]{}[/bold blue] [bold]{}[/bold]".format(
            self.index,
            self.filename,
            self.status
        )

    def update(self, status):
        self.status = status


def convert_task(task, filepath, outputpath):
    task.update(Status.RUNNING)
    console.print(str(task))

    try:
        epub2mobi(filepath, outputpath=outputpath)

        task.update(Status.SUCCESSFUL)
        console.print(str(task))
    except Warning as ex:
        task.update(Status.WARNING)
        console.print(str(task))
    except Exception as ex:
        task.update(Status.ERROR)
        console.print(str(task))

        console.print("    {}: [red bold]{}[/red bold]".format(type(ex).__name__, ex))
        console.print()


def convert_file(inputpath, outputpath=None):
    console.print('[green]Convert [bold]{}[/bold] to mobi ...[/green]'.format(click.format_filename(inputpath, shorten=True)))
    console.print()

    epub2mobi(inputpath, outputpath=outputpath)


def convert_tree(inputpath, outputpath=None, max_workers=5):
    console.clear()
    console.print('[green]Convert all epub files from [bold]{}[/bold] to mobi ...[/green]'.format(click.format_filename(inputpath, shorten=True)))
    console.print()

    index = 0

    start = time.time()

    with ThreadPoolExecutor(max_workers=None) as pool:
        for root, _, files in os.walk(inputpath, topdown=False):
            for filename in files:
                filepath = pathlib.Path(root).joinpath(filename)

                if not is_epub(filepath):
                    continue

                index += 1
                task = Task(filename, index=index)

                mobipath = outputpath.joinpath(filename).with_suffix('.mobi') if outputpath else None
                pool.submit(convert_task, task, filepath, mobipath)

    end = time.time()
    console.print()
    console.print('Elapsed time: {} seconds'.format(end - start))
    console.print('[green]DONE.[/green]')
    console.print()


@click.command()
@click.argument('input', type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option('--debug', is_flag=True, help='Enable logging.')
@click.option('--output', type=click.Path(exists=False, file_okay=True, dir_okay=True), help='The output path.')
@click.option('--max-workers', type=int, default=4, help='The max number of worker threads to execute the task asynchronously.')
def cli(input, output, debug, max_workers):
    """Convert epub files to mobi.

    If INPUT is a directory it converts all the epub files in a directory tree to mobi.

    IF INPUT is an epub file it converts the file to mobi.
    """

    if not debug:
        logger.disable('epub2mobi')

    inputpath = pathlib.Path(input).absolute()
    outputpath = pathlib.Path(output) if output else None

    if inputpath.is_file():
        return convert_file(inputpath, outputpath=outputpath)

    if outputpath and outputpath.is_file():
        raise ValueError('Expecting a directory. Got: {}'.format(click.format_filename(outputpath, shorten=True)))

    return convert_tree(inputpath, outputpath=outputpath, max_workers=max_workers)


if __name__ == '__main__':
    cli()
