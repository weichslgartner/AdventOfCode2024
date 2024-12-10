use aoc::{self, get_neighbours_4, Point};
use std::collections::{HashMap, HashSet};

fn parse_input(lines: Vec<&str>) -> (HashMap<Point, i32>, Vec<Point>, Point) {
    let mut points = HashMap::new();
    let mut starts = Vec::new();

    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let p = Point {
                x: x as isize,
                y: y as isize,
            };
            if c != '.' {
                points.insert(p, c.to_digit(10).unwrap() as i32);
            }
            if c == '0' {
                starts.push(p);
            }
        }
    }

    let p_max = Point {
        x: lines[0].len() as isize,
        y: lines.len() as isize,
    };

    (points, starts, p_max)
}

fn get_n_trailheads(p: Point, p_max: Point, points: &HashMap<Point, i32>) -> (usize, i32) {
    let mut cur = vec![p];
    let mut next_ps = Vec::new();
    let mut heads = HashSet::new();
    let mut score = 0;

    while !cur.is_empty() {
        for &p in &cur {
            for n in get_neighbours_4(p, p_max).into_iter().filter(|n| {
                points
                    .get(n)
                    .map_or(false, |&value| value - points[&p] == 1)
            }) {
                if let Some(&value) = points.get(&n) {
                    if value == 9 {
                        heads.insert(n);
                        score += 1;
                    } else {
                        next_ps.push(n);
                    }
                }
            }
        }
        cur = next_ps;
        next_ps = Vec::new();
    }

    (heads.len(), score)
}

fn solve(points: &HashMap<Point, i32>, starts: &Vec<Point>, p_max: Point) -> (usize, i32) {
    starts
        .iter()
        .map(|&p| get_n_trailheads(p, p_max, points))
        .fold((0, 0), |acc, (heads, score)| (acc.0 + heads, acc.1 + score))
}

fn main() {
    let input = include_str!("../../../inputs/input_10.txt");
    let lines: Vec<&str> = input.lines().collect();
    let (points, starts, p_max) = parse_input(lines);
    let (part1, part2) = solve(&points, &starts, p_max);
    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);
}
