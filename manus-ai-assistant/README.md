# Manus AI Assistant Addon for Home Assistant

A powerful Home Assistant addon that integrates Manus AI to enable natural language control of your smart home with advanced AI capabilities.

## Overview

The Manus AI Assistant addon brings cutting-edge AI capabilities to Home Assistant, allowing you to control your smart home using natural language commands. It leverages Manus's advanced AI to understand context, handle complex requests, and provide intelligent automation suggestions.

## Features

### Natural Language Control
Control your smart home devices using conversational commands instead of traditional automation rules. The addon understands context and can handle complex, multi-step commands.

**Examples:**
- "Turn on the living room lights"
- "Set the thermostat to 72 degrees"
- "Turn off all lights except the bedroom"

### Voice Control
Enable voice commands through Manus AI integration. The addon supports streaming audio for faster response times and can maintain conversation context across multiple turns.

### Image Recognition
Analyze images from your security cameras using Manus AI's image recognition capabilities. Perfect for:
- Detecting motion or specific objects
- Counting items in a scene
- Identifying people or animals
- Analyzing room conditions

### AI-Powered Automation Suggestions
Get intelligent suggestions for new automations based on your usage patterns. The addon analyzes your existing automations and suggests improvements.

### Multi-Turn Conversations
Maintain conversation context across multiple messages. The addon remembers previous commands and can handle follow-up requests naturally.

## Installation

### Prerequisites
- Home Assistant 2024.1 or later
- A Manus API key (obtain from https://www.manus.im)
- A Home Assistant long-lived access token

### Steps

1. Add the Manus addon repository to Home Assistant:
   - Go to **Settings → Add-ons → Add-on store**
   - Click the three-dot menu and select **Repositories**
   - Add: `https://github.com/your-username/manus-home-assistant-addons`

2. Install the Manus AI Assistant addon:
   - Search for "Manus AI Assistant"
   - Click **Install**

3. Configure the addon:
   - Go to the addon page
   - Click **Configuration**
   - Enter your Manus API key and Home Assistant token
   - Adjust feature toggles as needed
   - Click **Save**

4. Start the addon:
   - Click **Start**
   - Check the logs to confirm it's running

## Configuration

### Required Settings

**Manus API Key**: Your authentication key for Manus AI services. Obtain this from your Manus account dashboard.

**Home Assistant Token**: A long-lived access token for Home Assistant. Create one in **Settings → Users → Create Token**.

### Optional Settings

**Home Assistant URL**: The URL of your Home Assistant instance (default: `http://localhost:8123`). Change this if your HA instance is on a different host.

**Enable Voice Control**: Toggle voice command support (default: enabled)

**Enable Automations**: Toggle AI-powered automation suggestions (default: enabled)

**Enable Image Recognition**: Toggle image analysis from cameras (default: enabled)

**Log Level**: Set logging verbosity - `debug`, `info`, `warning`, or `error` (default: `info`)

## API Endpoints

The addon exposes the following REST API endpoints:

### POST `/api/control`
Send a natural language command to control devices.

**Request:**
```json
{
  "command": "Turn on the living room lights"
}
```

**Response:**
```json
{
  "command": "Turn on the living room lights",
  "results": [
    {
      "entity_id": "light.living_room",
      "action": "light.turn_on",
      "success": true
    }
  ],
  "timestamp": "2025-12-22T15:30:00"
}
```

### POST `/api/conversation`
Send a message for multi-turn conversation with context.

**Request:**
```json
{
  "message": "What's the current temperature?"
}
```

**Response:**
```json
{
  "message": "What's the current temperature?",
  "response": "The current temperature is 72°F",
  "history_length": 2,
  "timestamp": "2025-12-22T15:30:00"
}
```

### POST `/api/analyze`
Analyze an image from a camera entity.

**Request:**
```json
{
  "entity_id": "camera.living_room",
  "prompt": "Count the number of people in the room"
}
```

**Response:**
```json
{
  "entity_id": "camera.living_room",
  "prompt": "Count the number of people in the room",
  "analysis": "There are 2 people in the room",
  "timestamp": "2025-12-22T15:30:00"
}
```

### POST `/api/automation-suggest`
Get AI-powered suggestions for new automations.

**Request:**
```json
{
  "trigger": "When motion is detected in the living room",
  "action": "Turn on lights"
}
```

**Response:**
```json
{
  "trigger": "When motion is detected in the living room",
  "action": "Turn on lights",
  "suggestion": {
    "name": "Motion-Activated Lights",
    "description": "Automatically turns on lights when motion is detected",
    "automation_yaml": "..."
  },
  "timestamp": "2025-12-22T15:30:00"
}
```

### GET `/api/devices`
Get a list of all available devices and their current states.

**Response:**
```json
{
  "devices": {
    "light.living_room": {
      "state": "on",
      "attributes": {
        "brightness": 255,
        "color_temp": 4000
      }
    },
    "switch.kitchen": {
      "state": "off",
      "attributes": {}
    }
  },
  "count": 2,
  "timestamp": "2025-12-22T15:30:00"
}
```

### GET `/api/status`
Get the current status of the addon.

**Response:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "features": {
    "voice_control": true,
    "automations": true,
    "image_recognition": true
  },
  "devices_count": 42,
  "timestamp": "2025-12-22T15:30:00"
}
```

## Home Assistant Services

The addon registers the following Home Assistant services:

### `manus_ai_assistant.manus_control`
Send a natural language command to control your home.

**Service data:**
```yaml
command: "Turn on the living room lights"
```

### `manus_ai_assistant.manus_analyze_image`
Analyze an image from a camera.

**Service data:**
```yaml
entity_id: camera.living_room
prompt: "Count the number of people in the room"
```

## Usage Examples

### Example 1: Simple Light Control
```yaml
automation:
  - alias: "Voice Control Lights"
    trigger:
      platform: webhook
      webhook_id: voice_command
    action:
      service: manus_ai_assistant.manus_control
      data:
        command: "Turn on the bedroom lights"
