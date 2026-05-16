"""
IBM watsonx.ai Client
Handles API connections and model interactions using REST API
"""

import os
import time
from typing import Optional, Dict, Any
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WatsonxClient:
    """Client for interacting with IBM watsonx.ai via REST API"""
    
    def __init__(self):
        """Initialize the watsonx client with credentials from .env"""
        self.api_key = os.getenv("IBM_API_KEY")
        self.project_id = os.getenv("PROJECT_ID")
        self.watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.iam_url = "https://iam.cloud.ibm.com/identity/token"
        
        self._access_token = None
        self._token_expires = 0
        
        if not self.api_key or not self.project_id:
            raise ValueError(
                "Missing required environment variables. "
                "Please set IBM_API_KEY and PROJECT_ID in mcp_server/.env"
            )
    
    async def _get_token(self) -> str:
        """Get IAM token, caching it if still valid"""
        if self._access_token and time.time() < self._token_expires:
            return self._access_token
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.iam_url,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey", 
                    "apikey": self.api_key
                }
            )
            if response.status_code != 200:
                raise RuntimeError(f"Failed to authenticate with IBM Cloud: {response.text}")
                
            data = response.json()
            self._access_token = data["access_token"]
            self._token_expires = time.time() + data.get("expires_in", 3600) - 60
            return self._access_token

    async def generate_text(
        self,
        prompt: str,
        model_id: str = "ibm/granite-4-h-small",
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using watsonx.ai REST API
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional model parameters
            
        Returns:
            Generated text response
        """
        token = await self._get_token()
        
        url = f"{self.watsonx_url}/ml/v1/text/generation?version=2023-05-29"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model_id": model_id,
            "input": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                **kwargs
            },
            "project_id": self.project_id
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code != 200:
                    raise RuntimeError(f"watsonx.ai API Error: {response.status_code} - {response.text}")
                    
                data = response.json()
                return data["results"][0]["generated_text"]
                
        except Exception as e:
            raise RuntimeError(f"Error generating text with watsonx.ai: {str(e)}")

# Made with Bob
