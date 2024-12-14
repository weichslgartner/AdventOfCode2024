use aoc::{extract_all_ints, Point};

const COST_A: isize = 3;
const COST_B: isize = 1;
const OFFSET: isize = 10_000_000_000_000;

fn parse_input(input_str: &str) -> Vec<Vec<Point>> {
    input_str
        .trim()
        .split("\n\n")
        .map(|block| {
            block
                .lines()
                .map(|line| {
                    let nums = extract_all_ints(line);
                    Point::new(nums[0] as isize, nums[1] as isize)
                })
                .collect()
        })
        .collect()
}


fn solve(a: &Point, b: &Point, target: &Point) -> isize {
    let target_diff = target.x * b.y - target.y * b.x;
    let dividend = b.y * a.x - b.x * a.y;
    if target_diff % dividend != 0 {
        return 0;
    }
    let a_times = target_diff / dividend;
    let b_times = (target.y - a_times * a.y) / b.y;
    a_times * COST_A + b_times * COST_B
}

fn part_1(machines: &[Vec<Point>]) -> isize {
    machines
        .iter()
        .map(|machine| solve(&machine[0], &machine[1], &machine[2]))
        .sum()
}

fn part_2(machines: &[Vec<Point>]) -> isize {
    machines
        .iter()
        .map(|machine| {
            let target = Point::new(machine[2].x + OFFSET, machine[2].y + OFFSET);
            solve(&machine[0], &machine[1], &target)
        })
        .sum()
}

fn main() {
    let input = include_str!("../../../inputs/input_13.txt");
    let machines = parse_input(input);
    println!("Part 1: {}", part_1(&machines));
    println!("Part 2: {}", part_2(&machines));
}
