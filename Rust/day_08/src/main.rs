use itertools::Itertools;
use std::collections::{HashMap, HashSet};
use aoc::{Point,is_in_grid};

fn parse_input(input: &str) -> (HashMap<char, HashSet<Point>>, Point) {
    let mut antennas: HashMap<char, HashSet<Point>> = HashMap::new();
    let mut max_y = 0;
    let mut max_x = 0;

    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                continue;
            }
            if c != '.' {
                antennas
                    .entry(c)
                    .or_default()
                    .insert(Point::new(x, y));
            }
            max_x = max_x.max(x);
        }
        max_y = max_y.max(y);
    }

    (antennas, Point::new(max_x + 1, max_y + 1))
}

fn find_antinodes(p1: Point, p2: Point, p_max: Point, part2: bool) -> HashSet<Point> {
    let mut antinodes = if part2 {
        HashSet::from([p1, p2])
    } else {
        HashSet::new()
    };

    for &(start, dx, dy) in &[
        (
            p1,
            p1.x as isize - p2.x as isize,
            p1.y as isize - p2.y as isize,
        ),
        (
            p2,
            p2.x as isize - p1.x as isize,
            p2.y as isize - p1.y as isize,
        ),
    ] {
        let mut r = Point::new(
            (start.x as isize + dx) as usize,
            (start.y as isize + dy) as usize,
        );
        while is_in_grid(r, p_max) {
            antinodes.insert(r);
            if !part2 {
                break;
            }
            r = Point::new((r.x as isize + dx) as usize, (r.y as isize + dy) as usize);
        }
    }

    antinodes
}

fn solve(antennas: &HashMap<char, HashSet<Point>>, max_p: Point, part2: bool) -> usize {
    antennas
        .values()
        .flat_map(|locs| {
            locs.iter()
                .combinations(2)
                .map(|pair| find_antinodes(*pair[0], *pair[1], max_p, part2))
                .fold(HashSet::new(), |acc, set| &acc | &set)
        })
        .fold(HashSet::new(), |mut acc, p| {
            acc.insert(p);
            acc
        })
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
