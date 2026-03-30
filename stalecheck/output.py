import json
from pathlib import Path

from rich import box
from rich.console import Console
from rich.table import Table

from stalecheck.models import VersionSeverity, Package

console = Console()

SEVERITY_MAP = {
    VersionSeverity.ok: ("OK", "green"),
    VersionSeverity.minor: ("? minor", "yellow"),
    VersionSeverity.major: ("! major", "red"),
    VersionSeverity.ancient: ("X_X ancient", "bright_red"),
}


def print_table(results: list[Package]) -> None:
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")

    table.add_column("Package", style="bold")
    table.add_column("Installed", justify="center")
    table.add_column("Latest", justify="center")
    table.add_column("Severity", justify="center")

    for result in results:
        label, color = SEVERITY_MAP.get(result.severity, ("UNKNOWN", "dim"))
        table.add_row(
            result.name,
            result.installed if result.installed else "unknown",
            result.latest if result.latest else "unknown",
            f"[{color}]{label}[/{color}]",
        )

    console.print(table)
    _print_summary(results)


def _print_summary(results: list[Package]) -> None:
    counts = {
        VersionSeverity.ok: 0,
        VersionSeverity.minor: 0,
        VersionSeverity.major: 0,
        VersionSeverity.ancient: 0,
        "unknown": 0,
    }

    for r in results:
        counts[r.severity] += counts.get(r.severity, 0) + 1

    total = len(results)
    console.print(
        f"\n[dim]{total} packages checked · "
        f"[green]{counts[VersionSeverity.ok]} ok[/green] · "
        f"[yellow]{counts[VersionSeverity.minor]} minor[/yellow] · "
        f"[red]{counts[VersionSeverity.major]} major[/red] · "
        f"[bright_red]{counts[VersionSeverity.ancient]} ancient[/bright_red][/dim]"
    )


def export_json(results: list[Package], path: Path) -> None:
    data = [
        {
            "name": result.name,
            "installed": result.installed,
            "latest": result.latest,
            "severity": result.severity,
        }
        for result in results
    ]
    path.write_text(json.dumps(data, indent=2))
    console.print(f"[green]Results exported to {path}[/green]")
