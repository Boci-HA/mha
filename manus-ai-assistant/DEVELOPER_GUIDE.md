# Manus AI Assistant Addon - Developer Guide

This guide provides information for developers who want to extend, modify, or contribute to the Manus AI Assistant addon.

## Project Structure

```
manus_addon/
├── addon_config.json          # Addon configuration and metadata
├── main.py                    # Main addon application
├── manus_integration.py       # Python client library
├── Dockerfile                 # Container configuration
├── requirements.txt           # Python dependencies
├── README.md                  # User documentation
├── DEVELOPER_GUIDE.md         # This file
└── example_automations.yaml   # Example Home Assistant automations
```

## Architecture Overview

The addon follows a modular architecture:

### Core Components

**ManusBridgeAddon (main.py)**
- Main application class that manages the addon lifecycle
- Handles HTTP API endpoints
- Manages Home Assistant integration
- Coordinates with Manus AI services

**API Server**
- Built on aiohttp for async HTTP handling
- Exposes RESTful endpoints for Home Assistant integration
- Handles concurrent requests efficiently

**Home Assistant Integration**
- Uses Home Assistant REST API for device control
- Manages authentication via long-lived tokens
- Fetches device states and executes services

**Manus Integration**
- Communicates with Manus AI services
- Handles natural language processing
- Manages image recognition and analysis

## Setting Up Development Environment

### Prerequisites
- Python 3.9+
- Docker (for testing in addon environment)
- Home Assistant instance (for testing)
- Manus API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/manus-home-assistant-addons.git
cd manus_addon
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8
```

4. Create a `.env` file for local testing:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Development Workflow

### Running Locally

For local development without Docker:

```bash
export MANUS_API_KEY="your-key"
export HA_TOKEN="your-token"
export HA_URL="http://localhost:8123"
python3 main.py
```

The addon will start on `http://localhost:8123`

### Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. tests/
```

### Code Quality

Format code with Black:
```bash
black .
```

Check code style:
```bash
flake8 .
```

## API Development

### Adding New Endpoints

To add a new API endpoint:

1. Create a handler method in `ManusBridgeAddon`:

```python
async def handle_new_feature(self, request: web.Request) -> web.Response:
    """Handle new feature request"""
    try:
        data = await request.json()
        # Process request
        return web.json_response({'result': 'success'})
    except Exception as e:
        logger.error(f"Error: {e}")
        return web.json_response({'error': str(e)}, status=500)
```

2. Register the route in `setup_routes()`:

```python
self.app.router.add_post('/api/new-feature', self.handle_new_feature)
```

3. Document the endpoint in README.md

### Request/Response Format

All endpoints use JSON for request and response bodies:

**Request:**
```json
{
  "parameter1": "value1",
  "parameter2": "value2"
}
```

**Response (Success):**
```json
{
  "result": "success",
  "data": {},
  "timestamp": "2025-12-22T15:30:00"
}
```

**Response (Error):**
```json
{
  "error": "Error description",
  "timestamp": "2025-12-22T15:30:00"
}
```

## Extending the Integration

### Custom Command Parsers

To add custom command parsing logic:

1. Create a new parser class:

```python
class CustomCommandParser:
    def parse(self, command: str) -> Dict[str, Any]:
        # Parse logic here
        return {
            'domain': 'light',
            'service': 'turn_on',
            'entities': ['light.living_room']
        }
```

2. Integrate into `parse_natural_language_command()`:

```python
async def parse_natural_language_command(self, command: str) -> Dict[str, Any]:
    parser = CustomCommandParser()
    return parser.parse(command)
```

### Adding New Services

To add support for new Home Assistant services:

1. Extend the `call_ha_service()` method with service-specific logic
2. Update the command parser to recognize the new service
3. Add tests for the new service

## Testing

### Unit Tests

Example unit test:

```python
import pytest
from main import ManusBridgeAddon

@pytest.mark.asyncio
async def test_parse_light_command():
    addon = ManusBridgeAddon()
    result = await addon.parse_natural_language_command("Turn on the lights")
    
    assert len(result['actions']) > 0
    assert result['actions'][0]['domain'] == 'light'
    assert result['actions'][0]['service'] == 'turn_on'
```

### Integration Tests

Test with actual Home Assistant:

```python
@pytest.mark.asyncio
async def test_control_light_integration():
    addon = ManusBridgeAddon()
    await addon.get_ha_devices()
    
    result = await addon.handle_control_command(
        MockRequest({'command': 'Turn on living room light'})
    )
    
    assert result.status == 200
```

## Performance Optimization

### Caching

Implement device caching to reduce API calls:

```python
class DeviceCache:
    def __init__(self, ttl: int = 60):
        self.cache = {}
        self.ttl = ttl
        self.last_update = 0
    
    async def get_devices(self, addon):
        if self._is_expired():
            self.cache = await addon.get_ha_devices()
            self.last_update = time.time()
        return self.cache
```

### Async Optimization

Use asyncio properly for concurrent operations:

```python
# Good: Concurrent requests
results = await asyncio.gather(
    self.call_ha_service(domain1, service1, entity1),
    self.call_ha_service(domain2, service2, entity2),
    return_exceptions=True
)

# Bad: Sequential requests
await self.call_ha_service(domain1, service1, entity1)
await self.call_ha_service(domain2, service2, entity2)
```

## Debugging

### Enable Debug Logging

```bash
export LOG_LEVEL=debug
python3 main.py
```

### Using Python Debugger

```python
import pdb

async def handle_control_command(self, request):
    pdb.set_trace()  # Execution will pause here
    # ... rest of code
```

### Logging Best Practices

```python
# Good logging
logger.info(f"Processing command: {command}")
logger.error(f"Failed to call service: {e}", exc_info=True)

# Bad logging
print("Processing command")  # Don't use print
logger.info("error")  # Vague message
```

## Building Docker Image

Build the addon image:

```bash
docker build -t manus-addon:1.0.0 .
```

Run the image:

```bash
docker run -e MANUS_API_KEY="your-key" \
           -e HA_TOKEN="your-token" \
           -e HA_URL="http://host.docker.internal:8123" \
           -p 8123:8123 \
           manus-addon:1.0.0
```

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for all classes and public methods
- Keep functions focused and under 50 lines when possible

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add image recognition support
fix: Resolve timeout issue in device fetching
docs: Update API documentation
test: Add tests for command parsing
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and commit
4. Push to your fork: `git push origin feature/my-feature`
5. Create a pull request with description

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance impact assessed

## Troubleshooting Development

### Common Issues

**Import errors:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

**Port already in use:**
```bash
# Find process using port 8123
lsof -i :8123
# Kill the process
kill -9 <PID>
```

**Home Assistant connection issues:**
- Verify HA_URL is correct
- Check HA_TOKEN is valid (not expired)
- Ensure Home Assistant is running and accessible

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [Python asyncio Guide](https://docs.python.org/3/library/asyncio.html)
- [Manus API Documentation](https://www.manus.im/docs)

## License

This addon is licensed under the MIT License. See LICENSE file for details.

## Support

For development questions or issues:
- Open an issue on GitHub
- Join the Home Assistant community forums
- Check existing documentation and examples
