use anyhow::Result;
use std::str::FromStr;

/// Parses a line of text into a vector of values of type `T`, splitting by `SPLIT_CHAR`.
/// 
/// # Arguments
/// * `line` - A string slice containing the input line to parse.
/// 
/// # Returns
/// A `Result` containing a vector of parsed values, or an error if parsing fails for any element.
/// 
/// # Examples
/// 
/// ```
/// use aoc::line_to_int;
/// 
/// let result: Result<Vec<i32>, _> = line_to_int::<i32, ','>("1,2,3");
/// assert_eq!(result, Ok(vec![1, 2, 3]));
/// 
/// let result: Result<Vec<i32>, _> = line_to_int::<i32, ','>("4, 5, 6");
/// assert!(result.is_err()); // Whitespace would cause parsing to fail.
/// 
/// let result: Result<Vec<i32>, _> = line_to_int::<i32, ','>("");
/// assert_eq!(result, Ok(vec![])); // Empty input gives an empty vector.
/// ```
pub fn line_to_int<T: FromStr, const SPLIT_CHAR: char>(line: &str) -> Result<Vec<T>, T::Err> {
    line.split(SPLIT_CHAR)
        .filter(|i| !i.is_empty())
        .map(|i| i.parse::<T>())
        .collect()
}


/// Parses multiple lines of text into a vector of vectors of values of type `T`, splitting each line by `SPLIT_CHAR`.
/// 
/// # Arguments
/// * `input` - A string slice containing the input with multiple lines to parse.
/// 
/// # Returns
/// A `Result` containing a vector of vectors of parsed values, or an error if parsing fails for any element.
/// 
/// # Examples
/// 
/// ```
/// use aoc::parse_ints;
/// 
/// let input = "1,2,3\n4,5,6";
/// let result: Result<Vec<Vec<i32>>, _> = parse_ints::<i32, ','>(input);
/// assert_eq!(result, Ok(vec![vec![1, 2, 3], vec![4, 5, 6]]));
/// 
/// let input = "7 8\n9  10";
/// let result: Result<Vec<Vec<i32>>, _> = parse_ints::<i32, ' '>(input);
/// assert_eq!(result, Ok(vec![vec![7, 8], vec![9, 10]]));
/// 
/// let input = "11,12\ninvalid,13";
/// let result: Result<Vec<Vec<i32>>, _> = parse_ints::<i32, ','>(input);
/// assert!(result.is_err()); // Parsing fails due to "invalid".
/// ```
pub fn parse_ints<T: FromStr, const SPLIT_CHAR: char>(input: &str) -> Result<Vec<Vec<T>>, T::Err> {
    input
        .lines()
        .map(|line| line_to_int::<T,SPLIT_CHAR>(line))
        .collect()
}

/// A structure representing a point in a 2D grid.
/// 
/// # Fields
/// - `x`: The x-coordinate of the point.
/// - `y`: The y-coordinate of the point.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Point {
    pub x: isize,
    pub y: isize,
}

impl Point {
    /// Creates a new `Point` with the given x and y coordinates.
    ///
    /// # Arguments
    /// - `x`: The x-coordinate of the point.
    /// - `y`: The y-coordinate of the point.
    ///
    /// # Examples
    /// ```
    /// use aoc::Point; 
    ///
    /// let p = Point::new(3, 5);
    /// assert_eq!(p.x, 3);
    /// assert_eq!(p.y, 5);
    /// ```
    pub fn new(x: isize, y: isize) -> Self {
        Self { x, y }
    }
}

/// Checks if a given point `p` lies within the bounds of a grid defined by the maximum point `p_max`.
///
/// # Arguments
/// - `p`: The point to check.
/// - `p_max`: The maximum bounds of the grid. Points are valid if `0 <= x < p_max.x` and `0 <= y < p_max.y`.
///
/// # Returns
/// - `true` if the point is within the grid bounds.
/// - `false` otherwise.
///
/// # Examples
/// ```
/// use aoc::{Point, is_in_grid}; 
///
/// let p = Point::new(2, 3);
/// let grid_max = Point::new(5, 5);
/// assert!(is_in_grid(p, grid_max));
///
/// let outside_p = Point::new(5, 3);
/// assert!(!is_in_grid(outside_p, grid_max));
/// ```
pub fn is_in_grid(p: Point, p_max: Point) -> bool {
    p.x >= 0 && p.y >= 0 && p.x < p_max.x && p.y < p_max.y
}


pub fn get_neighbours_4(p: Point, p_max: Point) -> Vec<Point> {
    let mut neighbours = Vec::new();
    if p.x > 0 { neighbours.push(Point { x: p.x - 1, y: p.y }); }
    if p.y > 0 { neighbours.push(Point { x: p.x, y: p.y - 1 }); }
    if p.x + 1 < p_max.x { neighbours.push(Point { x: p.x + 1, y: p.y }); }
    if p.y + 1 < p_max.y { neighbours.push(Point { x: p.x, y: p.y + 1 }); }
    neighbours
}
