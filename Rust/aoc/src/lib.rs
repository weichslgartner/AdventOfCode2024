use anyhow::Result;
use std::str::FromStr;

pub fn line_to_int<T: FromStr>(line: &str, split_char: char) -> Result<Vec<T>, T::Err> {
    line.split(split_char)
        .filter(|i| !i.is_empty())
        .map(|i| i.parse::<T>())
        .collect()
}

pub fn parse_ints<T: FromStr>(input: &str, split_char: char) -> Result<Vec<Vec<T>>, T::Err> {
    input
        .lines()
        .map(|line| line_to_int(line, split_char))
        .collect()
}
