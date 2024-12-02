
fn safe(diffs: &[i32]) -> bool {
    let all_positive = diffs.iter().all(|&x| x > 0);
    let all_negative = diffs.iter().all(|&x| x < 0);
    let in_range = diffs.iter().all(|&x| x.abs() > 0 && x.abs() <= 3);
    in_range && (all_positive || all_negative)
}

fn adjacent_difference(level: &[i32]) -> Vec<i32> {
    level.windows(2).map(|w| w[0] - w[1]).collect()
}

fn damp(level: &[i32]) -> bool {
    (0..level.len()).any(|i| {
        let mut reduced = level.to_vec();
        reduced.remove(i);
        safe(&adjacent_difference(&reduced))
    })
}

fn part_1(levels: &[Vec<i32>]) -> usize {
    levels.iter().filter(|&level| safe(&adjacent_difference(level))).count()
}

fn part_2(levels: &[Vec<i32>]) -> usize {
    levels.iter().filter(|&level| safe(&adjacent_difference(level)) || damp(level)).count()
}

fn main() {
    let input = include_str!("../../../inputs/input_02.txt");
    let lines: Vec<String> = input.lines().map(String::from).collect();
    let levels = aoc::parse_ints::<i32>(&lines, ' ').expect("Failed to parse input");

    println!("Part 1: {}", part_1(&levels));
    println!("Part 2: {}", part_2(&levels));
}
