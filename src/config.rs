use std::convert::Infallible;

use beam_lib::AppId;
use clap::Parser;
use reqwest::Url;

#[derive(Debug, Parser)]
pub struct Config {
    #[clap(long, env, value_parser=|id: &str| Ok::<_, Infallible>(AppId::new_unchecked(id)))]
    /// Beam id for the application
    pub beam_id: AppId,

    #[clap(long, env)]
    /// Beam secret for the application
    pub beam_api_key: String,

    #[clap(long, env, default_value="http://bridgehead-beam-proxy")]
    /// Beam proxy url
    pub beam_proxy: Url,
}

