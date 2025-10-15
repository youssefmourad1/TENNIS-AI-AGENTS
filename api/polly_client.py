"""
Client AWS Polly pour Text-to-Speech
Génération audio à la demande (lazy loading)
"""

import boto3
from typing import Optional
from botocore.exceptions import ClientError


class PollyClient:
    """Client pour AWS Polly (TTS)"""
    
    # Configuration des voix par langue
    VOICES = {
        'fr': {
            'voice_id': 'Lea',
            'engine': 'neural',
            'language_code': 'fr-FR'
        },
        'en': {
            'voice_id': 'Joanna',  # Voix américaine naturelle
            'engine': 'neural',
            'language_code': 'en-US'
        }
    }
    
    def __init__(self, region: str = 'eu-west-1', language: str = 'fr'):
        """
        Initialiser le client Polly
        
        Args:
            region: Région AWS
            language: Langue ('fr' ou 'en')
        """
        self.region = region
        self.language = language.lower()
        self.client = boto3.client('polly', region_name=region)
        
        # Récupérer la configuration de la voix
        self.voice_config = self.VOICES.get(self.language, self.VOICES['fr'])
    
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
            voice_id: ID de la voix (optionnel, utilise la config de langue par défaut)
            engine: Engine (optionnel, utilise la config de langue par défaut)
            
        Returns:
            bytes: Audio MP3 ou None si erreur
        """
        voice_id = voice_id or self.voice_config['voice_id']
        engine = engine or self.voice_config['engine']
        language_code = self.voice_config['language_code']
        
        try:
            response = self.client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine=engine,
                LanguageCode=language_code
            )
            
            return response['AudioStream'].read()
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Polly Error [{error_code}]: {error_message}")
        
        except Exception as e:
            raise Exception(f"Erreur TTS: {str(e)}")
    
    def set_language(self, language: str):
        """
        Changer la langue du TTS
        
        Args:
            language: 'fr' ou 'en'
        """
        self.language = language.lower()
        self.voice_config = self.VOICES.get(self.language, self.VOICES['fr'])
    
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

