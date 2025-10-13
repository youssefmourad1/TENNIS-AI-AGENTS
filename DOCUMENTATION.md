# 🎾 Tennis AI - Agent d'Onboarding

## 📋 Vue d'ensemble

Tennis AI est une plateforme d'analyse technique alimentée par l'IA pour les joueurs et coachs de tennis. L'agent d'onboarding guide les nouveaux utilisateurs à travers un processus conversationnel complet en français.

## 🏗️ Architecture

### Composants Principaux

#### 1. **onboarding_agent_v2.py**
Agent conversationnel principal utilisant AWS Bedrock (Claude 3 Haiku).

**Caractéristiques:**
- Conversations 100% en français
- Workflows complets pour Joueurs et Coachs
- Mémoire contextuelle de la conversation
- Intégration complète de la connaissance Tennis AI
- Région AWS: `eu-west-1`
- Modèle: `anthropic.claude-3-haiku-20240307-v1:0`

**Classes:**
```python
class TennisAIOnboardingAgent:
    - __init__(user_type: str = None)
    - start_conversation() -> str
    - chat(user_message: str) -> str
    - get_profile() -> Dict[str, Any]
    - save_session(filepath: str)
```

#### 2. **streamlit_app.py**
Interface web moderne en Streamlit, mode clair permanent.

**Fonctionnalités:**
- Interface bilingue (français)
- Design responsive et épuré
- Chat conversationnel en temps réel
- Mode clair forcé (pas de dark mode)
- Gestion d'état avec session Streamlit

### Base de Connaissances

L'agent intègre une connaissance complète de:
- Workflows d'onboarding (Joueur et Coach)
- Terminologie tennis (technique, biomécanique)
- Niveaux de jeu (Débutant, Intermédiaire, Avancé)
- Métriques d'analyse (angles, timing, vitesse, stabilité)
- Programmes d'entraînement personnalisés
- Modèle freemium (1 analyse gratuite)

## 📊 Workflows d'Onboarding

### Workflow Joueur (10 étapes)

1. **Bienvenue** - Introduction et choix du rôle
2. **Profil** - Nom, âge, main dominante
3. **Objectifs** - Objectifs tennis et blessures
4. **Configuration Matériel** - Position téléphone/trépied
5. **Test Cadrage** - Validation du cadrage avec photo
6. **Calibration** - Explication mode mains libres
7. **Vidéo Évaluation** - Capture service + coup droit/revers
8. **Analyse** - Analyse technique IA
9. **Détection Niveau** - Débutant/Intermédiaire/Avancé
10. **Programme** - Programme personnalisé 2 semaines
11. **Upsell** - Présentation offre premium

### Workflow Coach (9 étapes)

1. **Bienvenue** - Introduction et choix du rôle
2. **Profil Coach** - Nom, club, rôle (coach principal, assistant)
3. **Préférences** - Groupes d'âge, focus (technique/tactique/fitness)
4. **Liaison Élèves** - Système de codes d'invitation
5. **Configuration Court** - Position caméra bord de court
6. **Validation Angle** - Vérification cadrage multi-élèves
7. **Évaluation Multi-Élèves** - Capture 1-2 coups par élève
8. **Synthèse** - Priorisation des interventions
9. **Micro-Programmes** - Programmes ciblés par élève
10. **Dashboard** - Accès au tableau de bord complet

## 🔧 Configuration

### Variables d'Environnement Requises

```bash
AWS_ACCESS_KEY_ID=votre_clé_aws
AWS_SECRET_ACCESS_KEY=votre_secret_aws
AWS_SESSION_TOKEN=votre_token_aws
```

### Configuration AWS Bedrock

- **Région:** eu-west-1 (Europe - Irlande)
- **Service:** bedrock-runtime
- **Modèle:** Claude 3 Haiku (`anthropic.claude-3-haiku-20240307-v1:0`)
- **Paramètres:**
  - `max_tokens`: 1024
  - `temperature`: 0.7
  - `anthropic_version`: "bedrock-2023-05-31"

## 🚀 Déploiement

### Option 1: Local avec Conda

```bash
# Activer l'environnement
conda activate ai

# Exporter les credentials
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."

# Lancer Streamlit
streamlit run streamlit_app.py
```

### Option 2: Docker

```bash
# Créer le fichier .env avec vos credentials
cp .env.example .env
# Éditer .env avec vos credentials

# Build et run
docker-compose up --build

# Ou avec Docker directement
docker build -t tennis-ai .
docker run -p 8501:8501 --env-file .env tennis-ai
```

L'application sera accessible sur: **http://localhost:8501**

