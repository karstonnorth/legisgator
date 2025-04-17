from rich.console import Console
from rich.table import Table

def render(result: dict) -> None:
    console = Console()
    c_tbl = Table(title="⚠️  Formal Contradictions")  # red flagged
    c_tbl.add_column("Premise A"), c_tbl.add_column("Premise B")
    for a, b in result["contradictions"]:
        c_tbl.add_row(a, b)
    console.print(c_tbl if c_tbl.row_count else "[green]No contradictions detected.[/]")
    w_tbl = Table(title="🩸  Weakest Clauses (bottom‑3)")
    w_tbl.add_column("ID"), w_tbl.add_column("Score"), w_tbl.add_column("Why")
    for w in result["weakest"]:
        w_tbl.add_row(w["id"], str(w["score"]), w["why"])
    console.print(w_tbl)
