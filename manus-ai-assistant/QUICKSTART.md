# Manus AI Assistant - Quick Start Guide

Get up and running with the Manus AI Assistant addon in just 5 minutes!

## Prerequisites

- Home Assistant 2024.1 or later
- A Manus account and API key (get one at https://www.manus.im)
- A Home Assistant long-lived access token

## Step 1: Get Your Credentials

### Manus API Key
1. Go to https://www.manus.im
2. Sign in or create an account
3. Navigate to Settings → API Keys
4. Create a new API key and copy it

### Home Assistant Token
1. In Home Assistant, go to **Settings → Users**
2. Click on your user account
3. Scroll to **Long-Lived Access Tokens**
4. Click **Create Token**
5. Give it a name like "Manus Addon"
6. Copy the token (you won't be able to see it again!)

## Step 2: Install the Addon

1. In Home Assistant, go to **Settings → Add-ons → Add-on store**
2. Click the three-dot menu (⋮) in the top right
3. Select **Repositories**
4. Add this URL: `https://github.com/your-username/manus-home-assistant-addons`
5. Click **Add**
6. Search for "Manus AI Assistant"
7. Click on it and then click **Install**

## Step 3: Configure the Addon

1. After installation, click **Configuration**
2. Fill in the required fields:
   - **Manus API Key**: Paste your API key from Step 1
   - **Home Assistant Token**: Paste your token from Step 1
3. Keep other settings as default (or customize as needed)
4. Click **Save**

## Step 4: Start the Addon

1. Click the **Start** button
2. Wait a few seconds for it to start
3. Check the **Logs** tab to confirm it's running
4. You should see: `Manus AI Assistant addon started on port 8123`

## Step 5: Test It Out

### Using the REST API

Open a terminal and test the addon:

```bash
# Get addon status
curl -X GET http://localhost:8123/api/status

# Send a command
curl -X POST http://localhost:8123/api/control \
  -H "Content-Type: application/json" \
  -d '{"command": "Turn on the living room lights"}'

# Get all devices
curl -X GET http://localhost:8123/api/devices
```

### Using Home Assistant Services

In Home Assistant, go to **Developer Tools → Services** and:

1. Select service: `manus_ai_assistant.manus_control`
2. In the YAML editor, enter:
```yaml
command: "Turn on the living room lights"
```
3. Click **Call Service**

## Common Commands

Try these natural language commands:

| Command | Result |
|---------|--------|
| "Turn on the living room lights" | Turns on living room lights |
| "Turn off all lights" | Turns off all lights |
| "Set thermostat to 72 degrees" | Sets temperature |
| "Close the blinds" | Closes window blinds |
| "Movie mode" | Dims lights and sets up theater |
| "Bedtime" | Turns off lights and locks doors |

## Troubleshooting

### Addon won't start
- Check that your API key is valid
- Verify your Home Assistant token is correct
- Check the addon logs for error messages

### Commands not working
- Make sure the device exists in Home Assistant
- Try simpler commands first
- Check that the addon can reach your Home Assistant instance

### Getting help
- Check the full [README.md](README.md) for detailed documentation
- Review [example_automations.yaml](example_automations.yaml) for more examples
- Visit the [Home Assistant community forums](https://community.home-assistant.io)

## Next Steps

Now that you have the basics working:

1. **Create Automations**: Use the addon in your Home Assistant automations
2. **Enable Image Recognition**: Analyze camera feeds with AI
3. **Set Up Voice Control**: Use voice commands to control your home
4. **Explore Advanced Features**: Check out the full README for all capabilities

## Example: Create Your First Automation

1. In Home Assistant, go to **Settings → Automations → Create Automation**
2. Choose **Create new automation**
3. Set up a trigger (e.g., time-based)
4. For the action, select **Call a service**
5. Choose `manus_ai_assistant.manus_control`
6. Enter your command
7. Save and test!

## Tips & Tricks

- **Use natural language**: The addon understands conversational commands
- **Combine actions**: "Turn on lights, close blinds, and set temperature to 70"
- **Context matters**: Previous commands help the AI understand follow-up requests
- **Test first**: Try commands in the developer tools before using in automations

## Getting More Help

- **Full Documentation**: See [README.md](README.md)
- **Developer Guide**: See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Example Automations**: See [example_automations.yaml](example_automations.yaml)
- **Manus Support**: Visit https://www.manus.im/support

Enjoy your AI-powered smart home! 🏠✨
