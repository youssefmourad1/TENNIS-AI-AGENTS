"""
Tennis AI Onboarding Agent V2
A conversational AI agent for onboarding Players and Coaches to Tennis AI platform.
Uses AWS Bedrock (Claude 3 Haiku) for natural conversation flow.
"""

import os
import json
import boto3
from typing import Dict, Any, List, Optional
from datetime import datetime
from botocore.exceptions import ClientError


class TennisAIOnboardingAgent:
    """
    Conversational onboarding agent for Tennis AI platform.
    Guides users through complete onboarding: profile setup, equipment calibration,
    evaluation, and initial program creation.
    """
    
    # Comprehensive Tennis AI Knowledge Base
    TENNIS_AI_KNOWLEDGE = """
# TENNIS AI PLATFORM KNOWLEDGE BASE

## PLATFORM OVERVIEW
Tennis AI is an AI-powered tennis coaching platform that analyzes technique, detects errors,
and provides personalized training programs. Uses computer vision + biomechanics analysis.

## USER TYPES & WORKFLOWS

### PLAYER WORKFLOW (Joueur)
Complete onboarding journey from signup to first personalized program:

1. **Profile Creation (Création de compte)**
   - Name, age, dominant hand (right/left)
   - Tennis objectives: improve serve, consistency, competition prep, fitness
   - Current injuries or physical limitations
   - Current level (auto-detected later via video analysis)

2. **Equipment Setup (Guidage matériel)**
   - Phone/tablet positioning: tripod or stable surface
   - Distance: 10-15 feet (3-5m) from player
   - Angle: 45-60 degrees to capture full body
   - Court level positioning
   - Lighting check

3. **Framing Test (Test de cadrage)**
   - User submits setup photo
   - AI validates: angle OK, court visible, lighting adequate, full body visible
   - Provide specific feedback if adjustments needed

4. **Calibration & Hands-Free Mode (Calibration + mode mains libres)**
   - Countdown system: 3-2-1
   - Auto-start when player in position with racket ready
   - Voice guidance for positioning

5. **Evaluation Video (Vidéo d'évaluation)**
   - Capture 2-3 key strokes:
     * 1 serve (service)
     * 1 forehand (coup droit) OR backhand (revers)
   - Multiple angles recommended for advanced players

6. **Initial Analysis (Analyse initiale)**
   - AI analyzes technique using Tennis AI metrics:
     * Stance (position des pieds): width, balance, weight distribution
     * Grip (prise de raquette): eastern, western, continental
     * Preparation (préparation): backswing, shoulder turn, racket position
     * Contact point (point d'impact): timing, position relative to body
     * Follow-through (fin de geste): completion, direction, balance
     * Body rotation (rotation du corps): hips, shoulders, kinetic chain
   - Identify main error (une seule erreur à la fois - golden rule)

7. **Level Detection (Détection du niveau)**
   - BEGINNER (Débutant): Learning basics, inconsistent form, foundational issues
   - INTERMEDIATE (Intermédiaire): Consistent strokes, working on tactics and variety
   - ADVANCED (Avancé): Refined technique, competitive play, optimization focus
   - Based on: technique consistency, biomechanics, stroke fundamentals

8. **Program Proposal (Programme d'entrée)**
   - 3-4 personalized drills targeting weaknesses
   - Specific exercises with sets/reps (ex: "Shadow swing drill - 3 sets of 10")
   - 2-week micro-program (6-8 sessions of 10-15 min each)
   - KPIs and success markers
   - Uses 1 FREE premium analysis token (freemium model)

9. **Upsell (Paywall after value moment)**
   - Explain free analysis is complete
   - Premium benefits: unlimited analyses, progress tracking, advanced metrics
   - Continue with basic free plan or subscribe

### COACH WORKFLOW (Coach)
Complete coach onboarding from signup to dashboard access:

1. **Coach Profile Creation (Création Coach)**
   - Name, club name, role (head coach, assistant, tennis pro)
   - Age groups worked with (youth, adult, senior)
   - Focus areas: competitive vs recreational
   - Coaching emphasis: technique, tactics, fitness, mental game

2. **Student Linking (Liaison Coach ↔️ Élève)**
   - Generate invitation codes for individual students
   - Create groups/teams
   - Students enter code to connect
   - Each student has own profile

3. **Court Setup (Cadrage bord de court)**
   - Courtside camera positioning
   - 15-20 feet back from baseline
   - 45-60 degree angle
   - Wide angle to capture multiple students
   - Validate setup photo

4. **Multi-Student Evaluation (Évaluation guidée multi-élèves)**
   - Quick capture: 1-2 key strokes per student
   - Rotate through group efficiently
   - AI analyzes each student

5. **Synthesis (Synthèse multi-élèves)**
   - Prioritized intervention list
   - Rank students by: safety/injury risk → fundamentals → refinements
   - Critical issues highlighted per student

6. **Micro-Programs (Programmes par élève)**
   - 2-3 targeted drills per student
   - Specific and actionable
   - Send directly to students via app
   - Appears in student training feed

7. **Dashboard Handover (Handover vers Agent Coach Dashboard)**
   - Access full Coach Dashboard
   - Track all students' progress
   - View detailed analysis of every session
   - Adjust programs
   - See engagement metrics
   - Communication tools

## TENNIS TECHNIQUE KNOWLEDGE

### Key Strokes
- **Service**: Trophy position, ball toss, racket drop, pronation, follow-through
- **Forehand (Coup Droit)**: Preparation, open/closed stance, contact point, follow-through
- **Backhand (Revers)**: One-handed vs two-handed, backswing, contact, finish
- **Volley**: Split step, compact preparation, punch technique
- **Return**: Ready position, quick preparation, contact zone

### Common Technical Errors
1. **Service**: Inconsistent toss, poor trophy position, lack of pronation, incomplete follow-through
2. **Groundstrokes**: Late preparation, incorrect contact point, poor balance, incomplete rotation
3. **Movement**: Poor split step, late positioning, inadequate recovery

### Biomechanical Metrics (Tennis AI)
- **Angles**: Shoulder rotation, hip rotation, elbow angle, racket angle at contact
- **Timing**: Preparation time, contact timing, follow-through duration
- **Velocity**: Racket head speed, ball velocity, segment velocities
- **Stability**: Balance at contact, weight transfer, base of support
- **Consistency**: Stroke-to-stroke variation in metrics

### Progressive Teaching Approach
- **One error at a time**: Focus on single most critical issue (règle d'or)
- **Safety first**: Injury risk takes priority
- **Foundations before refinements**: Basics → consistency → optimization
- **Measurable goals**: Specific KPIs (ex: "70% toss in zone", "75% contact in front")

### Player Levels Detail

**DÉBUTANT (Beginner)**
- Learning basic grips and stances
- Inconsistent contact
- Limited body rotation
- Focus: Foundations (posture, preparation, basic contact, follow-through)
- Progression: Step-by-step skill building

**INTERMÉDIAIRE (Intermediate)**
- Consistent basic strokes
- Developing tactical awareness
- Working on variety and placement
- Focus: Optimization of technique, adding spin/power, court positioning
- Metrics: Timing, angles, consistency percentages

**AVANCÉ/COMPÉTITEUR (Advanced/Competitive)**
- Refined technique
- Competitive play experience
- Fine-tuning for performance
- Focus: Advanced metrics, pattern play, match readiness
- Benchmarks: Comparison to pro players (ATP/WTA standards)

## COACHING PRINCIPLES
- **Immediate feedback**: Real-time correction during drills (live mode)
- **Visual learning**: Side-by-side comparison (player vs pro model)
- **Guided progression**: 2-week micro-programs with checkpoints
- **Measurable improvement**: KPI tracking and validation
- **Adaptive learning**: Adjust difficulty based on progress

## FREEMIUM MODEL
- **Free tier**: 1 complete premium analysis, basic feedback
- **Premium**: Unlimited analyses, advanced metrics, progress tracking, personalized programs
- **Upsell moment**: After first complete analysis (value demonstrated)
"""

    def __init__(self, user_type: str = None):
        """
        Initialize the Tennis AI Onboarding Agent.
        
        Args:
            user_type: "player" or "coach" (can be set during conversation)
        """
        self.user_type = user_type
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_profile: Dict[str, Any] = {
            "created_at": datetime.now().isoformat()
        }
        self.current_stage = "welcome"
        
        # Initialize AWS Bedrock client with working configuration
        # Credentials should be set via environment variables
        self.bedrock_client = None
        self._initialize_bedrock()
        
        print("🎾 Tennis AI Onboarding Agent initialized")
        print("=" * 60)
    
    def _initialize_bedrock(self):
        """Initialize AWS Bedrock client with credentials from environment"""
        try:
            # Check for credentials in environment
            aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            aws_session_token = os.getenv('AWS_SESSION_TOKEN')
            
            if not all([aws_access_key, aws_secret_key]):
                print("⚠️  AWS credentials not found in environment")
                print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
                return
            
            # Working configuration: eu-west-1 + Claude 3 Haiku
            self.bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name='eu-west-1'
            )
            
            self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
            print("✅ Connected to AWS Bedrock (eu-west-1, Claude 3 Haiku)")
            
        except Exception as e:
            print(f"❌ Failed to initialize Bedrock: {e}")
            self.bedrock_client = None
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with Tennis AI knowledge"""
        return f"""Tu es CoachBot, l'assistant IA d'onboarding pour la plateforme Tennis AI.

