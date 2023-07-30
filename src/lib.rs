use std::collections::HashMap;

use pyo3::prelude::*;

const KEYWORDS: [char; 5] = ['*', '_', '~', '`', '|'];
const NO_SUB_PARSING_KEYWORDS: [char; 1] = ['`'];
const QUOTE_KEYWORDS: [char; 1] = ['>'];
const BLOCK_KEYWORDS: [(char, usize); 2] = [('`', 2), ('|', 1)];
const PLACEHOLDER: &str = "\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}";

#[pyfunction]
fn format_body(body: String, new_tags: HashMap<String, (String, String)>) -> PyResult<String> {
    let mut chars: Vec<char> = body.chars().collect();
    if chars.len() < 1 {
        return Ok(body);
    }
    let styles: Vec<(String, usize, usize)> = parse_with_limits(&chars, 0, chars.len() - 1, 0);
    let parse_quotes = new_tags.contains_key(&">".to_string());

    let mut tags: Vec<(usize, String, String, bool)> = vec![];
    for style in styles {
        let (keyword, start, end) = style;
        if new_tags.contains_key(&keyword) {
            tags.push((start, keyword.clone(), new_tags.get(&keyword).unwrap().0.clone(), false));
            tags.push((end, keyword.clone(), new_tags.get(&keyword).unwrap().1.clone(), QUOTE_KEYWORDS.contains(&keyword.chars().next().unwrap())));
        } else if keyword == ">>" && parse_quotes {
            tags.push((start, keyword.clone(), "".to_string(), false));
        }
    }

    tags.sort_by(|a, b| b.0.cmp(&a.0));

    for tag in tags {
        let (index, keyword, tag, is_end_quote_block) = tag;
        let end = if is_end_quote_block {
            index
        } else if keyword == ">>" {
            index + 1
        } else {
            index + keyword.len()
        };
        chars = [chars[..index].to_vec(), tag.chars().collect(), chars[end..].to_vec()].concat();
    }

    Ok(remove_non_escaped_backslashes(chars.into_iter().collect()))
}

fn remove_non_escaped_backslashes(text: String) -> String {
    let tmp_string = text.replace("\\\\", PLACEHOLDER);
    let tmp_string = tmp_string.replace("\\", "");
    tmp_string.replace(PLACEHOLDER, "\\")
}

fn parse_with_limits(chars: &Vec<char>, start: usize, end: usize, depth: usize) -> Vec<(String, usize, usize)> {
    let mut styles = Vec::new();
    let mut index = start;
    let end = end.min(chars.len() - 1);
    println!("parse with limits start {}, end {}", start, end);

    while index <= end {
        if preceeded_by_backslash(chars, index, start) {
            index += 1;
            continue;
        }

        let c = chars[index];
        if c == '|' && !is_char_repeating(chars, c, index, end) {
            index += 1;
            continue;
        }

        if QUOTE_KEYWORDS.contains(&c) {
            if is_quote_start(chars, index, depth) {
                let to = seek_end_of_quote(chars, index, end, depth);
                styles.push((">".to_string(), index, to));
                styles.append(&mut parse_with_limits(chars, index + 1, to, depth + 1));
                index = to;
                continue;
            }
            if depth > 0 {
                styles.push((">>".to_string(), index, index + 1));
            }
            index += 1;
            continue;
        }

        if !preceeded_by_whitespace(chars, index, start) || followed_by_whitespace(chars, index, end) {
            index += 1;
            continue;
        }

        if !KEYWORDS.contains(&c) {
            index += 1;
            continue;
        }

        if BLOCK_KEYWORDS.iter().any(|&(k, _)| k == c) && is_char_repeating(chars, c, index, end) {
            let block_indicator_size = get_block_indicator_size(c);
            match seek_end_block(chars, c, index + block_indicator_size + 1, end) {
                Some(to) => {
                    if to != index + block_indicator_size * 2 - 1 {
                        let keyword = c.to_string().repeat(block_indicator_size+1);
                        styles.push((keyword, index, to));
                        if !NO_SUB_PARSING_KEYWORDS.contains(&c) {
                            styles.append(&mut parse_with_limits(chars, index + block_indicator_size + 1, to - 1, depth));
                        }
                    }
                    index = to + block_indicator_size;
                    continue;
                }
                None => ()
            }
        }

        match seek_end(chars, c, index + 1, end) {
            Some (to) => {
                if to != index + 1 {
                    styles.push((c.to_string(), index, to));
                    if !NO_SUB_PARSING_KEYWORDS.contains(&c) {
                        styles.append(&mut parse_with_limits(chars, index + 1, to - 1, depth));
                    }
                }
                index = to;
            }
            None => ()
        }
        index += 1;
    }
    styles
}

fn is_char_repeating(chars: &Vec<char>, keyword: char, index: usize, end: usize) -> bool {
    let block_indicator_size = get_block_indicator_size(keyword);

    (0..block_indicator_size as usize)
        .all(|i| index + i <= end && chars[index + i] == keyword)
}

fn preceeded_by_whitespace(chars: &Vec<char>, index: usize, start: usize) -> bool {
    index == start || chars[index - 1].is_whitespace()
}

fn followed_by_whitespace(chars: &Vec<char>, index: usize, end: usize) -> bool {
    index >= end || chars[index + 1].is_whitespace()
}

fn seek_end(chars: &Vec<char>, keyword: char, start: usize, end: usize) -> Option<usize> {
    for i in start..=end {
        let c = chars[i];
        if c == '\n' {
            return None;
        }
        if c == keyword
            && !chars[i - 1].is_whitespace()
            && !preceeded_by_backslash(chars, i, start)
        {
            return Some(i);
        }
    }
    None
}

fn seek_end_of_quote(chars: &Vec<char>, start: usize, end: usize, depth: usize) -> usize {
    for i in start..=end {
        if chars[i] == '\n' {
            if i + 2 + depth > chars.len() {
                return i;
            }
            if chars[i + 1..=i + 1 + depth].iter().any(|&c| !QUOTE_KEYWORDS.contains(&c)) {
                return i;
            }
        }
    }
    end + 1
}

fn seek_end_block(chars: &Vec<char>, keyword: char, start: usize, end: usize) -> Option<usize> {
    for i in start..=end {
        if chars[i] == keyword
            && is_char_repeating(chars, keyword, i + 1, end)
            && !preceeded_by_backslash(chars, i, start)
        {
            return Some(i);
        }
    }
    None
}

fn is_quote_start(chars: &Vec<char>, index: usize, depth: usize) -> bool {
    index - depth == 0 || chars[index - 1 - depth] == '\n'
}

fn preceeded_by_backslash(chars: &Vec<char>, index: usize, start: usize) -> bool {
    if index == start {
        return false;
    }
    let mut num_backslashes = 0;
    while index > num_backslashes && chars[index - 1 - num_backslashes] == '\\' {
        num_backslashes += 1;
    }
    num_backslashes % 2 == 1
}

fn get_block_indicator_size(keyword: char) -> usize {
    for &(k, v) in BLOCK_KEYWORDS.iter() {
        if k == keyword {
            return v;
        }
    }
    1 // shouldn't ever happen
}

#[pymodule]
fn slidge_style_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(format_body, m)?)?;
    Ok(())
}
