use pyo3::prelude::*;

mod parser;

mod telegram;
use telegram::parse_for_telegram;

mod general;
use general::format_body;

#[pymodule]
fn slidge_style_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(format_body, m)?)?;
    m.add_function(wrap_pyfunction!(parse_for_telegram, m)?)?;
    Ok(())
}
