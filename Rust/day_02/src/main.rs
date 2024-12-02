use itertools::Itertools;

fn safe(diffs: &[i32]) -> bool {
    let all_positive = diffs.iter().all(|&x| x > 0);
    let all_negative = diffs.iter().all(|&x| x < 0);
    let in_range = diffs.iter().all(|&x| x.abs() > 0 && x.abs() <= 3);
    in_range && (all_positive || all_negative)
}

pub fn skip_nth<'a, I>(iter: I, n: usize) -> impl Iterator<Item = &'a i32>
where
    I: Iterator<Item = &'a i32>,
{
    iter.enumerate()
        .filter_map(move |(index, item)| if index == n { None } else { Some(item) })
}

fn adjacent_difference<'a, I>(level: I) -> Vec<i32>
where
    I: Iterator<Item = &'a i32>,
{
    level.tuple_windows().map(|(a, b)| b - a).collect()
}

fn damp(level: &[i32]) -> bool {
    (0..level.len()).any(|i| safe(&adjacent_difference(skip_nth(level.iter(), i))))
}

fn part_1(levels: &[Vec<i32>]) -> usize {
    levels
        .iter()
        .filter(|&level| safe(&adjacent_difference(level.iter())))
        .count()
}

fn part_2(levels: &[Vec<i32>]) -> usize {
    levels
        .iter()
        .filter(|&level| safe(&adjacent_difference(level.iter())) || damp(level))
        .count()
}

fn main() {
    let input = include_str!("../../../inputs/input_02.txt");
    let levels = aoc::parse_ints::<i32, ' '>(input).expect("Failed to parse input");
    println!("Part 1: {}", part_1(&levels));
    println!("Part 2: {}", part_2(&levels));
}
