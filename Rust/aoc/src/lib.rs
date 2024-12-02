use anyhow::Result;
use std::str::FromStr;

pub fn line_to_int<T: FromStr, const SPLIT_CHAR: char>(line: &str) -> Result<Vec<T>, T::Err> {
    line.split(SPLIT_CHAR)
        .filter(|i| !i.is_empty())
        .map(|i| i.parse::<T>())
        .collect()
}

pub fn parse_ints<T: FromStr, const SPLIT_CHAR: char>(input: &str) -> Result<Vec<Vec<T>>, T::Err> {
    input
        .lines()
        .map(|line| line_to_int::<T,SPLIT_CHAR>(line))
        .collect()
}
