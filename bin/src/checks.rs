use async_trait::async_trait;
use bridgehead_monitoring_lib::Check;
use serde_json::Value;

use crate::{CLIENT, CONFIG};

#[async_trait]
pub trait CheckExecutor {
    async fn execute(&self) -> String;
}

#[async_trait]
impl CheckExecutor for Check {
    async fn execute(&self) -> String {
        match self {
            Check::BlazeHealth => {
                match CLIENT.get(format!("{}/health", CONFIG.blaze_url)).send().await {
                    Ok(res) => {
                        res.status().to_string()
                    },
                    Err(e) => e.to_string()
                }
            },
            Check::BlazeResources => {
                match CLIENT.get(format!("{}/fhir", CONFIG.blaze_url)).send().await {
                    Ok(res) => {
                        let json = &res.json::<Value>().await.unwrap_or(Value::Null)["total"];
                        serde_json::to_string(json).unwrap_or_else(|e| e.to_string())
                    },
                    Err(e) => e.to_string()
                }
            },
            Check::BlazeVersion => {
                match CLIENT.get(format!("{}/fhir/metadata", CONFIG.blaze_url)).send().await {
                    Ok(res) => {
                        let json = &res.json::<Value>().await.unwrap_or(Value::Null)["software"]["version"];
                        serde_json::to_string(json).unwrap_or_else(|e| e.to_string())
                    },
                    Err(e) => e.to_string()
                }
            }
        }
    }
}