## 🧪 Tests

### Tests Automatisés

```bash
# Tests complets (Joueur + Coach + Cas limites)
conda run -n ai python test_complete_workflows.py

# Test simple de connexion Bedrock
conda run -n ai python test_bedrock_simple.py
```

### Tests Manuels

1. Ouvrir l'interface web
2. Choisir un rôle (Joueur ou Coach)
3. Suivre la conversation guidée
4. Tester différents scénarios:
   - Réponses courtes vs détaillées
   - Informations complètes vs incomplètes
   - Questions hors contexte
   - Mélange français/anglais

## 📁 Structure du Projet

```
TENNIS AI/
├── Dockerfile                      # Configuration Docker
├── docker-compose.yml              # Orchestration Docker
├── .dockerignore                   # Exclusions Docker
├── .env.example                    # Template credentials
├── requirements.txt                # Dépendances Python
├── DOCUMENTATION.md                # Ce fichier
│
├── onboarding_agent_v2.py         # Agent IA principal
├── streamlit_app.py               # Interface web
│
├── test_bedrock_simple.py         # Test connexion AWS
├── test_complete_workflows.py     # Tests complets
│
└── docs txt/                      # Documentation source
    ├── Parcours Coach.txt
    ├── TennisAI_Parcours_*.txt
    └── ...
```

## 🎯 Fonctionnalités Clés

### 1. Conversation Naturelle
- Agent conversationnel intelligent
- Réponses contextuelles
- Mémoire de conversation complète
- Ton professionnel et chaleureux

### 2. Multilingue Intelligent
- Répond toujours en français
- Comprend l'anglais et le français
- Gère les inputs mixtes

### 3. Guidage Progressif
- Étapes claires et structurées
- Une question à la fois
- Validation des informations
- Feedback constructif

### 4. Analyse Technique
- Détection du niveau (Débutant/Intermédiaire/Avancé)
- Analyse biomécanique
- Identification des erreurs principales
- Recommandations personnalisées

### 5. Programmes Personnalisés
- Drills ciblés sur les faiblesses
- Plans 2 semaines (6-8 sessions)
- KPIs mesurables
- Progression suivie

## 🔐 Sécurité

### Bonnes Pratiques

1. **Credentials:**
   - Jamais dans le code source
   - Toujours via variables d'environnement
   - Utiliser `.env` pour Docker
   - Ne pas committer `.env`

2. **Données Utilisateur:**
   - Sessions sauvegardées localement
   - Pas de stockage cloud par défaut
   - Profils anonymisés pour analyse

3. **API:**
   - Rate limiting AWS Bedrock
   - Gestion des throttling exceptions
   - Retry logic avec backoff

## 📊 Monitoring

### Logs

L'application génère des logs pour:
- Initialisation Bedrock
- Appels API (succès/échec)
- Erreurs et exceptions
- État de session

### Métriques à Surveiller

- Temps de réponse API
- Taux d'erreur
- Complétude des onboardings
- Étapes d'abandon

## 🐛 Dépannage

### Problème: "AWS credentials not found"
**Solution:** Vérifier que les variables d'environnement sont bien exportées

### Problème: "ThrottlingException"
**Solution:** Trop de requêtes rapides. Attendre quelques secondes entre les tests.

### Problème: "ValidationException - Model not found"
**Solution:** Vérifier la région (doit être eu-west-1) et le model ID

### Problème: Interface Streamlit ne charge pas
**Solution:** 
```bash
# Vérifier le port
lsof -i :8501
# Tuer le processus si nécessaire
pkill -f streamlit
# Relancer
streamlit run streamlit_app.py
```

## 🚀 Évolutions Futures

### Phase 1 (Court terme)
- [ ] Upload d'images pour validation cadrage
- [ ] Analyse vidéo réelle (intégration avec backend)
- [ ] Sauvegarde sessions en base de données
- [ ] Authentification utilisateurs

### Phase 2 (Moyen terme)
- [ ] Dashboard coach complet
- [ ] Suivi progression joueurs
- [ ] Notifications et rappels
- [ ] Partage de programmes

### Phase 3 (Long terme)
- [ ] Analyse temps réel pendant jeu
- [ ] Comparaisons vs joueurs pro
- [ ] Recommandations tactiques
- [ ] Intégration wearables

## 📞 Support

Pour toute question ou problème:
1. Vérifier cette documentation
2. Consulter les logs d'erreur
3. Exécuter les tests de diagnostic
4. Vérifier la configuration AWS

## 📄 Licence

Tennis AI - Tous droits réservés © 2025

