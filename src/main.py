import argparse
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from integrity_checker import IntegrityChecker

__version__ = "1.0.0"

def main():
    console = Console()
    console.print(Panel(f"[bold cyan]🛡️ HexGuard Security — v{__version__}[/bold cyan]", expand=False))
    
    parser = argparse.ArgumentParser(description="🛡️ HexGuard — File Integrity Monitor (FIM)")
    parser.add_argument("--init", help="Initialize or update baseline for a directory", metavar="DIR")
    parser.add_argument("--check", help="Scan directory against saved baseline", metavar="DIR")
    parser.add_argument("--baseline", help="Custom baseline file path", default="baseline.json")
    parser.add_argument("--ignore", help="Custom ignore file path", default=".fim-ignore")
    
    args = parser.parse_args()
    
    if args.init:
        if not os.path.isdir(args.init):
            console.print(f"[bold red][-] Error: {args.init} is not a directory.[/bold red]")
            sys.exit(1)
        checker = IntegrityChecker(args.init, ignore_file=args.ignore)
        checker.generate_baseline(args.baseline)
    elif args.check:
        if not os.path.isdir(args.check):
            console.print(f"[bold red][-] Error: {args.check} is not a directory.[/bold red]")
            sys.exit(1)
        
        checker = IntegrityChecker(args.check, ignore_file=args.ignore)
        results = checker.verify_integrity(args.baseline)
        
        if results is None:
            return

        table = Table(title="🔍 INTEGRITY SCAN RESULTS", header_style="bold magenta")
        table.add_column("Status", style="bold")
        table.add_column("Filename", style="dim")
        
        if not any(results.values()):
            console.print("[bold green]✅ No integrity violations detected. Files are consistent.[/bold green]")
        else:
            for f in results["modified"]: table.add_row("⚠️ MODIFIED", f, style="yellow")
            for f in results["deleted"]:  table.add_row("❌ DELETED", f, style="red")
            for f in results["new"]:      table.add_row("🆕 NEW", f, style="green")
            console.print(table)
            
        console.print("[dim italic]Audit logs updated in hexguard.log[/dim italic]\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
