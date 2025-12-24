#!/usr/bin/env python3
"""
Manus Integration Module
Provides easy-to-use Python interface for integrating Manus with Home Assistant
"""

import aiohttp
import asyncio
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Device:
    """Represents a Home Assistant device"""
    entity_id: str
    state: str
    attributes: Dict[str, Any]
    
    def __str__(self) -> str:
        return f"{self.entity_id}: {self.state}"


@dataclass
class CommandResult:
    """Result of executing a command"""
    command: str
    success: bool
    results: List[Dict[str, Any]]
    timestamp: str
    error: Optional[str] = None


class ManusBridge:
    """Client for communicating with the Manus addon"""
    
    def __init__(self, addon_url: str = 'http://localhost:8123', timeout: int = 30):
        """
        Initialize the Manus Bridge client
        
        Args:
            addon_url: URL of the Manus addon API
            timeout: Request timeout in seconds
        """
        self.addon_url = addon_url.rstrip('/')
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _ensure_session(self):
        """Ensure session is initialized"""
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
    
    async def control(self, command: str) -> CommandResult:
        """
        Send a natural language command to control devices
        
        Args:
            command: Natural language command (e.g., "Turn on the living room lights")
        
        Returns:
            CommandResult with execution results
        """
        await self._ensure_session()
        
        try:
            async with self.session.post(
                f'{self.addon_url}/api/control',
                json={'command': command}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return CommandResult(
                        command=command,
                        success=True,
                        results=data.get('results', []),
                        timestamp=data.get('timestamp', datetime.now().isoformat())
                    )
                else:
                    error_data = await resp.json()
                    return CommandResult(
                        command=command,
                        success=False,
                        results=[],
                        timestamp=datetime.now().isoformat(),
                        error=error_data.get('error', f'HTTP {resp.status}')
                    )
        except Exception as e:
            logger.error(f"Error sending control command: {e}")
            return CommandResult(
                command=command,
                success=False,
                results=[],
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )
    
    async def analyze_image(self, entity_id: str, prompt: str) -> Dict[str, Any]:
        """
        Analyze an image from a camera entity
        
        Args:
            entity_id: Camera entity ID (e.g., "camera.living_room")
            prompt: What to analyze in the image
        
        Returns:
            Analysis results
        """
        await self._ensure_session()
        
        try:
            async with self.session.post(
                f'{self.addon_url}/api/analyze',
                json={'entity_id': entity_id, 'prompt': prompt}
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    error_data = await resp.json()
                    return {'error': error_data.get('error', f'HTTP {resp.status}')}
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {'error': str(e)}
    
    async def get_devices(self) -> List[Device]:
        """
        Get all available devices
        
        Returns:
            List of Device objects
        """
        await self._ensure_session()
        
        try:
            async with self.session.get(f'{self.addon_url}/api/devices') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    devices = []
                    for entity_id, device_data in data.get('devices', {}).items():
                        devices.append(Device(
                            entity_id=entity_id,
                            state=device_data.get('state', 'unknown'),
                            attributes=device_data.get('attributes', {})
                        ))
                    return devices
                else:
                    logger.error(f"Failed to get devices: HTTP {resp.status}")
                    return []
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
            return []
    
    async def suggest_automation(self, trigger: str, action: str) -> Dict[str, Any]:
        """
        Get AI-powered automation suggestions
        
        Args:
            trigger: Automation trigger description
            action: Automation action description
        
        Returns:
            Automation suggestion
        """
        await self._ensure_session()
        
        try:
            async with self.session.post(
                f'{self.addon_url}/api/automation-suggest',
                json={'trigger': trigger, 'action': action}
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    error_data = await resp.json()
                    return {'error': error_data.get('error', f'HTTP {resp.status}')}
        except Exception as e:
            logger.error(f"Error suggesting automation: {e}")
            return {'error': str(e)}
    
    async def send_message(self, message: str) -> Dict[str, Any]:
        """
        Send a message for multi-turn conversation
        
        Args:
            message: Message to send
        
        Returns:
            Conversation response
        """
        await self._ensure_session()
        
        try:
            async with self.session.post(
                f'{self.addon_url}/api/conversation',
                json={'message': message}
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    error_data = await resp.json()
                    return {'error': error_data.get('error', f'HTTP {resp.status}')}
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {'error': str(e)}
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get addon status
        
        Returns:
            Status information
        """
        await self._ensure_session()
        
        try:
            async with self.session.get(f'{self.addon_url}/api/status') as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {'error': f'HTTP {resp.status}'}
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {'error': str(e)}


# Synchronous wrapper for easier use in non-async code
class ManusBridgeSync:
    """Synchronous wrapper for ManusBridge"""
    
    def __init__(self, addon_url: str = 'http://localhost:8123', timeout: int = 30):
        """Initialize the synchronous bridge"""
        self.addon_url = addon_url
        self.timeout = timeout
        self._bridge = ManusBridge(addon_url, timeout)
    
    def control(self, command: str) -> CommandResult:
        """Send a control command (synchronous)"""
        return asyncio.run(self._bridge.control(command))
    
    def analyze_image(self, entity_id: str, prompt: str) -> Dict[str, Any]:
        """Analyze an image (synchronous)"""
        return asyncio.run(self._bridge.analyze_image(entity_id, prompt))
    
    def get_devices(self) -> List[Device]:
        """Get devices (synchronous)"""
        return asyncio.run(self._bridge.get_devices())
    
    def suggest_automation(self, trigger: str, action: str) -> Dict[str, Any]:
        """Get automation suggestions (synchronous)"""
        return asyncio.run(self._bridge.suggest_automation(trigger, action))
    
    def send_message(self, message: str) -> Dict[str, Any]:
        """Send a message (synchronous)"""
        return asyncio.run(self._bridge.send_message(message))
    
    def get_status(self) -> Dict[str, Any]:
        """Get status (synchronous)"""
        return asyncio.run(self._bridge.get_status())


# Example usage
if __name__ == '__main__':
    # Async example
    async def async_example():
        async with ManusBridge() as bridge:
            # Get status
            status = await bridge.get_status()
            print(f"Addon Status: {status}")
            
            # Get devices
            devices = await bridge.get_devices()
            print(f"Found {len(devices)} devices")
            
            # Send a command
            result = await bridge.control("Turn on the living room lights")
            print(f"Command result: {result}")
    
    # Sync example
    def sync_example():
        bridge = ManusBridgeSync()
        
        # Get status
        status = bridge.get_status()
        print(f"Addon Status: {status}")
        
        # Send a command
        result = bridge.control("Turn on the living room lights")
        print(f"Command result: {result}")
    
    # Run async example
    print("=== Async Example ===")
    asyncio.run(async_example())
    
    print("\n=== Sync Example ===")
    sync_example()
