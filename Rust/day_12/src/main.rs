use std::collections::{HashSet, HashMap};
use aoc::Point;
type SideType = (HashMap<(isize, isize), Vec<isize>>, HashMap<(isize, isize), Vec<isize>>) ;

fn parse_input(input: &str) -> HashMap<char, HashSet<Point>> {
    let mut regions: HashMap<char, HashSet<Point>> = HashMap::new();
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            regions.entry(c).or_default().insert(Point::new(x as isize, y as isize));
        }
    }
    regions
}

fn get_neighbours_4(p: Point) -> HashSet<Point> {
    let mut neighbours = HashSet::new();
    neighbours.insert(Point::new(p.x - 1, p.y));
    neighbours.insert(Point::new(p.x, p.y - 1));
    neighbours.insert(Point::new(p.x + 1, p.y));
    neighbours.insert(Point::new(p.x, p.y + 1));
    neighbours
}

fn partition(mut points: HashSet<Point>) -> Vec<HashSet<Point>> {
    let mut res = Vec::new();
    while let Some(&p) = points.iter().next() {
        points.remove(&p);
        let mut queue: Vec<Point> = get_neighbours_4(p).intersection(&points).cloned().collect();
        let mut region = HashSet::new();
        region.insert(p);
        
        while let Some(q) = queue.pop() {
            if points.remove(&q) {
                region.insert(q);
                queue.extend(get_neighbours_4(q).intersection(&points).cloned());
            }
        }
        res.push(region);
    }
    res
}

fn add_to_sides(new_perimeter: &HashSet<Point>, p: Point, sides: &mut SideType) {
    for n in new_perimeter {
        if n.x == p.x {
            sides.0.entry((n.y, p.y)).or_default().push(p.x);
        }
        if n.y == p.y {
            sides.1.entry((n.x, p.x)).or_default().push(p.y);
        }
    }
}

fn calc_sides(sides: &SideType) -> i32 {
    let mut n_v = 0;
    for side in [&sides.0, &sides.1] {
        for q in side.values() {
            let mut sorted_q = q.clone();
            sorted_q.sort_unstable();
            let mut prev = -2;
            for &s in &sorted_q {
                if (s - prev).abs() > 1 {
                    n_v += 1;
                }
                prev = s;
            }
        }
    }
    n_v
}

fn eval_region(points: &HashSet<Point>) -> (i32, i32) {
    let mut perimeter = 0;
    let mut sides: SideType = (HashMap::new(), HashMap::new());
    for &p in points {
        let new_perimeter: HashSet<Point> = get_neighbours_4(p).difference(points).cloned().collect();
        perimeter += new_perimeter.len() as i32;
        add_to_sides(&new_perimeter, p, &mut sides);
    }
    (calc_sides(&sides), perimeter)
}

fn solve(regions: HashMap<char, HashSet<Point>>) -> (i32, i32) {
    let new_regions: Vec<HashSet<Point>> = regions
        .values()
        .flat_map(|region| partition(region.clone()))
        .collect();

    let mut part1 = 0;
    let mut part2 = 0;
    for points in new_regions {
        let (n, perimeter) = eval_region(&points);
        part1 += points.len() as i32 * perimeter;
        part2 += points.len() as i32 * n;
    }
    (part1, part2)
}

fn main() {
    let input = include_str!("../../../inputs/input_12.txt");
    let regions = parse_input(input);
    let (part1, part2) = solve(regions);
    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);
}