```

### Example 2: Image Analysis Automation
```yaml
automation:
  - alias: "Analyze Camera Feed"
    trigger:
      platform: time_pattern
      minutes: "/5"
    action:
      service: manus_ai_assistant.manus_analyze_image
      data:
        entity_id: camera.front_door
        prompt: "Is there a person at the front door?"
```

### Example 3: Complex Multi-Device Control
```yaml
automation:
  - alias: "Evening Mode"
    trigger:
      platform: sun
      event: sunset
    action:
      service: manus_ai_assistant.manus_control
      data:
        command: "Set evening mode - dim all lights to 30%, close blinds, and set thermostat to 68 degrees"
```

## Troubleshooting

### Addon won't start
- Check that your Manus API key is valid
- Verify your Home Assistant token is correct
- Check the addon logs for detailed error messages

### Commands not working
- Ensure the addon can reach your Home Assistant instance
- Verify that the entities you're trying to control exist
- Check that your Home Assistant token has the necessary permissions

### Image analysis not working
- Ensure image recognition is enabled in the addon settings
- Verify that the camera entity exists and is accessible
- Check that your Manus API key has image analysis permissions

### High latency
- Check your network connection
- Verify that the addon and Home Assistant are on the same network
- Consider enabling caching for frequently used commands

## Advanced Configuration

### Custom Entity Mapping
You can create custom mappings for entity names to improve command recognition:

```yaml
entity_mapping:
  "living room lights": "light.living_room"
  "kitchen fan": "switch.kitchen_fan"
  "bedroom temperature": "climate.bedroom"
```

### Command Aliases
Create aliases for common commands:

```yaml
command_aliases:
  "movie time": "Turn on TV, dim lights to 10%, close blinds"
  "bedtime": "Turn off all lights, lock doors, set thermostat to 65"
```

## Privacy & Security

- **Local Processing**: Commands are processed locally when possible
- **Encrypted Communication**: All communication with Manus is encrypted
- **Token Security**: Your Home Assistant token is stored securely and never shared
- **Data Control**: You have full control over what data is sent to Manus AI

## Performance Considerations

- The addon uses approximately 50-100 MB of RAM
- API response times typically range from 100ms to 2 seconds depending on command complexity
- Image analysis may take 2-5 seconds depending on image size and complexity

## Support & Feedback

For issues, feature requests, or general support:
- Open an issue on the [GitHub repository](https://github.com/your-username/manus-home-assistant-addons)
- Visit the [Manus website](https://www.manus.im)
- Check the [Home Assistant community forums](https://community.home-assistant.io)

## License

This addon is licensed under the MIT License. See LICENSE file for details.

## Changelog

### Version 1.0.0 (Initial Release)
- Natural language device control
- Voice command support
- Image recognition capabilities
- AI-powered automation suggestions
- Multi-turn conversation support
- REST API for integration with other tools
