#[cfg(unix)]
pub async fn wait_for_shutdown_signal() {
    use std::process::exit;

    use tokio::signal::unix::{signal, SignalKind};
    let mut sigterm = signal(SignalKind::terminate())
        .expect("Unable to register shutdown handler; are you running a Unix-based OS?");
    let mut sigint = signal(SignalKind::interrupt())
        .expect("Unable to register shutdown handler; are you running a Unix-based OS?");
    let signal = tokio::select! {
        _ = sigterm.recv() => "SIGTERM",
        _ = sigint.recv() => "SIGINT"
    };
    println!("Received signal ({signal}) - shutting down.");
    exit(0);
}

#[cfg(windows)]
pub async fn wait_for_shutdown_signal() {
    if let Err(e) = tokio::signal::ctrl_c().await {
        panic!("Unable to register shutdown handler: {e}.");
    }
    println!("Received shutdown signal - shutting down.");
    exit(0);
}
