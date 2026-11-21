from rich.console import Console

console = Console()


def afficher_resultat(rep):
    if rep["ok"]:
        console.print(f"[green]✔ {rep['message']}[/green]")
    else:
        console.print(f"[red]✘ {rep['message']}[/red]")


def attendre():
    console.input("\n[dim]Entrée pour continuer...[/dim]")