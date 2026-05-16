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
            model_id: Model identifier (default: granite-13b-chat-v2)
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
    
    async def analyze_code(
        self,
        code: str,
        analysis_type: str = "quality",
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze code using watsonx.ai"""
        prompt = self._build_analysis_prompt(code, analysis_type, language)
        response = await self.generate_text(prompt, temperature=0.3)
        
        return {
            "analysis_type": analysis_type,
            "language": language or "auto-detected",
            "results": response
        }
    
    async def generate_documentation(
        self,
        code: str,
        doc_type: str = "full",
        language: Optional[str] = None
    ) -> str:
        """Generate documentation for code using watsonx.ai"""
        prompt = self._build_documentation_prompt(code, doc_type, language)
        response = await self.generate_text(prompt, temperature=0.5)
        
        return response
    
    def _build_analysis_prompt(
        self,
        code: str,
        analysis_type: str,
        language: Optional[str]
    ) -> str:
        """Build prompt for code analysis"""
        lang_hint = f" ({language})" if language else ""
        
        prompts = {
            "bugs": f"Analyze the following code{lang_hint} for potential bugs and errors:\n\n{code}\n\nProvide a detailed list of bugs found.",
            "vulnerabilities": f"Analyze the following code{lang_hint} for security vulnerabilities:\n\n{code}\n\nProvide a detailed security assessment.",
            "quality": f"Analyze the following code{lang_hint} for code quality issues:\n\n{code}\n\nProvide suggestions for improvement.",
            "all": f"Perform a comprehensive analysis of the following code{lang_hint} including bugs, vulnerabilities, and quality issues:\n\n{code}\n\nProvide a detailed report."
        }
        
        return prompts.get(analysis_type, prompts["all"])
    
    def _build_documentation_prompt(
        self,
        code: str,
        doc_type: str,
        language: Optional[str]
    ) -> str:
        """Build prompt for documentation generation"""
        lang_hint = f" ({language})" if language else ""
        
        prompts = {
            "inline": f"Add inline comments and docstrings to the following code{lang_hint}:\n\n{code}",
            "api": f"Generate API documentation for the following code{lang_hint}:\n\n{code}",
            "readme": f"Generate a README.md section documenting the following code{lang_hint}:\n\n{code}",
            "full": f"Generate comprehensive documentation including inline comments, API docs, and usage examples for the following code{lang_hint}:\n\n{code}"
        }
        
        return prompts.get(doc_type, prompts["full"])

# Made with Bob
