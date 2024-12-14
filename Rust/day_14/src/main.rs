use std::collections::HashMap;

use aoc::extract_all_ints;
use aoc::Point;

const WIDTH: isize = 101;
const HEIGHT: isize = 103;

fn parse_input(input: &str) -> Vec<(Point, Point)> {
    input
        .lines()
        .map(|line| {
            let nums: Vec<isize> = extract_all_ints(line);
            (
                Point {
                    x: nums[0],
                    y: nums[1],
                },
                Point {
                    x: nums[2],
                    y: nums[3],
                },
            )
        })
        .collect()
}

fn part_1(mut points: Vec<(Point, Point)>, steps: isize) -> isize {
    perform_movement(&mut points, steps);
    calc_quads(&points).iter().product()
}

fn perform_movement(points: &mut [(Point, Point)], steps: isize) {
    for (pos, vel) in points.iter_mut() {
        pos.x = (pos.x + vel.x * steps).rem_euclid(WIDTH);
        pos.y = (pos.y + vel.y * steps).rem_euclid(HEIGHT);
    }
}

fn is_christmas_tree(points: &[(Point, Point)]) -> bool {
    let mut counter = HashMap::new();
    for (pos, _) in points {
        *counter.entry(*pos).or_insert(0) += 1;
    }
    counter.values().all(|&v| v == 1)
}

fn calc_quads(points: &[(Point, Point)]) -> [isize; 4] {
    let mut quads = [0; 4];
    for (p, _) in points {
        match (
            p.y < HEIGHT / 2,
            p.y > HEIGHT / 2,
            p.x < WIDTH / 2,
            p.x > WIDTH / 2,
        ) {
            (true, _, true, _) => quads[0] += 1, // Top-left
            (true, _, _, true) => quads[1] += 1, // Top-right
            (_, true, true, _) => quads[2] += 1, // Bottom-left
            (_, true, _, true) => quads[3] += 1, // Bottom-right
            _ => (),                             // Ignore points on boundaries
        }
    }
    quads
}

fn part_2(mut points: Vec<(Point, Point)>) -> isize {
    for i in 0..1_000_000 {
        if is_christmas_tree(&points) {
            return i;
        }
        perform_movement(&mut points, 1);
    }
    -1
}

fn main() {
    let input: &str = include_str!("../../../inputs/input_14.txt");
    let points = parse_input(input);
    println!("Part 1: {}", part_1(points.clone(), 100));
    println!("Part 2: {}", part_2(points));
}
