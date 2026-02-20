# Desi Alarm & Smart Lock Integration for Home Assistant

This custom component integrates Desi Alarm and Smart Lock systems into Home Assistant.

## Features
* **Alarm Control Panel:** Arm (away/home) and disarm your Desi alarm system.
* **Lock:** Lock and unlock your Desi smart doors.
* **Switch:** Control additional Desi smart relays or features.

## Installation

### Method 1: HACS
1. Open HACS in your Home Assistant.
2. Go to "Integrations" -> Click the three dots in the top right -> "Custom repositories".
3. Add the URL of this repository and select "Integration" as the category.
4. Click "Add" and then download the integration.
5. Restart Home Assistant.

### Method 2: Manual
1. Download this repository.
2. Copy the `custom_components/desi` folder to your Home Assistant's `custom_components` directory.
3. Restart Home Assistant.

## Configuration
This integration supports setup via the Home Assistant UI (Config Flow).
1. Go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** and search for "Desi".
3. Enter your login credentials via Desi Login Web page.
