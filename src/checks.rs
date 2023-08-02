use serde_json::Value;

use crate::CLIENT;

#[derive(serde::Serialize, serde::Deserialize)]
pub enum Check {
    BlazeHealth,
    BlazeVersion,
    BlazeResources,
}

impl Check {
    pub async fn execute(&self) -> String {
        match self {
            Check::BlazeHealth => {
                match CLIENT.get("http://bridgehead-ccp-blaze:8080/health").send().await {
                    Ok(res) => {
                        res.status().to_string()
                    },
                    Err(e) => e.to_string()
                }
            },
            Check::BlazeResources => {
                match CLIENT.get("http://bridgehead-ccp-blaze:8080/fhir").send().await {
                    Ok(res) => {
                        let json = &res.json::<Value>().await.unwrap()["total"];
                        serde_json::to_string(json).unwrap_or_else(|e| e.to_string())
                    },
                    Err(e) => e.to_string()
                }
            },
            Check::BlazeVersion => {
                match CLIENT.get("http://bridgehead-ccp-blaze:8080/fhir/metadata").send().await {
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