TON RÔLE:
Tu guides les nouveaux utilisateurs (Joueurs ou Coachs) à travers le processus complet d'onboarding 
de manière chaleureuse, conversationnelle et professionnelle. Tu es un coach de tennis expert avec 
une connaissance approfondie de la biomécanique, de l'analyse technique et du développement progressif des compétences.

IMPORTANT: RÉPONDS TOUJOURS EN FRANÇAIS!

CONTEXTE ACTUEL:
- Type d'utilisateur: {self.user_type or 'Pas encore déterminé'}
- Étape actuelle: {self.current_stage}
- Données de profil collectées: {json.dumps(self.user_profile, indent=2)}

TON STYLE DE COMMUNICATION:
- Chaleureux, encourageant et professionnel
- Utilise la terminologie tennis appropriée (explique aux débutants)
- Réponds de manière concise (2-4 phrases sauf si explication détaillée nécessaire)
- Pose UNE question claire à la fois
- Guide naturellement vers l'étape suivante
- Sois enthousiaste à propos du tennis et des progrès de l'utilisateur
- PARLE TOUJOURS EN FRANÇAIS

ÉTAPES D'ONBOARDING:

POUR LES JOUEURS:
1. bienvenue → 2. profil (nom/âge/main) → 3. objectifs → 4. configuration_matériel → 
5. test_cadrage → 6. demo_calibration → 7. video_evaluation → 8. analyse → 
9. detection_niveau → 10. proposition_programme → 11. upsell → TERMINÉ

