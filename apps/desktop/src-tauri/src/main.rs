fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            get_default_api_endpoint,
            get_default_storage_path
        ])
        .run(tauri::generate_context!())
        .expect("failed to run PromptSpec desktop app");
}

#[tauri::command]
fn get_default_api_endpoint() -> String {
    "http://localhost:8000".to_string()
}

#[tauri::command]
fn get_default_storage_path() -> String {
    ".promptspec/app.sqlite".to_string()
}

