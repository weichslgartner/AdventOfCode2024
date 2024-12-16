use std::collections::{BinaryHeap, HashSet, HashMap};
use std::cmp::Reverse;

use aoc::{Direction, Point};


fn parse_input(input: &str) -> (HashSet<Point>, Point, Point) {
    let mut walls = HashSet::new();
    let mut start = None;
    let mut end = None;

    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let point = Point {
                x: x as isize,
                y: y as isize,
            };
            match c {
                '#' => {
                    walls.insert(point);
                }
                'S' => start = Some(point),
                'E' => end = Some(point),
                _ => {}
            }
        }
    }

    (
        walls,
        start.expect("Start point not found"),
        end.expect("End point not found"),
    )
}

fn solve(
    walls: &HashSet<Point>,
    start: Point,
    end: Point,
) -> (isize, usize) {
    let mut queue = BinaryHeap::new();
    let mut costs: HashMap<(Point, Direction), isize> = HashMap::new();
    let mut tiles_best_paths = HashSet::new();

    queue.push(Reverse((0, Direction::East, vec![start])));

    for d in Direction::all() {
        costs.insert((end, d), isize::MAX);
    }

    while let Some(Reverse((cost, dir, path))) = queue.pop() {
        let point = *path.last().unwrap();

        if let Some(&current_cost) = costs.get(&(point, dir)) {
            if cost > current_cost {
                continue;
            }
        }

        if cost > Direction::all()
            .iter()
            .map(|&d| *costs.get(&(end, d)).unwrap_or(&isize::MAX))
            .min()
            .unwrap()
        {
            continue;
        }

        costs.insert((point, dir), cost);

        if point == end {
            let min_cost = Direction::all()
                .iter()
                .map(|&d| *costs.get(&(end, d)).unwrap())
                .min()
                .unwrap();

            if cost < min_cost {
                tiles_best_paths = path.iter().cloned().collect();
            } else if cost == min_cost {
                tiles_best_paths.extend(path.iter().cloned());
            }

            continue;
        }

        let p_delta = dir.to_point();
        let next_p = Point {
            x: point.x + p_delta.x,
            y: point.y + p_delta.y,
        };

        if !walls.contains(&next_p) {
            let mut next_path = path.clone();
            next_path.push(next_p);
            queue.push(Reverse((cost + 1, dir, next_path)));
        }

        for &new_dir in &[dir.rotate(true), dir.rotate(false)] {
            let p_delta = new_dir.to_point();
            let next_p = Point {
                x: point.x + p_delta.x,
                y: point.y + p_delta.y,
            };

            if !walls.contains(&next_p) {
                let mut next_path = path.clone();
                next_path.push(next_p);
                queue.push(Reverse((cost + 1001, new_dir, next_path)));
            }
        }
    }

    let min_path = Direction::all()
        .iter()
        .map(|&d| *costs.get(&(end, d)).unwrap())
        .min()
        .unwrap();

    (min_path, tiles_best_paths.len())
}



fn main() {
    let input = include_str!("../../../inputs/input_16.txt");


    let (walls, start, end) = parse_input(input);
    let (part1, part2) = solve(&walls, start, end);

    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);
}



