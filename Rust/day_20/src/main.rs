use std::collections::{HashMap, HashSet};

use aoc::{get_neighbours_4, is_in_grid, Point};
use rayon::iter::{IndexedParallelIterator, IntoParallelRefIterator, ParallelIterator};

type Walls = HashSet<Point>;

type Costs = HashMap<Point, isize>;

type Path = Vec<Point>;

fn parse_input(input: &str) -> (Walls, Point, Point) {
    let mut walls = HashSet::new();
    let mut start = None;
    let mut end = None;

    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let p = Point {
                x: x as isize,
                y: y as isize,
            };
            match c {
                '#' => {
                    walls.insert(p);
                }
                'S' => {
                    start = Some(p);
                }
                'E' => {
                    end = Some(p);
                }
                _ => {}
            }
        }
    }

    (walls, start.unwrap(), end.unwrap())
}

fn calc_costs(end: &Point, start: &Point, walls: &Walls, p_max: &Point) -> (Costs, Path) {
    let mut stack = vec![(0, *start)];
    let mut costs_dict = HashMap::new();
    let mut path = vec![*start];

    while let Some((cost, point)) = stack.pop() {
        costs_dict.insert(point, cost);
        if point == *end {
            return (costs_dict, path);
        }

        for n in get_neighbours_4(point, *p_max)
            .iter()
            .filter(|n| !walls.contains(n) && !costs_dict.contains_key(n))
        {
            stack.push((cost + 1, *n));
            path.push(*n);
        }
    }

    (costs_dict, path)
}

fn get_cheat_destinations(
    p: &Point,
    p_max: &Point,
    walls: &Walls,
    costs_dict: &Costs,
    save_at_least: isize,
    max_dist: isize,
) -> HashSet<Point> {
    let mut point_set = HashSet::new();

    for y in -max_dist..=max_dist {
        for x in -max_dist..=max_dist {
            let n = Point {
                x: p.x + x,
                y: p.y + y,
            };
            if is_in_grid(n, *p_max) && !walls.contains(&n) && p.manhattan_distance(&n) <= max_dist
            {
                if let Some(&n_cost) = costs_dict.get(&n) {
                    if n_cost >= costs_dict[p] + p.manhattan_distance(&n) + save_at_least {
                        point_set.insert(n);
                    }
                }
            }
        }
    }

    point_set
}

fn solve(start: Point, end: Point, walls: Walls, max_dist: isize, save_at_least: isize) -> usize {
    let p_max = Point {
        x: walls.iter().map(|w| w.x).max().unwrap_or(0),
        y: walls.iter().map(|w| w.y).max().unwrap_or(0),
    };

    let (costs_dict, path) = calc_costs(&end, &start, &walls, &p_max);
    path.par_iter()
        .take(path.len() - save_at_least as usize)
        .map(|p| {
            get_cheat_destinations(p, &p_max, &walls, &costs_dict, save_at_least, max_dist).len()
        })
        .sum()
}

fn part_1(walls: Walls, start: Point, end: Point) -> usize {
    solve(start, end, walls, 2, 100)
}

fn part_2(walls: Walls, start: Point, end: Point) -> usize {
    solve(start, end, walls, 20, 100)
}

fn main() {
    let input = include_str!("../../../inputs/input_20.txt");
    let (walls, start, end) = parse_input(input);
    println!("Part 1: {}", part_1(walls.clone(), start, end));
    println!("Part 2: {}", part_2(walls, start, end));
}
