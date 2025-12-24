#!/usr/bin/env python3
"""
Manus AI Assistant Addon for Home Assistant
Enables natural language control of smart home devices using Manus AI
"""

import os
import json
import logging
import asyncio
from typing import Any, Dict, Optional
from aiohttp import web
import aiohttp
from datetime import datetime

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'info').upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ManusBridgeAddon:
    """Main addon class that bridges Manus AI with Home Assistant"""

    def __init__(self):
        """Initialize the Manus Bridge addon"""
        self.manus_api_key = os.getenv('MANUS_API_KEY', '')
        self.ha_token = os.getenv('HA_TOKEN', '')
        self.ha_url = os.getenv('HA_URL', 'http://localhost:8123')
        self.enable_voice = os.getenv('ENABLE_VOICE', 'true').lower() == 'true'
        self.enable_automations = os.getenv('ENABLE_AUTOMATIONS', 'true').lower() == 'true'
        self.enable_image_recognition = os.getenv('ENABLE_IMAGE_RECOGNITION', 'true').lower() == 'true'
        
        self.app = web.Application()
        self.setup_routes()
        self.ha_devices = {}
        self.conversation_history = []
        
        logger.info("Manus AI Assistant addon initialized")

    def setup_routes(self):
        """Setup API routes"""
        self.app.router.add_post('/api/control', self.handle_control_command)
        self.app.router.add_post('/api/analyze', self.handle_image_analysis)
        self.app.router.add_get('/api/devices', self.handle_get_devices)
        self.app.router.add_post('/api/automation-suggest', self.handle_automation_suggestion)
        self.app.router.add_get('/api/status', self.handle_status)
        self.app.router.add_post('/api/conversation', self.handle_conversation)

    async def get_ha_devices(self) -> Dict[str, Any]:
        """Fetch all devices and entities from Home Assistant"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.ha_token}',
                    'Content-Type': 'application/json'
                }
                
                # Get all states
                async with session.get(
                    f'{self.ha_url}/api/states',
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        states = await resp.json()
                        self.ha_devices = {
                            state['entity_id']: {
                                'state': state['state'],
                                'attributes': state.get('attributes', {})
                            }
                            for state in states
                        }
                        logger.info(f"Fetched {len(self.ha_devices)} devices from Home Assistant")
                        return self.ha_devices
                    else:
                        logger.error(f"Failed to fetch devices: {resp.status}")
                        return {}
        except Exception as e:
            logger.error(f"Error fetching devices: {e}")
            return {}

    async def call_ha_service(self, domain: str, service: str, entity_id: str, **kwargs) -> bool:
        """Call a Home Assistant service"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.ha_token}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'entity_id': entity_id,
                    **kwargs
                }
                
                async with session.post(
                    f'{self.ha_url}/api/services/{domain}/{service}',
                    headers=headers,
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        logger.info(f"Called service {domain}.{service} on {entity_id}")
                        return True
                    else:
                        logger.error(f"Service call failed: {resp.status}")
                        return False
        except Exception as e:
            logger.error(f"Error calling service: {e}")
            return False

    async def parse_natural_language_command(self, command: str) -> Dict[str, Any]:
        """
        Parse natural language command to Home Assistant actions
        In a real implementation, this would call Manus AI to interpret the command
        """
        command_lower = command.lower()
        
        # Simple pattern matching for demonstration
        # In production, this would use Manus AI for sophisticated NLP
        actions = []
        
        # Light control patterns
        if 'light' in command_lower or 'lights' in command_lower:
            if 'on' in command_lower or 'turn on' in command_lower:
                actions.append({
                    'domain': 'light',
                    'service': 'turn_on',
                    'pattern': 'light'
                })
            elif 'off' in command_lower or 'turn off' in command_lower:
                actions.append({
                    'domain': 'light',
                    'service': 'turn_off',
                    'pattern': 'light'
                })
        
        # Switch control patterns
        if 'switch' in command_lower or 'fan' in command_lower or 'plug' in command_lower:
            if 'on' in command_lower or 'turn on' in command_lower:
                actions.append({
                    'domain': 'switch',
                    'service': 'turn_on',
                    'pattern': 'switch'
                })
            elif 'off' in command_lower or 'turn off' in command_lower:
                actions.append({
                    'domain': 'switch',
                    'service': 'turn_off',
                    'pattern': 'switch'
                })
        
        # Temperature control patterns
        if 'temperature' in command_lower or 'thermostat' in command_lower or 'heat' in command_lower:
            actions.append({
                'domain': 'climate',
                'service': 'set_temperature',
                'pattern': 'climate'
            })
        
        return {
            'command': command,
            'actions': actions,
            'timestamp': datetime.now().isoformat()
        }

    async def handle_control_command(self, request: web.Request) -> web.Response:
        """Handle natural language control commands"""
        try:
            data = await request.json()
            command = data.get('command', '')
            
            if not command:
                return web.json_response(
                    {'error': 'No command provided'},
                    status=400
                )
            
            logger.info(f"Processing command: {command}")
            
            # Fetch current devices
            await self.get_ha_devices()
            
            # Parse the command
            parsed = await self.parse_natural_language_command(command)
            
            # Execute actions
            results = []
            for action in parsed['actions']:
                # Find matching entities
                domain = action['domain']
                matching_entities = [
                    entity_id for entity_id in self.ha_devices.keys()
                    if entity_id.startswith(domain)
                ]
                
                for entity_id in matching_entities:
                    success = await self.call_ha_service(
                        action['domain'],
                        action['service'],
                        entity_id
                    )
                    results.append({
                        'entity_id': entity_id,
                        'action': f"{action['domain']}.{action['service']}",
                        'success': success
                    })
            
            return web.json_response({
                'command': command,
                'results': results,
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            logger.error(f"Error handling control command: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )

    async def handle_image_analysis(self, request: web.Request) -> web.Response:
        """Handle image analysis requests"""
        try:
            data = await request.json()
            entity_id = data.get('entity_id', '')
            prompt = data.get('prompt', '')
            
            if not entity_id or not prompt:
                return web.json_response(
                    {'error': 'Missing entity_id or prompt'},
                    status=400
                )
            
            if not self.enable_image_recognition:
                return web.json_response(
                    {'error': 'Image recognition is disabled'},
                    status=403
                )
            
            logger.info(f"Analyzing image from {entity_id} with prompt: {prompt}")
            
            # In a real implementation, this would:
            # 1. Capture image from camera entity
            # 2. Send to Manus AI for analysis
            # 3. Return results
            
            return web.json_response({
                'entity_id': entity_id,
                'prompt': prompt,
                'analysis': 'Image analysis feature - would be powered by Manus AI',
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )

    async def handle_get_devices(self, request: web.Request) -> web.Response:
        """Get all available devices"""
        try:
            await self.get_ha_devices()
            return web.json_response({
                'devices': self.ha_devices,
                'count': len(self.ha_devices),
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )

    async def handle_automation_suggestion(self, request: web.Request) -> web.Response:
        """Get AI-powered automation suggestions"""
        try:
            data = await request.json()
            trigger = data.get('trigger', '')
            action = data.get('action', '')
            
            if not trigger or not action:
                return web.json_response(
                    {'error': 'Missing trigger or action'},
                    status=400
                )
            
            if not self.enable_automations:
                return web.json_response(
                    {'error': 'Automation suggestions are disabled'},
                    status=403
                )
            
            logger.info(f"Generating automation suggestion for: {trigger} -> {action}")
            
            # In a real implementation, this would call Manus AI
            return web.json_response({
                'trigger': trigger,
                'action': action,
                'suggestion': {
                    'name': 'AI-Generated Automation',
                    'description': 'Automation suggestion from Manus AI',
                    'automation_yaml': '# Generated automation YAML would go here'
                },
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            logger.error(f"Error generating suggestion: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )

    async def handle_conversation(self, request: web.Request) -> web.Response:
        """Handle multi-turn conversations"""
        try:
            data = await request.json()
            message = data.get('message', '')
            
            if not message:
                return web.json_response(
                    {'error': 'No message provided'},
                    status=400
                )
            
            # Add to conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # In a real implementation, this would call Manus AI with conversation context
            response = f"Processing: {message}"
            
            self.conversation_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return web.json_response({
                'message': message,
                'response': response,
                'history_length': len(self.conversation_history),
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )

    async def handle_status(self, request: web.Request) -> web.Response:
        """Get addon status"""
        return web.json_response({
            'status': 'running',
            'version': '1.0.0',
            'features': {
                'voice_control': self.enable_voice,
                'automations': self.enable_automations,
                'image_recognition': self.enable_image_recognition
            },
            'devices_count': len(self.ha_devices),
            'timestamp': datetime.now().isoformat()
        })

    async def start(self):
        """Start the addon server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8123)
        await site.start()
        logger.info("Manus AI Assistant addon started on port 8123")
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Shutting down addon")
            await runner.cleanup()


async def main():
    """Main entry point"""
    addon = ManusBridgeAddon()
    await addon.start()


if __name__ == '__main__':
    asyncio.run(main())
