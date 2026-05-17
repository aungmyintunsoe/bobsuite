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
    
    async def synthesize_prd(
        self,
        conversation_data: Dict[str, Any],
        sample_prd: str = "",
        project_name: Optional[str] = None
    ) -> str:
        """
        Synthesize a Product Requirements Document from conversation data.
        
        Args:
            conversation_data: Structured conversation data or transcript
            sample_prd: Sample PRD markdown for reference
            project_name: Name of the project/feature
            
        Returns:
            Generated PRD in markdown format
        """
        prompt = self._build_ideation_prompt(
            conversation_data=conversation_data,
            sample_prd=sample_prd,
            project_name=project_name
        )
        
        # Use higher temperature for creative PRD writing
        return await self.generate_text(
            prompt=prompt,
            temperature=0.4,  # Balanced between creativity and structure
            max_tokens=4000   # PRDs can be lengthy
        )
    
    def _build_ideation_prompt(
        self,
        conversation_data: Dict[str, Any],
        sample_prd: str,
        project_name: Optional[str]
    ) -> str:
        """
        Build a comprehensive prompt for PRD synthesis.
        
        Delegates to the extracted prompts module for better maintainability.
        """
        from lib.ideation.prompts import build_prd_synthesis_prompt
        return build_prd_synthesis_prompt(conversation_data, sample_prd, project_name)
    
    def _format_structured_conversation(self, data: Dict[str, Any]) -> str:
        """Format structured conversation data for the prompt"""
        pillars = data.get("pillars", {})
        lines = []
        
        pillar_titles = {
            "description": "What are we building?",
            "in_scope": "What are we including?",
            "out_scope": "What are we excluding?",
            "implementation": "How might we build it?",
            "acceptance": "How do we know it works?",
            "timeline": "What's the timeline?",
            "resources": "What resources do we need?"
        }
        
        for pillar_id, pillar_data in pillars.items():
            title = pillar_titles.get(pillar_id, pillar_id.replace("_", " ").title())
            answer = pillar_data.get("answer", "")
            
            lines.append(f"\n## {title}")
            lines.append(f"\n{answer}")
            
            # Include follow-up Q&A if present
            follow_ups = pillar_data.get("follow_ups", [])
            if follow_ups:
                lines.append("\n\n**Follow-up Discussion:**")
                for fu in follow_ups:
                    lines.append(f"\nQ: {fu.get('q', '')}")
                    lines.append(f"\nA: {fu.get('a', '')}")
            
            lines.append("\n")
        
        return "".join(lines)
    
    def _format_transcript_conversation(self, data: Dict[str, Any]) -> str:
        """Format transcript conversation data for the prompt"""
        messages = data.get("messages", [])
        lines = ["\n## Conversation Transcript\n"]
        
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            if role == "assistant":
                lines.append(f"\n**Bob:** {content}")
            elif role == "user":
                lines.append(f"\n**Developer:** {content}")
            else:
                lines.append(f"\n**{role.title()}:** {content}")
        
        return "".join(lines)

# Made with Bob
