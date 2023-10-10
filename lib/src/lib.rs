use std::{fmt, error::Error};

use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "lowercase")]
pub enum Check {
    BlazeHealth,
    BlazeVersion,
    BlazeResources,
}

impl fmt::Display for Check {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let name = match self {
            Check::BlazeHealth => "Blaze Health",
            Check::BlazeVersion => "Blaze Version",
            Check::BlazeResources => "Blaze Resources",
        };
        f.write_str(name)
    }
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
pub enum CheckResult {
    Ok(String),
    Err(String),
    Unexpected(String)
}

impl<E: Error> From<E> for CheckResult {
    fn from(value: E) -> Self {
        Self::Err(value.to_string())
    }
}
