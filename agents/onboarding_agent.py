"""
Tennis AI Onboarding Agent
Agent conversationnel pour l'onboarding des Joueurs et Coachs
Utilise AWS Bedrock (Claude) via API client propre
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.bedrock_client import BedrockClient


class OnboardingAgent:
    """Agent d'onboarding conversationnel pour Tennis AI"""
    
    # Base de connaissances Tennis AI
    TENNIS_AI_KNOWLEDGE = """
# TENNIS AI PLATFORM KNOWLEDGE BASE

## PLATFORM OVERVIEW
Tennis AI est une plateforme de coaching tennis alimentée par IA qui analyse la technique, 
détecte les erreurs et fournit des programmes d'entraînement personnalisés.

## WORKFLOWS UTILISATEUR

### WORKFLOW JOUEUR (Player)
1. Profil (nom, âge, main dominante, objectifs)
2. Configuration matériel (trépied, angle, distance)
3. Test de cadrage (validation IA)
4. Calibration + mode mains libres
5. Vidéo d'évaluation (service + coup droit/revers)
6. Analyse initiale (métriques Tennis AI)
7. Détection niveau (débutant/intermédiaire/avancé)
8. Programme d'entrée (drills personnalisés)
9. Upsell (premium après moment de valeur)

### WORKFLOW COACH (Coach)
1. Profil coach (nom, club, rôle)
2. Liaison élèves (codes invitation)
3. Configuration court (angle, hauteur)
4. Validation court (test cadrage)
5. Demo multi-élèves
6. Synthèse multi-élèves
7. Demo programmes
8. Intro dashboard

## MÉTRIQUE CLÉS
- Stance (position pieds)
- Grip (prise raquette)
- Contact point (point d'impact)
- Follow-through (fin de geste)
- Body rotation (rotation corps)

RÈGLE D'OR: Une seule erreur à la fois!
"""
    
    # Étapes pour chaque type d'utilisateur
    PLAYER_STAGES = [
        "bienvenue", "profil", "objectifs", "configuration_matériel",
        "test_cadrage", "demo_calibration", "video_evaluation", "analyse",
        "detection_niveau", "proposition_programme", "upsell", "terminé"
    ]
    
    COACH_STAGES = [
        "bienvenue", "profil_coach", "préférences", "liaison_élèves",
        "configuration_court", "validation_court", "demo_multi_élèves",
        "demo_synthèse", "demo_programmes", "intro_dashboard", "terminé"
    ]
    
    def __init__(
        self,
        user_type: str,
        region: str = 'eu-west-1',
        model_id: str = 'anthropic.claude-3-haiku-20240307-v1:0'
    ):
        """
        Initialiser l'agent d'onboarding
        
        Args:
            user_type: Type d'utilisateur ('player' ou 'coach')
            region: Région AWS
            model_id: ID du modèle Claude
        """
        self.user_type = user_type.lower()
        self.bedrock = BedrockClient(region=region, model_id=model_id)
        
        # État de la conversation
        self.conversation_history = []
        self.current_stage = "bienvenue"
        self.user_profile = {}
        
        # Étapes selon le type d'utilisateur
        self.stages = self.PLAYER_STAGES if self.user_type == 'player' else self.COACH_STAGES
    
    def _build_system_prompt(self) -> str:
        """Construire le prompt système avec la connaissance Tennis AI"""
        user_type_fr = "Joueur" if self.user_type == "player" else "Coach"
        
        return f"""Tu es CoachBot, l'assistant IA d'onboarding pour la plateforme Tennis AI.

TON RÔLE:
Tu guides les nouveaux {user_type_fr}s à travers le processus complet d'onboarding 
de manière chaleureuse, conversationnelle et professionnelle. Tu es un coach de tennis expert.

IMPORTANT: RÉPONDS TOUJOURS EN FRANÇAIS!

CONTEXTE ACTUEL:
- Type d'utilisateur: {user_type_fr}
- Étape actuelle: {self.current_stage}
- Profil collecté: {json.dumps(self.user_profile, indent=2, ensure_ascii=False)}

TON STYLE:
- Chaleureux et encourageant
- 2-4 phrases par réponse
- UNE question claire à la fois
- Utilise la terminologie tennis appropriée
- Sois enthousiaste!

ÉTAPES D'ONBOARDING:
{' → '.join(self.stages)}

{self.TENNIS_AI_KNOWLEDGE}

Basé sur l'étape actuelle et le message de l'utilisateur, continue la conversation naturellement.
Avance à travers le flux d'onboarding étape par étape.

RAPPEL: Tu es un coach IA, pas juste un bot de formulaire. Rends ça engageant!
RÉPONDS TOUJOURS EN FRANÇAIS!"""
    
    def start_conversation(self) -> str:
        """
        Démarrer la conversation avec un message de bienvenue adapté au type d'utilisateur
        
        Returns:
            str: Message de bienvenue
        """
        if self.user_type == "player":
            welcome = """Bienvenue sur Tennis AI! 🎾

Je suis CoachBot, ton assistant personnel pour améliorer ton jeu. 
Je vais t'accompagner pas à pas pour analyser ta technique et créer ton premier programme d'entraînement personnalisé.

Pour commencer, dis-moi comment tu t'appelles et quel âge tu as?"""
        else:
            welcome = """Bienvenue sur Tennis AI! 🎾

Je suis CoachBot, ton assistant pour gérer et analyser tes élèves.
Je vais te guider pour configurer ton espace coach et découvrir tous les outils disponibles.

Pour commencer, dis-moi ton nom et le nom de ton club?"""
        
        return welcome
    
    def chat(self, user_message: str) -> str:
        """
        Envoyer un message et obtenir la réponse
        
        Args:
            user_message: Message de l'utilisateur
            
        Returns:
            str: Réponse de l'agent
        """
        # Ajouter le message utilisateur à l'historique
        self.conversation_history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_message}]
        })
        
        # Construire le prompt système
        system_prompt = self._build_system_prompt()
        
        # Obtenir la réponse de Claude
        try:
            response = self.bedrock.chat(
                messages=self.conversation_history,
                system_prompt=system_prompt,
                max_tokens=1024,
                temperature=0.7
            )
            
            # Ajouter la réponse à l'historique
            self.conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": response}]
            })
            
            # Mise à jour automatique de l'étape (logique simplifiée)
            self._update_stage_if_needed(user_message, response)
            
            return response
            
        except Exception as e:
            return f"Désolé, une erreur s'est produite: {str(e)}"
    
    def _update_stage_if_needed(self, user_message: str, response: str):
        """
        Mettre à jour l'étape si nécessaire (logique simplifiée)
        
        Args:
            user_message: Message utilisateur
            response: Réponse de l'agent
        """
        # Logique simple: avancer après quelques échanges
        # Dans une vraie implémentation, utiliser l'analyse sémantique
        current_index = self.stages.index(self.current_stage)
        
        # Avancer si on a assez d'informations
        if len(self.conversation_history) > (current_index + 1) * 4:
            if current_index < len(self.stages) - 1:
                self.current_stage = self.stages[current_index + 1]
    
    def get_current_stage(self) -> str:
        """Obtenir l'étape actuelle"""
        return self.current_stage
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Obtenir le profil utilisateur"""
        return self.user_profile
    
    def save_session(self, file_path: Optional[str] = None):
        """
        Sauvegarder la session
        
        Args:
            file_path: Chemin du fichier de sauvegarde
        """
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"sessions/session_{self.user_type}_{timestamp}.json"
        
        session_data = {
            "user_type": self.user_type,
            "current_stage": self.current_stage,
            "user_profile": self.user_profile,
            "conversation_history": self.conversation_history,
            "timestamp": datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

