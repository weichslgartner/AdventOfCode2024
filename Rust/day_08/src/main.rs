use aoc::{is_in_grid, Point};
use itertools::Itertools;
use std::collections::{HashMap, HashSet};

fn parse_input(input: &str) -> (HashMap<char, HashSet<Point>>, Point) {
    let mut max_y: isize = 0;
    let mut max_x: isize = 0;
    let antennas: HashMap<char, HashSet<Point>> = input
        .lines()
        .enumerate()
        .fold(HashMap::new(), |mut acc, (y, line)| {
            line.chars().enumerate().for_each(|(x, c)| {
                max_x = max_x.max(x as isize);
                max_y = max_y.max(y as isize);
                if !("#.".contains(c)) {
                    acc.entry(c)
                        .or_default()
                        .insert(Point::new(x as isize, y as isize));
                }
            });
            acc
        });
    (antennas, Point::new(max_x + 1, max_y + 1))
}

fn find_antinodes(p1: Point, p2: Point, p_max: Point, part2: bool) -> HashSet<Point> {
    let mut antinodes = if part2 {
        HashSet::from([p1, p2])
    } else {
        HashSet::new()
    };

    for &(start, dx, dy) in &[
        (p1, p1.x - p2.x, p1.y - p2.y),
        (p2, p2.x - p1.x, p2.y - p1.y),
    ] {
        let mut r = Point::new(start.x + dx, start.y + dy);
        while is_in_grid(r, p_max) {
            antinodes.insert(r);
            if !part2 {
                break;
            }
            r = Point::new(r.x + dx, r.y + dy);
        }
    }

    antinodes
}

fn solve(antennas: &HashMap<char, HashSet<Point>>, max_p: Point, part2: bool) -> usize {
    antennas
        .values()
        .map(|locs| {
            locs.iter()
                .combinations(2)
                .map(|pair| find_antinodes(*pair[0], *pair[1], max_p, part2))
                .fold(HashSet::new(), |acc, set| &acc | &set)
        })
        .fold(HashSet::new(), |acc, set| &acc | &set)
        .len()
}

fn part_1(antennas: &HashMap<char, HashSet<Point>>, p_max: Point) -> usize {
    solve(antennas, p_max, false)
}

fn part_2(antennas: &HashMap<char, HashSet<Point>>, p_max: Point) -> usize {
    solve(antennas, p_max, true)
}

fn main() {
    let input = include_str!("../../../inputs/input_08.txt");
    let (antennas, p_max) = parse_input(input);
    println!("Part 1: {}", part_1(&antennas, p_max));
    println!("Part 2: {}", part_2(&antennas, p_max));
}
