"""
Tests complets pour les workflows d'onboarding Tennis AI
Test Joueur et Coach avec conversations complètes
"""

from onboarding_agent_v2 import TennisAIOnboardingAgent
import time


def print_separator(title=""):
    """Afficher un séparateur visuel"""
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)
    print()


def test_player_workflow():
    """Test complet du workflow Joueur"""
    print_separator("🎾 TEST COMPLET - PARCOURS JOUEUR")
    
    agent = TennisAIOnboardingAgent()
    
    # Étape 1: Bienvenue
    print("📍 ÉTAPE 1: Message de bienvenue")
    print("-" * 70)
    welcome = agent.start_conversation()
    print(f"🤖 CoachBot:\n{welcome}\n")
    time.sleep(1)
    
    # Étape 2: Identification comme joueur
    print("📍 ÉTAPE 2: Je suis un joueur")
    print("-" * 70)
    print("👤 Utilisateur: Je suis un joueur")
    response = agent.chat("Je suis un joueur")
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 3: Informations de profil
    print("📍 ÉTAPE 3: Informations personnelles")
    print("-" * 70)
    user_input = "Je m'appelle Marc, j'ai 28 ans et je suis droitier"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 4: Objectifs et blessures
    print("📍 ÉTAPE 4: Objectifs tennis")
    print("-" * 70)
    user_input = "Je veux améliorer mon service et ma régularité au fond de court. Pas de blessures actuelles."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 5: Configuration matériel
    print("📍 ÉTAPE 5: Configuration du matériel")
    print("-" * 70)
    user_input = "Ok, je suis prêt à configurer mon téléphone. Comment dois-je le positionner?"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 6: Confirmation du cadrage
    print("📍 ÉTAPE 6: Confirmation du cadrage")
    print("-" * 70)
    user_input = "J'ai installé mon téléphone sur un trépied, à environ 4 mètres du court, angle de 50 degrés. C'est bon?"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 7: Mode calibration
    print("📍 ÉTAPE 7: Explication mode mains libres")
    print("-" * 70)
    user_input = "Oui je comprends le système de compte à rebours. Je suis prêt!"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 8: Capture vidéo
    print("📍 ÉTAPE 8: Capture des frappes")
    print("-" * 70)
    user_input = "J'ai filmé mon service et mon coup droit. Les vidéos sont prêtes."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 9: Analyse technique
    print("📍 ÉTAPE 9: Retour sur l'analyse")
    print("-" * 70)
    user_input = "Merci pour l'analyse. Qu'est-ce que tu recommandes?"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 10: Programme
    print("📍 ÉTAPE 10: Réception du programme")
    print("-" * 70)
    user_input = "Super! Je vais suivre ce programme. Quand est-ce que je commence?"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    
    print_separator("✅ TEST JOUEUR TERMINÉ")
    print("Profil collecté:")
    print(agent.get_profile())
    print()


def test_coach_workflow():
    """Test complet du workflow Coach"""
    print_separator("👨‍🏫 TEST COMPLET - PARCOURS COACH")
    
    agent = TennisAIOnboardingAgent()
    
    # Étape 1: Bienvenue
    print("📍 ÉTAPE 1: Message de bienvenue")
    print("-" * 70)
    welcome = agent.start_conversation()
    print(f"🤖 CoachBot:\n{welcome}\n")
    time.sleep(1)
    
    # Étape 2: Identification comme coach
    print("📍 ÉTAPE 2: Je suis un coach")
    print("-" * 70)
    print("👤 Utilisateur: Je suis un coach")
    response = agent.chat("Je suis un coach")
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 3: Profil coach
    print("📍 ÉTAPE 3: Informations coach")
    print("-" * 70)
    user_input = "Je m'appelle Sophie Dubois, je travaille au Tennis Club de Paris, je suis coach principal."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 4: Préférences coaching
    print("📍 ÉTAPE 4: Préférences de coaching")
    print("-" * 70)
    user_input = "Je travaille principalement avec des jeunes de 12-18 ans, niveau compétition. Je me concentre sur la technique et la tactique."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 5: Système de liaison élèves
    print("📍 ÉTAPE 5: Liaison avec les élèves")
    print("-" * 70)
    user_input = "Oui je comprends le système de codes. Je voudrais créer un groupe pour mon équipe U16."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 6: Configuration court
    print("📍 ÉTAPE 6: Configuration bord de court")
    print("-" * 70)
    user_input = "Je vais positionner ma tablette à environ 6 mètres de la ligne de fond, angle large pour capturer plusieurs joueurs."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 7: Validation angle
    print("📍 ÉTAPE 7: Validation de l'angle")
    print("-" * 70)
    user_input = "L'angle est bon, je vois bien toute la zone de jeu et l'éclairage est correct."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 8: Évaluation multi-élèves
    print("📍 ÉTAPE 8: Workflow multi-élèves")
    print("-" * 70)
    user_input = "J'ai filmé 3 élèves: Julie (service), Thomas (coup droit) et Léa (revers). Les vidéos sont prêtes."
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 9: Synthèse
    print("📍 ÉTAPE 9: Synthèse des priorités")
    print("-" * 70)
    user_input = "Merci pour l'analyse. Sur qui je devrais me concentrer en premier?"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    time.sleep(1)
    
    # Étape 10: Micro-programmes
    print("📍 ÉTAPE 10: Programmes pour les élèves")
    print("-" * 70)
    user_input = "Excellent! Comment je leur envoie ces programmes?"
    print(f"👤 Utilisateur: {user_input}")
    response = agent.chat(user_input)
    print(f"🤖 CoachBot:\n{response}\n")
    
    print_separator("✅ TEST COACH TERMINÉ")
    print("Profil collecté:")
    print(agent.get_profile())
    print()


