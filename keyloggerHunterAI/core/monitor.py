import threading
from core.logger import log_alert
from core.behavior_analyzer import start_typing_monitor
# From Phase 3+ onward, import other modules here:
from scanner.process_scanner import scan_processes
from scanner.api_detector import scan_api_usage
from scanner.registry_scanner import scan_registry
from scanner.file_checker import scan_files

def main():
    log_alert(" KeyloggerHunterAI initialized.")

    # Start AI typing behavior monitor
    threading.Thread(target=start_typing_monitor, daemon=True).start()

    # Placeholder: Scanners will be added here later
    threading.Thread(target=scan_processes, daemon=True).start()
    threading.Thread(target=scan_api_usage, daemon=True).start()
    threading.Thread(target=scan_registry, daemon=True).start()
    threading.Thread(target=scan_files, daemon=True).start()

    # Keep main thread alive
    while True:
        pass

if __name__ == "__main__":
    main()
