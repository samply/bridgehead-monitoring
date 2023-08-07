use std::fmt;

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
