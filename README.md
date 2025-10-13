# 🎾 Tennis AI - Agent d'Onboarding

Application d'onboarding conversationnelle en français pour la plateforme Tennis AI, alimentée par AWS Bedrock (Claude 3 Haiku).

## 🚀 Démarrage Rapide avec Docker

### Prérequis
- Docker et Docker Compose installés
- Credentials AWS Bedrock

### Lancer l'application

```bash
# 1. Créer le fichier .env avec vos credentials AWS
cp .env.example .env
# Éditer .env avec vos credentials

# 2. Builder et lancer
docker-compose up --build

# 3. Accéder à l'application
# Ouvrir http://localhost:8501 dans votre navigateur
```

### Commandes Docker

```bash
# Lancer en arrière-plan
docker-compose up -d

# Voir les logs
docker logs tennis-ai-onboarding -f

# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Rebuild complet
docker-compose down
docker-compose up --build
```

## 📋 Fonctionnalités

### Workflows d'Onboarding

**Pour les Joueurs:**
1. Profil (nom, âge, main dominante)
2. Objectifs tennis et blessures
3. Configuration matériel (téléphone/trépied)
4. Test de cadrage
5. Mode calibration mains libres
6. Capture vidéo (service + coup droit/revers)
7. Analyse technique IA
8. Détection de niveau
9. Programme personnalisé
10. Présentation premium

**Pour les Coachs:**
1. Profil coach (club, rôle)
2. Préférences de coaching
3. Système de liaison élèves
4. Configuration bord de court
5. Validation angle caméra
6. Évaluation multi-élèves
7. Synthèse des priorités
8. Génération de micro-programmes
9. Accès au dashboard complet

### Caractéristiques Techniques

- **100% en français** - Conversations naturelles
- **AWS Bedrock** - Claude 3 Haiku (eu-west-1)
- **Streamlit** - Interface moderne en mode clair
- **Docker** - Déploiement simplifié
- **Mémoire contextuelle** - L'agent se souvient de toute la conversation

## 🧪 Tests

```bash
# Tests complets (hors Docker)
conda activate ai
python test_complete_workflows.py

# Test simple de connexion Bedrock
python test_bedrock_simple.py
```

## 📂 Structure du Projet

```
TENNIS AI/
├── docker-compose.yml          # Orchestration Docker
├── Dockerfile                  # Configuration Docker
├── .env                        # Credentials AWS (non committé)
├── requirements.txt            # Dépendances Python
├── DOCUMENTATION.md            # Documentation complète
│
├── onboarding_agent_v2.py     # Agent IA principal
├── streamlit_app.py           # Interface web Streamlit
│
├── test_bedrock_simple.py     # Test API Bedrock
└── test_complete_workflows.py # Tests complets
```

## ⚙️ Configuration

### Variables d'Environnement (.env)

```bash
AWS_ACCESS_KEY_ID=votre_clé
AWS_SECRET_ACCESS_KEY=votre_secret
AWS_SESSION_TOKEN=votre_token
```

### Configuration AWS Bedrock

- **Région:** eu-west-1
- **Modèle:** anthropic.claude-3-haiku-20240307-v1:0
- **Service:** bedrock-runtime

## 📖 Documentation

Voir [DOCUMENTATION.md](./DOCUMENTATION.md) pour:
- Architecture complète
- Workflows détaillés
- Configuration avancée
- Dépannage

## 🐛 Dépannage

### Container ne démarre pas
```bash
docker logs tennis-ai-onboarding
docker-compose down && docker-compose up --build
```

### Erreur AWS Credentials
```bash
# Vérifier le fichier .env
cat .env

# Vérifier dans le container
docker exec tennis-ai-onboarding env | grep AWS
```

### Port 8501 déjà utilisé
```bash
# Trouver le processus
lsof -i :8501

# Changer le port dans docker-compose.yml
ports:
  - "8502:8501"
```

## 📊 Monitoring

### Vérifier l'état
```bash
# Status du container
docker ps

# Health check
docker inspect tennis-ai-onboarding | grep -A5 Health

# Logs en temps réel
docker logs -f tennis-ai-onboarding
```

## 🔒 Sécurité

- ⚠️ Ne jamais committer le fichier `.env`
- ⚠️ Credentials AWS sensibles
- ✅ `.env` est dans `.gitignore`
- ✅ `.dockerignore` exclut les fichiers sensibles

## 🚀 Utilisation

1. Ouvrir http://localhost:8501
2. Choisir votre rôle (Joueur ou Coach)
3. Suivre la conversation guidée avec CoachBot
4. Obtenir votre programme personnalisé

## 📝 Notes

- L'agent répond toujours en français
- Mémoire conversationnelle complète
- Interface en mode clair permanent
- Health check automatique (30s)

## 📄 Licence

Tennis AI © 2025 - Tous droits réservés

---

**Support**: Voir DOCUMENTATION.md pour plus d'informations

