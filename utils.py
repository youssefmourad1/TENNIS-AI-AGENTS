"""
Utilities pour Tennis AI
Fonctions utilitaires générales
"""

import os
from typing import Optional


def get_aws_credentials() -> dict:
    """
    Récupérer les credentials AWS depuis les variables d'environnement
    
    Returns:
        dict: Credentials AWS ou None si non trouvés
    """
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    session_token = os.getenv('AWS_SESSION_TOKEN')
    
    if not access_key or not secret_key:
        return None
    
    credentials = {
        'aws_access_key_id': access_key,
        'aws_secret_access_key': secret_key
    }
    
    if session_token:
        credentials['aws_session_token'] = session_token
    
    return credentials


def validate_user_type(user_type: str) -> bool:
    """
    Valider le type d'utilisateur
    
    Args:
        user_type: Type d'utilisateur (player ou coach)
        
    Returns:
        bool: True si valide
    """
    return user_type.lower() in ['player', 'coach']


def format_chat_message(role: str, content: str) -> dict:
    """
    Formater un message pour l'historique de chat
    
    Args:
        role: Rôle (user ou assistant)
        content: Contenu du message
        
    Returns:
        dict: Message formaté
    """
    return {
        'role': role,
        'content': content
    }

