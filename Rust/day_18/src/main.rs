use std::collections::{BinaryHeap, HashSet, HashMap};
use std::cmp::Reverse;

use aoc::{get_neighbours_4, Point};



fn parse_input(input: &str) -> Vec<Point> {
    input.lines()
        
        .map(|line| {
            let (x,y) = line.split_once(',').unwrap();
            Point::new(x.parse().unwrap(), y.parse().unwrap())
        })
        .collect()
}

fn find_min_path(n_nbytes: usize, points: &[Point], target: Point) -> Option<isize> {
    let p_max = Point::new(target.x + 1, target.y + 1);
    let walls: HashSet<Point> = points.iter().cloned().take(n_nbytes).collect();
    let mut queue = BinaryHeap::new();
    queue.push((Reverse(0), Point::new(0, 0)));

    let mut costs_dict: HashMap<Point, isize> = HashMap::new();
    costs_dict.insert(Point::new(0, 0), isize::MAX);

    while let Some((Reverse(cost), point)) = queue.pop() {
        if cost >= *costs_dict.get(&point).unwrap_or(&isize::MAX) {
            continue;
        }
        costs_dict.insert(point, cost);

        if point == target {
            return Some(cost);
        }

        for neighbor in get_neighbours_4(point, p_max) {
            if !walls.contains(&neighbor) {
                queue.push((Reverse(cost + 1), neighbor));
            }
        }
    }

    None
}

fn binary_search(
    mut left: usize,
    mut right: usize,
    points: &[Point],
    target: Point,
) -> (Option<usize>, Option<isize>) {
    let mut m = None;
    let mut res = None;

    while left <= right {
        m = Some((left + right) / 2);
        res = find_min_path(m.unwrap(), points, target);

        if res.is_some() {
            left = m.unwrap() + 1;
        } else {
            right = m.unwrap() - 1;
        }
    }

    (m, res)
}

fn part_1(points: &[Point], target: Point, n_nbytes: usize) -> isize {
    find_min_path(n_nbytes, points, target).unwrap_or(-1)
}

fn part_2(points: &[Point], target: Point, start_byte: usize) -> String {
    let (i, res) = binary_search(start_byte, points.len(), points, target);

    if let Some(idx) = i {
        if res.is_none() {
            format!("{},{}", points[idx - 1].x, points[idx - 1].y)
        } else {
            format!("{},{}", points[idx].x, points[idx].y)
        }
    } else {
        String::new()
    }
}

fn main() {
    let input = include_str!("../../../inputs/input_18.txt");
    let points = parse_input(input);

    println!("Part 1: {}", part_1(&points, Point::new(70, 70), 1024));
    println!("Part 2: {}", part_2(&points, Point::new(70, 70), 1024));
}

