use std::collections::HashSet;

use aoc::Direction;
use aoc::Point;

type Walls = HashSet<Point>;
type Boxes = HashSet<Point>;

fn parse_input(input_str: &str) -> (Walls, Boxes, Point, Vec<Direction>) {
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
            directions.push(Direction::from_char(c).expect("cannot parse direction"));
        }
    }

    (walls, boxes, robot.expect("Robot not found"), directions)
}

#[allow(unused)]
fn print_grid(
    boxes_left: &Boxes,
    boxes_right: &Boxes,
    robot: Point,
    walls: &Walls,
    dir: Direction,
) {
    println!("{:?}", dir);
    for y in 0..=7 {
        for x in 0..=15 {
            let p = Point::new(x, y);
            if boxes_left.contains(&p) {
                print!("[");
            } else if boxes_right.contains(&p) {
                print!("]");
            } else if walls.contains(&p) {
                print!("#");
            } else if p == robot {
                print!("@");
            } else {
                print!(".");
            }
        }
        println!();
    }
}

fn revert(points: &Boxes, p: Point) -> Boxes {
    points
        .iter()
        .map(|x| Point::new(x.x - p.x, x.y - p.y))
        .collect()
}

fn can_move_free(to_add_right: &Boxes, to_add_left: &Boxes,boxes_left: &Boxes, boxes_right: &Boxes, walls: &Walls) -> bool{
    for non_free in [boxes_left,boxes_right,walls]{
        for to_add in [to_add_right,to_add_left]{
            if !to_add.is_disjoint(non_free){
                return  false;
            }
        }
    }
    true
}

fn move_boxes(
    boxes_left: &mut Boxes,
    boxes_right: &mut Boxes,
    p: Point,
    robot: Point,
    robot_next: Point,
    walls: &Walls,
) -> Point {
    let (mut to_add_left, mut to_add_right) = add_boxes(boxes_left, boxes_right, p, robot_next);
    revert(&to_add_left,p).iter().for_each(|value: &Point| {boxes_left.remove(value);});
    revert(&to_add_right,p).iter().for_each(|value: &Point| {boxes_right.remove(value);});
    loop {
        if can_move_free(&to_add_right, &to_add_left,boxes_left, boxes_right, walls) {
            boxes_left.extend(&to_add_left);
            boxes_right.extend(&to_add_right);
            return robot_next;
        }

        if !to_add_left.is_disjoint(walls) || !to_add_right.is_disjoint(walls) {
            // revert changes
            boxes_left.extend(revert(&to_add_left, p));
            boxes_right.extend(revert(&to_add_right, p));
            return robot;
        }

        for s in [to_add_left.clone(), to_add_right.clone()].iter() {
            for b in s {
                let (add_l, add_r) = add_boxes(boxes_left, boxes_right, p, *b);
                to_add_left.extend(&add_l);
                to_add_right.extend(&add_r);
                revert(&add_l,p).iter().for_each(|value: &Point| {boxes_left.remove(value);});
                revert(&add_r,p).iter().for_each(|value: &Point| {boxes_right.remove(value);});
                
            }
        }
    }
}

fn add_boxes(
    boxes_left: &Boxes,
    boxes_right: &Boxes,
    p: Point,
    robot_next: Point,
) -> (Boxes, Boxes) {
    if boxes_left.contains(&robot_next) {
        let mut to_add_left = HashSet::new();
        let mut to_add_right = HashSet::new();
        to_add_left.insert(Point::new(robot_next.x + p.x, robot_next.y + p.y));
        if !boxes_right.is_empty() {
            to_add_right.insert(Point::new(robot_next.x + 1 + p.x, robot_next.y + p.y));
        }
        return (to_add_left, to_add_right);
    }

    if boxes_right.contains(&robot_next) {
        let mut to_add_left = HashSet::new();
        let mut to_add_right = HashSet::new();
        to_add_left.insert(Point::new(robot_next.x - 1 + p.x, robot_next.y + p.y));
        to_add_right.insert(Point::new(robot_next.x + p.x, robot_next.y + p.y));
        return (to_add_left, to_add_right);
    }

    (HashSet::new(), HashSet::new())
}

fn solve(
    walls: &Walls,
    boxes_left: &Boxes,
    boxes_right: &Boxes,
    mut robot: Point,
    directions: &[Direction],
) -> isize {
    let mut boxes_left = boxes_left.clone();
    let mut boxes_right = boxes_right.clone();
    //print_grid(&boxes_left, &boxes_right, robot, walls, DirectionStr::North);
    for &direct in directions {
        let p = direct.to_point();
        let robot_next = Point::new(robot.x + p.x, robot.y + p.y);
        if walls.contains(&robot_next) {
            //print_grid(&boxes_left, &boxes_right, robot, walls, direct);
            continue;
        }

        if !boxes_left.contains(&robot_next)
            && (boxes_right.is_empty() || !boxes_right.contains(&robot_next))
        {
            robot = robot_next;
            //print_grid(&boxes_left, &boxes_right, robot, walls, direct);
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
        //print_grid(&boxes_left, &boxes_right, robot, walls, direct);
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

fn part_1(walls: &Walls, boxes: &Boxes, robot: Point, directions: &[Direction]) -> isize {
    solve(walls, boxes, &HashSet::new(), robot, directions)
}

fn part_2(walls: &Walls, boxes: &Boxes, robot: Point, directions: &[Direction]) -> isize {
    let (mut new_walls_left, new_walls_right) = expand(walls);
    let (new_boxes_left, new_boxes_right) = expand(boxes);
    let new_robot = Point::new(robot.x * 2, robot.y);
    new_walls_left.extend(new_walls_right);
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
