# Wi-Fi Presence-Based Shinobi Notification Script

## Description
This script enables or disables notifications on Shinobi based on the presence of residents, utilizing connected cell phones on the Wi-Fi network as a reference. The script runs a continuous scan of the network, monitoring connected devices to determine resident presence. It activates or deactivates Shinobi notifications accordingly, factoring in specific time ranges defined in the configuration file.

## Code Overview
### `main.py`
- `ScanRede` class: Manages the scanning of the network, monitoring devices, validating presence, and toggling Shinobi notifications.
- `change_status()`: Determines whether to activate or deactivate notifications based on resident presence or specified time ranges.
- `valida_horario()`: Validates the current time falls within the defined time range.
- `valida_presence()`: Validates resident presence based on connected devices.
- `gravar_status()`, `ler_status()`, `default_status()`: Functions to read, write, and set default status in a cache file.
- `scanear_rede()`: Scans the network for connected devices and updates the presence map accordingly.
- `monitorar_dispositivo()`: Monitors specific devices on the network and notifies changes in their presence.
- `logger()`: Logs messages and events.

### `shinobi.py`
- `Shinobi` class: Interacts with the Shinobi API to activate or deactivate notifications.

### `telegram.py`
- `TelegramBot` class: Manages the Telegram bot functionalities for sending notifications.

## Usage
- Ensure correct setup of the configuration file (`config_helper.py`) with appropriate token, URL, time ranges, and devices to monitor.
- Run `main.py` to initiate the script, which continuously monitors the Wi-Fi network and manages Shinobi notifications.

## Configuration
- Adjust the `config_helper.py` file to set up tokens, URLs, time ranges, and other parameters necessary for proper functionality.

## Dependencies
- Python 3.x
- `requests` library
- `telegram` library
- Other libraries as listed in the script's import statements.

