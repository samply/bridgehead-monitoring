use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub enum Check {
    BlazeHealth,
    BlazeVersion,
    BlazeResources,
}
