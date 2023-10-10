use async_trait::async_trait;
use bridgehead_monitoring_lib::{Check, CheckResult};
use reqwest::StatusCode;
use serde_json::Value;

use crate::{CLIENT, CONFIG};

#[async_trait]
pub trait CheckExecutor {
    async fn execute(&self) -> Result<CheckResult, CheckResult>;
}

#[async_trait]
impl CheckExecutor for Check {
    async fn execute(&self) -> Result<CheckResult, CheckResult> {
        match self {
            Check::BlazeHealth => {
                let res = CLIENT.get(format!("{}health", CONFIG.blaze_url)).send().await?;
                if res.status() == StatusCode::OK {
                    Ok(CheckResult::Ok(res.status().to_string()))
                } else {
                    Err(CheckResult::Err(format!("Unhealthy: {}", res.status())))
                }
            },
            Check::BlazeResources => {
                let res = CLIENT.get(format!("{}fhir", CONFIG.blaze_url)).send().await?;
                let json = &res.json::<Value>().await?["total"];
                Ok(CheckResult::Ok(serde_json::to_string(json)?))
            },
            Check::BlazeVersion => {
                let res = CLIENT.get(format!("{}fhir/metadata", CONFIG.blaze_url)).send().await?;
                let json = &res.json::<Value>().await?["software"]["version"];
                Ok(CheckResult::Ok(serde_json::to_string(json)?))
            }
        }
    }
}
