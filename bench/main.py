import struct
import timeit
from typing import Callable, List, Tuple

from bytex.endianes import Endianes
from bytex.types import I8, U16, U8
from bytex import Structure
from construct import Int8sb, Struct, Byte, Int16ub

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)

STRUCT_FMT = ">BHb"

FormatConstruct = Struct(
    "a" / Byte,
    "b" / Int16ub,
    "c" / Int8sb,
)


class Format(Structure):
    a: U8
    b: U16
    c: I8


FAKE_DATA: bytes = Format(a=123, b=4567, c=-89).dump(endianes=Endianes.BIG)

BenchmarkFunc = Callable[[bytes], None]


def struct_parse(data: bytes) -> None:
    struct.unpack(STRUCT_FMT, data)


def bytex_parse(data: bytes) -> None:
    Format.parse(data, endianes=Endianes.BIG)


def construct_parse(data: bytes) -> None:
    FormatConstruct.parse(data)


def benchmark(
    name: str, func: BenchmarkFunc, data: bytes, iterations: int
) -> Tuple[str, float]:
    duration = timeit.timeit(lambda: func(data), number=iterations)
    return name, duration / iterations


def run_all_benchmarks(data: bytes, iterations: int) -> List[Tuple[str, float]]:
    results: List[Tuple[str, float]] = []
    console = Console()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Running benchmarks...", total=3)

        results.append(benchmark("struct", struct_parse, data, iterations))
        progress.advance(task)

        results.append(benchmark("bytex", bytex_parse, data, iterations))
        progress.advance(task)

        results.append(benchmark("construct", construct_parse, data, iterations))
        progress.advance(task)

    return results


def plot_single_parse_time(results: List[Tuple[str, float]]) -> None:
    console = Console()
    table = Table(
        title="Benchmark Results", show_edge=True, show_lines=True, expand=True
    )
    table.add_column("Library", justify="left", style="bold")
    table.add_column("Time per parse (s)", justify="left")
    table.add_column("Graph", justify="left")

    max_time = max(t for _, t in results)

    for name, time in results:
        bar_length = int(30 * (time / max_time))
        bar = "█" * bar_length
        table.add_row(name, f"{time:.2e}", bar)

    console.print("\n")
    console.print(table)
    console.print("\n")


def main() -> None:
    results = run_all_benchmarks(FAKE_DATA, iterations=1_000_000)
    plot_single_parse_time(results)


if __name__ == "__main__":
    main()
