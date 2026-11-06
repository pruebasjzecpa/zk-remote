// ZK-REMOTE: marca compilada en el binario. Usa el mismo mecanismo que un
// custom.txt firmado (APP_NAME), sin depender de la firma de upstream.
use hbb_common::config;

pub const APP_NAME: &str = "ZK-REMOTE";
pub const SOURCE_URL: &str = "https://github.com/pruebasjzecpa/zk-remote";

pub fn apply() {
    *config::APP_NAME.write().unwrap() = APP_NAME.to_owned();
}
