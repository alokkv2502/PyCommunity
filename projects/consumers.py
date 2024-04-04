# your_app/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# Use asyncio for asynchronous execution
import asyncio

class PythonTerminalConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        code = text_data_json['code']
        
        # Placeholder for code execution - use safe execution environment
        output = await self.run_code(code)

        await self.send(text_data=json.dumps({
            'output': output
        }))
    
    async def run_code(self, code):
        # Safely execute the Python code and return output
        # IMPORTANT: Implement code execution with security and resource constraints
        return "Executed: " + code
