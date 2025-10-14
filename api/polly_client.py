"""
Client AWS Polly pour Text-to-Speech
Génération audio à la demande (lazy loading)
"""

import boto3
from typing import Optional
from botocore.exceptions import ClientError


class PollyClient:
    """Client pour AWS Polly (TTS)"""
    
    def __init__(self, region: str = 'eu-west-1'):
        """
        Initialiser le client Polly
        
        Args:
            region: Région AWS
        """
        self.region = region
        self.client = boto3.client('polly', region_name=region)
        self.default_voice = 'Lea'  # Voix française naturelle
        self.default_engine = 'neural'
    
    def synthesize(
        self,
        text: str,
        voice_id: Optional[str] = None,
        engine: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Convertir du texte en audio (LAZY - appelé seulement au clic)
        
        Args:
            text: Texte à synthétiser
            voice_id: ID de la voix (défaut: Lea)
            engine: Engine (neural ou standard)
            
        Returns:
            bytes: Audio MP3 ou None si erreur
        """
        voice_id = voice_id or self.default_voice
        engine = engine or self.default_engine
        
        try:
            response = self.client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine=engine,
                LanguageCode='fr-FR'
            )
            
            return response['AudioStream'].read()
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Polly Error [{error_code}]: {error_message}")
        
        except Exception as e:
            raise Exception(f"Erreur TTS: {str(e)}")
    
    def get_available_voices(self, language_code: str = 'fr-FR') -> list:
        """
        Lister les voix disponibles
        
        Args:
            language_code: Code de langue
            
        Returns:
            list: Liste des voix
        """
        try:
            response = self.client.describe_voices(LanguageCode=language_code)
            return response['Voices']
        except Exception as e:
            print(f"Erreur récupération voix: {e}")
            return []

