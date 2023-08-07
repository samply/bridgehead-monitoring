use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq, Clone)]
#[serde(rename_all = "lowercase")]
pub enum Check {
    BlazeHealth,
    BlazeVersion,
    BlazeResources,
}
