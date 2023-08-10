use std::time::Duration;

use beam_lib::{MsgId, TaskRequest, TaskResult, WorkStatus, AppId};
use checks::CheckExecutor;
use clap::Parser;
use config::Config;
use bridgehead_monitoring_lib::Check;
use futures::future::join_all;
use once_cell::sync::Lazy;
use reqwest::{Client, StatusCode, header::{HeaderMap, AUTHORIZATION, HeaderValue, ACCEPT}};
use serde_json::Value;

mod config;
mod checks;
mod shutdown;

static CONFIG: Lazy<Config> = Lazy::new(|| Config::parse());

static CLIENT: Lazy<Client> = Lazy::new(|| {
    let mut header_map = HeaderMap::new();
    header_map.insert(AUTHORIZATION, HeaderValue::from_bytes(format!("ApiKey {} {}", CONFIG.beam_id, CONFIG.beam_api_key).as_bytes()).unwrap());
    header_map.insert(ACCEPT, HeaderValue::from_static("application/json"));
    reqwest::Client::builder().default_headers(header_map).build().unwrap()
});

const RETRY_INTERVAL: Duration = Duration::from_secs(60);
const MAX_RETRYS: usize = 100;

#[tokio::main]
async fn main() {
    tokio::spawn(shutdown::wait_for_shutdown_signal());
    loop {
        let Some((checks, task_id, sender)) = poll_checks().await else {
            break;
        };
        let results = join_all(checks.iter().map(CheckExecutor::execute)).await;
        send_results(results, task_id, sender).await;
    }
}

async fn poll_checks() -> Option<(Vec<Check>, MsgId, AppId)> {
    static URL: Lazy<String> = Lazy::new(|| {
        let mut url = CONFIG.beam_proxy_url.join("/v1/tasks").unwrap();
        url.set_query(Some("wait_count=1&filter=todo"));
        url.to_string()
    });

    for _ in 0..MAX_RETRYS {
        let resp = match CLIENT.get(&*URL).send().await {
            Ok(resp) => resp,
            Err(e) => {
                eprintln!("Request to proxy failed: {e}");
                tokio::time::sleep(RETRY_INTERVAL).await;
                continue;
            },
        };

        return match resp.status() {
            StatusCode::OK | StatusCode::PARTIAL_CONTENT => {
                match resp.json::<Vec<TaskRequest<Vec<Check>>>>().await.as_mut().map(Vec::pop) {
                    Ok(Some(TaskRequest { id, body, from, .. })) => Some((body, id, from)),
                    Ok(None) => {
                        eprintln!("Got 0 Tasks");
                        continue
                    },
                    Err(e) => {
                        eprintln!("Failed to get response json: {e}");
                        tokio::time::sleep(RETRY_INTERVAL).await;
                        continue
                    },
                }
            },
            StatusCode::GATEWAY_TIMEOUT => continue,
            e => {
                eprintln!("Polling got unexpected statuscode while fetching tasks: {e}");
                tokio::time::sleep(RETRY_INTERVAL).await;
                continue
            },
        }
    }
    None
}

async fn send_results(results: Vec<String>, task_id: MsgId, sender: AppId) {
    let url = CONFIG.beam_proxy_url.join(&format!("/v1/tasks/{task_id}/results/{}", CONFIG.beam_id)).unwrap();
    
    let resp = CLIENT.put(url).json(&TaskResult {
        from: CONFIG.beam_id.clone(),
        to: vec![sender],
        task: task_id,
        status: WorkStatus::Succeeded,
        body: results,
        metadata: Value::Null,
    }).send().await;

    match resp {
        Ok(resp) => if resp.status() == StatusCode::CREATED {
            println!("Successfully reported health")
        },
        Err(e) => {
            eprintln!("Failed to send results: {e}");
            return;
        },
    };
}
