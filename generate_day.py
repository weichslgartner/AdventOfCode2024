#!/usr/bin/env python3
import tomllib
from datetime import date
from enum import Enum
from pathlib import Path

from requests import get


class Language(str, Enum):
    Python = "Python"
    Haskell = "Haskell"
    Rust = "Rust"
    Cargo = "Cargo"


extension = {Language.Python: "py", Language.Haskell: "hs", Language.Rust: "rs", Language.Cargo: "toml"}

cookie = open(".cookie", 'r').readline().strip()
cookies = {'session': cookie}
year = 2024


def dumps(toml_dict, table=""):
    document = []
    for key, value in toml_dict.items():
        match value:
            case dict():
                table_key = f"{table}.{key}" if table else key
                document.append(
                    f"\n[{table_key}]\n{dumps(value, table=table_key)}"
                )
            case _:
                document.append(f"{key} = {_dumps_value(value)}")
    return "\n".join(document)


def _dumps_value(value):
    match value:
        case bool():
            return "true" if value else "false"
        case float() | int():
            return str(value)
        case str():
            return f'"{value}"'
        case date():
            return value.isoformat()
        case list():
            return f"[{', '.join(_dumps_value(v) for v in value)}]"
        case _:
            raise TypeError(
                f"{type(value).__name__} {value!r} is not supported"
            )


def python_stub(day: int) -> str:
    return f"""from aoc import get_lines


def parse_input(lines):
    return lines


def part_1(lines):
    pass


def part_2(lines):
    pass


def main():
    lines = get_lines("input_{day:02d}.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
"""


def rust_stub(day: int) -> str:
    return f"""fn part_1(input: &str) -> &str {{
    input
}}

fn part_2(input: &str) -> &str {{
    input
}}

fn main() {{
    let input = include_str!("../../../inputs/input_{day:02d}.txt");
    println!("Part 1: {{}}", part_1(&input));
    println!("Part 2: {{}}", part_2(&input));
}}

"""


def cargo_stub(day):
    return f"""[package]
name = "day_{day:02d}"
version = "0.1.0"
edition = "2021"
authors = ["weichslgartner <weichslgartner@gmail.com>"]

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]

"""


def haskell_stub(day: int) -> str:
    return f"""
main = do  
    contents <- readFile "../../inputs/input_{day:02d}.txt"
    print . map readInt . words $ contents
readInt :: String -> Int
readInt = read
    """


stubs = {
    Language.Python: python_stub,
    Language.Rust: rust_stub,
    Language.Cargo: cargo_stub,
    Language.Haskell: haskell_stub
}


def get_input(day: int):
    input_file = Path("inputs") / f"input_{day:02d}.txt"
    input_file.parent.mkdir(parents=True, exist_ok=True)
    if input_file.exists():
        return
    print(f"Fetching day {day}")
    raw_input = get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    with input_file.open('w') as f:
        f.writelines(raw_input.content.decode('utf-8'))


def generate_stub(day: int, lang: Language) -> None:
    source_file = generate_source_path(day, lang)
    source_file.parent.mkdir(parents=True, exist_ok=True)
    if source_file.exists():
        return
    print(f"Creating stub day {day} for {lang.name}")
    with source_file.open('w') as f:
        f.write(stubs[lang](day))


def generate_source_path(day: int, lang: Language) -> Path:
    if lang == Language.Rust:
        return Path(f"{lang.name}") / f"day_{day:02d}" / "src" / f"main.{extension[lang]}"
    if lang == Language.Cargo:
        return Path(f"{Language.Rust.name}") / f"day_{day:02d}" / f"Cargo.{extension[lang]}"
    return Path(f"{lang.name}") / f"day_{day:02d}.{extension[lang]}"


def main():
    today = date.today()
    print("Today is:", today)
    for day in range(1, 26):
        if today.year == year and (today.day < day or today.month != 12):
            break
        get_input(day)
        generate_stub(day, lang=Language.Python)
        generate_stub(day, lang=Language.Rust)
        generate_stub(day, lang=Language.Cargo)
        add_to_cargo_workspace(day)
    print("Done")


def add_to_cargo_workspace(day):
    cargo_file = Path(__file__).parent / "Rust" / "Cargo.toml"
    with cargo_file.open(mode="rb") as f:
        data = tomllib.load(f)
        data["workspace"]["members"].append(f"day_{day:02d}")
    with cargo_file.open(mode="w") as f:
        f.write(dumps(data))


if __name__ == '__main__':
    main()
