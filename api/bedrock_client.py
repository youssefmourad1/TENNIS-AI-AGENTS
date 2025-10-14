"""
Client AWS Bedrock pour Claude
Gère les appels à l'API Claude via Bedrock
"""

import boto3
import json
from typing import List, Dict, Any, Optional
from botocore.exceptions import ClientError


class BedrockClient:
    """Client pour AWS Bedrock (Claude)"""
    
    def __init__(self, region: str = 'eu-west-1', model_id: str = 'anthropic.claude-3-haiku-20240307-v1:0'):
        """
        Initialiser le client Bedrock
        
        Args:
            region: Région AWS
            model_id: ID du modèle Claude
        """
        self.region = region
        self.model_id = model_id
        self.client = boto3.client('bedrock-runtime', region_name=region)
    
    def chat(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Envoyer un message à Claude
        
        Args:
            messages: Historique des messages
            system_prompt: Prompt système
            max_tokens: Nombre max de tokens
            temperature: Température
            
        Returns:
            str: Réponse de Claude ou None si erreur
        """
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": messages
        }
        
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Bedrock Error [{error_code}]: {error_message}")
        
        except Exception as e:
            raise Exception(f"Erreur inattendue: {str(e)}")

