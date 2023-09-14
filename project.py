#!/usr/bin/env python3

import json
import subprocess
import tempfile
import typer
from logger import logger
from rich import print
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from typer import prompt
from typing_extensions import Annotated

app = typer.Typer()
console = Console()


def main():
    app()


@app.command()
def show_all(snippets_file: Annotated[typer.FileText, typer.Argument()]):
    """
    Show a table indexing all of the snippets in a json formatted snippets file
    """
    snippets = load_snippets(snippets_file)

    table = Table(
        "Name", "Prefix", "Description", title=f"Snippets from {snippets_file.name}"
    )

    for snippet, details in snippets.items():
        name = snippet
        prefix = details.get("prefix")
        desc = details.get("description")

        table.add_row(name, prefix, Text(desc, no_wrap=True, overflow="ellipsis"))

    table = Padding(table, (2, 4))
    console.print(table)


@app.command()
def show(
    snippets_file: Annotated[typer.FileText, typer.Argument()],
    prefix: Annotated[str, typer.Argument()],
):
    """
    Show the body of a snippet
    """
    snippets = load_snippets(snippets_file)

    for snippet, details in snippets.items():
        if details.get("prefix") == prefix:
            if isinstance(details["body"], str):
                syntax = Syntax(details["body"], "python")
            elif isinstance(details["body"], list):
                syntax = Syntax("\n".join(details["body"]), "python")
            else:
                raise ValueError

            print()
            console.print(Panel.fit(syntax, title=f"{snippet}\tTrigger: {prefix}"))
            print()


@app.command()
def new(snippets_file: Annotated[typer.FileText, typer.Argument()]):
    """
    Add a snippet to the file
    """
    snippets = load_snippets(snippets_file)

    name = prompt("Snippet's name")
    prefix = prompt("Prefix/trigger")
    desc = prompt("Description")
    body = []
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        subprocess.call(["nvim", temp.name])
        temp.seek(0)
        body = temp.read()
    snippets[name] = {"prefix": prefix, "body": body, "description": desc}

    with open(snippets_file.name, "w") as f:
        json.dump(snippets, f, indent=4)


@app.command()
def edit(
    snippets_file: Annotated[typer.FileText, typer.Argument()],
    prefix: Annotated[str, typer.Argument()],
):
    """
    Edit the body of a snippet
    """
    snippets = load_snippets(snippets_file)

    for _, details in snippets.items():
        if details.get("prefix") == prefix:
            with tempfile.NamedTemporaryFile(mode="w+") as temp:
                temp.write(details["body"])
                temp.flush()
                subprocess.call(["nvim", temp.name])
                temp.seek(0)
                details["body"] = temp.read().rstrip()

    with open(snippets_file.name, "w") as f:
        json.dump(snippets, f, indent=4)


def load_snippets(snippets_file):
    """
    Open a snippets file and handle some errors, returning usable json
    """
    try:
        snippets = json.load(snippets_file)
    except json.JSONDecodeError as e:
        logger.error(f"{snippets_file.name} is not valid JSON:\n{e}")
        raise typer.Abort()

    checked = {}

    # TODO: group these errors together into a panel and have the user acknowledge them before continuing
    for snippet, details in snippets.items():
        if "prefix" not in details.keys():
            logger.warning(
                f"Prefix missing from '{snippet}' in {snippets_file.name}. Skipping for now."
            )
        elif "body" not in details.keys():
            logger.warning(
                f"Body missing from '{snippet}' in {snippets_file.name}. Skipping for now."
            )
        elif "description" not in details.keys():
            logger.warning(
                f"Description missing from '{snippet}' in {snippets_file.name}. Skipping for now."
            )
        else:
            checked[snippet] = details

    # if len(checked) < len(snippets):
    #     ...

    return checked


if __name__ == "__main__":
    main()
