use std::collections::HashSet;

use aoc::DirectionStr;
use aoc::Point;

type Walls = HashSet<Point>;
type Boxes = HashSet<Point>;

fn parse_input(input_str: &str) -> (Walls, Boxes, Point, Vec<DirectionStr>) {
    let mut robot = None;
    let mut walls = HashSet::new();
    let mut boxes = HashSet::new();
    let mut directions = Vec::new();

    let parts: Vec<&str> = input_str.split("\n\n").collect();
    let grid = parts[0];
    let directions_str = parts[1];

    for (y, line) in grid.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let p = Point::new(x as isize, y as isize);
            match c {
                '#' => {
                    walls.insert(p);
                }
                '@' => {
                    robot = Some(p);
                }
                'O' => {
                    boxes.insert(p);
                }
                _ => {}
            }
        }
    }

    for line in directions_str.lines() {
        for c in line.chars() {
            directions.push(DirectionStr::from_char(c).expect("cannot parse direction"));
        }
    }

    (walls, boxes, robot.expect("Robot not found"), directions)
}

fn move_boxes(
    boxes_left: &mut Boxes,
    boxes_right: &mut Boxes,
    p: Point,
    robot: Point,
    robot_next: Point,
    walls: &Walls,
) -> Point {
    let left_old = boxes_left.clone();
    let right_old = boxes_right.clone();
    let (mut to_add_left, mut to_add_right, to_remove_left, to_remove_right) =
        add_boxes(boxes_left, boxes_right, p, robot_next);
    boxes_left.retain(|x| !&to_remove_left.contains(x));
    boxes_right.retain(|x| !&to_remove_right.contains(x));
    let mut to_remove_left: Boxes = HashSet::new();
    let mut to_remove_right: Boxes = HashSet::new();
    to_remove_left.extend(to_remove_left.clone());
    to_remove_right.extend(to_remove_right.clone());
    loop {
        let all_adds: HashSet<_> = to_add_left.union(&to_add_right).collect();
        let all_non_free_space: HashSet<_> = boxes_left.union(boxes_right).cloned().collect();
        let all_non_free_space: HashSet<_> = all_non_free_space.union(walls).collect();

        
        if all_adds.is_disjoint(&all_non_free_space) {
            boxes_left.extend(&to_add_left);
            boxes_right.extend(&to_add_right);
            return robot_next;
        }

        if !to_add_left.is_disjoint(walls) || !to_add_right.is_disjoint(walls) {
            *boxes_left = left_old;
            *boxes_right = right_old;
           // boxes_left.extend(to_remove_left);
           // boxes_right.extend(to_add_right);
            return robot;
        }

        for s in [to_add_left.clone(), to_add_right.clone()].iter() {
            for b in s {
                let (add_l, add_r, rem_l, rem_r) = add_boxes(boxes_left, boxes_right, p, *b);
                to_add_left.extend(add_l);
                to_add_right.extend(add_r);
                boxes_left.retain(|x| !rem_l.contains(x));
                boxes_right.retain(|x| !rem_r.contains(x));
                to_remove_left.extend(rem_l);
                to_remove_right.extend(rem_r);

            }
        }
    }
}

fn add_boxes(
    boxes_left: &Boxes,
    boxes_right: &Boxes,
    p: Point,
    robot_next: Point,
) -> (Boxes, Boxes, Boxes, Boxes) {
    if boxes_left.contains(&robot_next) {
        let mut to_add_left = HashSet::new();
        let mut to_add_right = HashSet::new();
        let mut to_remove_left = HashSet::new();
        let mut to_remove_right = HashSet::new();
        to_remove_left.insert(robot_next);
        to_add_left.insert(Point::new(robot_next.x + p.x, robot_next.y + p.y));
        if !boxes_right.is_empty() {
            to_remove_right.insert(Point::new(robot_next.x + 1, robot_next.y));
            to_add_right.insert(Point::new(robot_next.x + 1 + p.x, robot_next.y + p.y));
        }

        return (to_add_left, to_add_right, to_remove_left, to_remove_right);
    }

    if boxes_right.contains(&robot_next) {
        let mut to_add_left = HashSet::new();
        let mut to_add_right = HashSet::new();
        let mut to_remove_left = HashSet::new();
        let mut to_remove_right = HashSet::new();

        to_remove_right.insert(robot_next);
        to_remove_left.insert(Point::new(robot_next.x - 1, robot_next.y));

        to_add_left.insert(Point::new(robot_next.x - 1 + p.x, robot_next.y + p.y));
        to_add_right.insert(Point::new(robot_next.x + p.x, robot_next.y + p.y));

        return (to_add_left, to_add_right, to_remove_left, to_remove_right);
    }

    (
        HashSet::new(),
        HashSet::new(),
        HashSet::new(),
        HashSet::new(),
    )
}

fn solve(
    walls: &Walls,
    boxes_left: &Boxes,
    boxes_right: &Boxes,
    mut robot: Point,
    directions: &[DirectionStr],
) -> isize {
    let mut boxes_left = boxes_left.clone();
    let mut boxes_right = boxes_right.clone();
    for &direct in directions {
        let p = direct.to_point();
        let robot_next = Point::new(robot.x + p.x, robot.y + p.y);

        if walls.contains(&robot_next) {
            continue;
        }

        if !boxes_left.contains(&robot_next)
            && (boxes_right.is_empty() || !boxes_right.contains(&robot_next))
        {
            robot = robot_next;
            continue;
        }

        robot = move_boxes(
            &mut boxes_left,
            &mut boxes_right,
            p,
            robot,
            robot_next,
            walls,
        );
    }
    boxes_left.iter().map(|p| 100 * p.y + p.x).sum()
}

fn expand(points: &HashSet<Point>) -> (HashSet<Point>, HashSet<Point>) {
    let mut left = HashSet::new();
    let mut right = HashSet::new();

    for &p in points {
        let b_new = Point::new(p.x * 2, p.y);
        left.insert(b_new);
        right.insert(Point::new(b_new.x + 1, p.y));
    }

    (left, right)
}

fn part_1(walls: &Walls, boxes: &Boxes, robot: Point, directions: &[DirectionStr]) -> isize {
    solve(walls, boxes, &HashSet::new(), robot, directions)
}

fn part_2(walls: &Walls, boxes: &Boxes, robot: Point, directions: &[DirectionStr]) -> isize {
    let (mut new_walls_left, new_walls_right) = expand(walls);
    let (new_boxes_left, new_boxes_right) = expand(boxes);
    let new_robot = Point::new(robot.x * 2, robot.y);
    new_walls_left.extend(new_walls_right.iter());
    solve(
        &new_walls_left,
        &new_boxes_left,
        &new_boxes_right,
        new_robot,
        directions,
    )
}

fn main() {
    let input: &str = include_str!("../../../inputs/input_15.txt");
    let (walls, boxes, robot, directions) = parse_input(input);
    println!("Part 1: {}", part_1(&walls, &boxes, robot, &directions));
    println!("Part 2: {}", part_2(&walls, &boxes, robot, &directions));
}