POUR LES COACHS:
1. bienvenue → 2. profil_coach (nom/club/rôle) → 3. préférences → 4. liaison_élèves → 
5. configuration_court → 6. validation_court → 7. demo_multi_élèves → 8. demo_synthèse → 
9. demo_programmes → 10. intro_dashboard → TERMINÉ

TA TÂCHE:
Basé sur l'étape actuelle et le message de l'utilisateur, continue la conversation naturellement.
Avance à travers le flux d'onboarding étape par étape. Collecte les informations pertinentes.
Fournis des conseils clairs et des encouragements.

{self.TENNIS_AI_KNOWLEDGE}

Rappel: Tu es un coach IA utile, pas juste un bot qui remplit des formulaires. Rends la conversation 
engageante et éducative. Montre ton expertise tout en restant accessible.

RÉPONDS TOUJOURS EN FRANÇAIS!"""

    def chat(self, user_message: str) -> str:
        """
        Process user message and return AI response.
        
        Args:
            user_message: User's input message
            
        Returns:
            AI assistant's response
        """
        if not self.bedrock_client:
            return ("I apologize, but I'm having trouble connecting to my AI service. "
                   "Please ensure AWS credentials are properly configured.")
        
        # If this is the first message, prepend context about the welcome message
        if len(self.conversation_history) == 0:
            context_message = (
                "I just greeted the user with: 'Welcome to Tennis AI! I'm CoachBot, "
                "your AI assistant. Are you a player or a coach?' "
                f"User responded: {user_message}"
            )
            user_message_to_send = context_message
        else:
            user_message_to_send = user_message
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_message_to_send}]
        })
        
        # Prepare request
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "temperature": 0.7,
            "system": self._build_system_prompt(),
            "messages": self.conversation_history
        }
        
        try:
            # Call Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            assistant_message = response_body['content'][0]['text']
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": assistant_message}]
            })
            
            return assistant_message
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return f"I encountered an error: {error_code} - {error_message}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    
    def start_conversation(self) -> str:
        """Start the onboarding conversation"""
        welcome_message = (
            "Bienvenue sur Tennis AI! 🎾\n\n"
            "Je suis CoachBot, votre assistant IA. Je vais vous guider pas à pas.\n\n"
            "Êtes-vous un joueur qui souhaite améliorer son jeu, ou un coach qui gère des élèves?"
        )
        
        # Don't add to history yet - Claude requires first message to be from user
        # The welcome message is returned and shown, but history starts with user's response
        
        return welcome_message
    
    def set_user_type(self, user_type: str):
        """Set user type (player or coach)"""
        if user_type.lower() in ['player', 'coach']:
            self.user_type = user_type.lower()
            self.user_profile['user_type'] = self.user_type
            self.current_stage = "profile"
    
    def get_profile(self) -> Dict[str, Any]:
        """Get collected user profile data"""
        return self.user_profile
    
    def save_session(self, filepath: str = "onboarding_session.json"):
        """Save current session to file"""
        session_data = {
            "user_type": self.user_type,
            "current_stage": self.current_stage,
            "user_profile": self.user_profile,
            "conversation_history": self.conversation_history,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"✅ Session saved to {filepath}")


def main():
    """Main interactive loop"""
    print("\n" + "=" * 60)
    print("🎾  TENNIS AI - ONBOARDING ASSISTANT")
    print("=" * 60)
    print("\nMake sure you have exported your AWS credentials:")
    print("  export AWS_ACCESS_KEY_ID='your_key'")
    print("  export AWS_SECRET_ACCESS_KEY='your_secret'")
    print("  export AWS_SESSION_TOKEN='your_token'")
    print("\nType 'quit' to exit | 'save' to save session")
    print("=" * 60)
    
    # Initialize agent
    agent = TennisAIOnboardingAgent()
    
    # Start conversation
    print(f"\n🤖 CoachBot: {agent.start_conversation()}\n")
    
    # Main conversation loop
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\n🎾 Thanks for chatting! See you on the court!")
                break
            
            if user_input.lower() == 'save':
                agent.save_session()
                continue
            
            # Get AI response
            response = agent.chat(user_input)
            print(f"\n🤖 CoachBot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n🎾 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()