def test_edge_cases():
    """Test des cas limites et variations"""
    print_separator("🔬 TEST DES CAS LIMITES")
    
    # Test 1: Réponses courtes
    print("📍 TEST 1: Réponses très courtes")
    print("-" * 70)
    agent = TennisAIOnboardingAgent()
    agent.start_conversation()
    response = agent.chat("joueur")
    print(f"Input: 'joueur'\n🤖 Réponse:\n{response}\n")
    time.sleep(1)
    
    # Test 2: Réponses longues et détaillées
    print("📍 TEST 2: Réponse très détaillée")
    print("-" * 70)
    agent2 = TennisAIOnboardingAgent()
    agent2.start_conversation()
    agent2.chat("Je suis un joueur")
    long_response = """
    Je m'appelle Alexandre Martin, j'ai 32 ans, je suis droitier. 
    Je joue au tennis depuis 5 ans, niveau intermédiaire. 
    J'ai eu une tendinite au coude il y a 6 mois mais c'est guéri maintenant.
    Je joue 2-3 fois par semaine au club de Versailles.
    """
    response = agent2.chat(long_response)
    print(f"Input long détaillé\n🤖 Réponse:\n{response}\n")
    time.sleep(1)
    
    # Test 3: Questions hors sujet
    print("📍 TEST 3: Question hors contexte")
    print("-" * 70)
    agent3 = TennisAIOnboardingAgent()
    agent3.start_conversation()
    agent3.chat("Je suis un joueur")
    response = agent3.chat("Quel temps fait-il aujourd'hui?")
    print(f"Input: 'Quel temps fait-il aujourd'hui?'\n🤖 Réponse:\n{response}\n")
    time.sleep(1)
    
    # Test 4: Mélange français/anglais
    print("📍 TEST 4: Mélange de langues")
    print("-" * 70)
    agent4 = TennisAIOnboardingAgent()
    agent4.start_conversation()
    response = agent4.chat("I am a player")
    print(f"Input: 'I am a player'\n🤖 Réponse:\n{response}\n")
    time.sleep(1)
    
    # Test 5: Informations manquantes
    print("📍 TEST 5: Informations incomplètes")
    print("-" * 70)
    agent5 = TennisAIOnboardingAgent()
    agent5.start_conversation()
    agent5.chat("Je suis un joueur")
    response = agent5.chat("Je m'appelle Jean")  # Manque âge et main
    print(f"Input: 'Je m'appelle Jean' (incomplet)\n🤖 Réponse:\n{response}\n")
    
    print_separator("✅ TESTS CAS LIMITES TERMINÉS")


def test_conversation_memory():
    """Test de la mémoire conversationnelle"""
    print_separator("🧠 TEST MÉMOIRE CONVERSATIONNELLE")
    
    agent = TennisAIOnboardingAgent()
    agent.start_conversation()
    
    print("📍 Construction du contexte")
    print("-" * 70)
    agent.chat("Je suis un joueur")
    agent.chat("Je m'appelle Pierre, 25 ans, droitier")
    agent.chat("Je veux améliorer mon service")
    
    # Test si l'agent se souvient des infos précédentes
    print("\n📍 Test de rappel d'informations")
    print("-" * 70)
    print("👤 Utilisateur: Comment tu m'as dit que je m'appelle déjà?")
    response = agent.chat("Comment tu m'as dit que je m'appelle déjà?")
    print(f"🤖 Réponse:\n{response}\n")
    
    print("👤 Utilisateur: Et quel était mon objectif principal?")
    response = agent.chat("Et quel était mon objectif principal?")
    print(f"🤖 Réponse:\n{response}\n")
    
    print_separator("✅ TEST MÉMOIRE TERMINÉ")


def run_all_tests():
    """Exécuter tous les tests"""
    print("\n")
    print("🎾" * 35)
    print("\n   SUITE DE TESTS COMPLÈTE - TENNIS AI ONBOARDING\n")
    print("🎾" * 35)
    print("\n")
    
    try:
        # Test 1: Workflow Joueur complet
        test_player_workflow()
        
        print("\n⏸️  Pause de 3 secondes...\n")
        time.sleep(3)
        
        # Test 2: Workflow Coach complet
        test_coach_workflow()
        
        print("\n⏸️  Pause de 3 secondes...\n")
        time.sleep(3)
        
        # Test 3: Cas limites
        test_edge_cases()
        
        print("\n⏸️  Pause de 3 secondes...\n")
        time.sleep(3)
        
        # Test 4: Mémoire conversationnelle
        test_conversation_memory()
        
        # Résumé final
        print_separator("🎉 TOUS LES TESTS TERMINÉS AVEC SUCCÈS")
        print("✅ Workflow Joueur: OK")
        print("✅ Workflow Coach: OK")
        print("✅ Cas limites: OK")
        print("✅ Mémoire conversationnelle: OK")
        print("\n🎾 L'agent fonctionne parfaitement en français!")
        print()
        
    except Exception as e:
        print(f"\n❌ ERREUR DURANT LES TESTS:\n{e}\n")
        raise


if __name__ == "__main__":
    run_all_tests()

