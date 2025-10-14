"""
Tennis AI - Onboarding Application
Interface Streamlit moderne et propre
"""

import streamlit as st
import sys
import os
from typing import Optional

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.onboarding_agent import OnboardingAgent
from api.polly_client import PollyClient
from utils import get_aws_credentials


# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="Tennis AI - Onboarding",
    page_icon="🎾",
    layout="centered",
    initial_sidebar_state="expanded"  # Sidebar ouverte par défaut pour montrer les options
)


# ==================== STYLES ====================

def load_custom_css():
    """Charger le CSS personnalisé (light mode)"""
    st.markdown("""
    <style>
    /* Mode light forcé */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    
    /* Messages */
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: fadeIn 0.3s;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #667eea;
    }
    
    .message-header {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #333;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Boutons */
    .stButton > button {
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Cards de sélection */
    .role-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        margin: 1rem 0;
    }
    
    .role-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
    }
    
    .role-card-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .role-card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .role-card-desc {
        color: #666;
        font-size: 0.95rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== SESSION STATE ====================

def initialize_session():
    """Initialiser l'état de session Streamlit"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.user_type = None
        st.session_state.agent = None
        st.session_state.messages = []
        st.session_state.tts_enabled = False
        st.session_state.polly_client = None
        st.session_state.audio_cache = {}  # Cache pour TTS lazy


# ==================== TTS (LAZY LOADING) ====================

def get_tts_audio(text: str, message_id: str) -> Optional[bytes]:
    """
    Obtenir l'audio TTS (généré UNIQUEMENT au clic via cache)
    
    Args:
        text: Texte à synthétiser
        message_id: ID unique du message
        
    Returns:
        bytes: Audio MP3 ou None
    """
    # Vérifier le cache
    if message_id in st.session_state.audio_cache:
        return st.session_state.audio_cache[message_id]
    
    # Générer l'audio (LAZY - seulement si pas en cache)
    try:
        if st.session_state.polly_client is None:
            st.session_state.polly_client = PollyClient(region='eu-west-1')
        
        audio_bytes = st.session_state.polly_client.synthesize(text)
        
        # Mettre en cache
        st.session_state.audio_cache[message_id] = audio_bytes
        
        return audio_bytes
        
    except Exception as e:
        st.error(f"Erreur TTS: {str(e)}")
        return None


# ==================== UI COMPONENTS ====================

def render_header():
    """Afficher le header de l'application"""
    st.markdown("""
    <div class="main-header">
        <h1>🎾 Tennis AI</h1>
        <p>Votre coach IA personnel</p>
    </div>
    """, unsafe_allow_html=True)


def render_role_selection():
    """Afficher l'écran de sélection de rôle"""
    st.markdown("## Bienvenue sur Tennis AI! 👋")
    st.markdown("Pour commencer, sélectionne ton rôle:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎾 Joueur", key="btn_player", use_container_width=True):
            start_onboarding("player")
    
    with col2:
        if st.button("🏆 Coach", key="btn_coach", use_container_width=True):
            start_onboarding("coach")
    
    # Descriptions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="role-card">
            <div class="role-card-icon">👤</div>
            <div class="role-card-title">Joueur</div>
            <div class="role-card-desc">
                Améliore ta technique avec des analyses vidéo et des programmes personnalisés
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="role-card">
            <div class="role-card-icon">👨‍🏫</div>
            <div class="role-card-title">Coach</div>
            <div class="role-card-desc">
                Gère tes élèves, analyse leurs performances et crée des programmes d'entraînement
            </div>
        </div>
        """, unsafe_allow_html=True)


def start_onboarding(user_type: str):
    """
    Démarrer l'onboarding pour un type d'utilisateur
    
    Args:
        user_type: 'player' ou 'coach'
    """
    st.session_state.user_type = user_type
    
    # Créer l'agent avec le type d'utilisateur
    st.session_state.agent = OnboardingAgent(user_type=user_type)
    
    # Obtenir le message de bienvenue
    welcome_message = st.session_state.agent.start_conversation()
    
    # Ajouter à l'historique
    st.session_state.messages = [("assistant", welcome_message)]
    
    # Rafraîchir pour afficher le chat
    st.rerun()


def render_chat_message(role: str, content: str, message_id: str):
    """
    Afficher un message de chat avec option TTS lazy
    
    Args:
        role: 'user' ou 'assistant'
        content: Contenu du message
        message_id: ID unique pour le cache TTS
    """
    if role == "user":
        st.markdown(f'''
        <div class="chat-message user-message">
            <div class="message-header">👤 Vous</div>
            <div>{content}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="chat-message assistant-message">
            <div class="message-header">🤖 CoachBot</div>
            <div>{content}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # TTS LAZY LOADING: Audio généré UNIQUEMENT au clic
        if st.session_state.tts_enabled:
            # Vérifier si l'audio est déjà en cache
            audio_cached = message_id in st.session_state.audio_cache
            
            # Bouton ou lecteur selon l'état
            if not audio_cached:
                # Bouton pour générer l'audio (LAZY)
                if st.button(f"🔊 Écouter", key=f"tts_btn_{message_id}"):
                    with st.spinner("Génération audio..."):
                        audio_bytes = get_tts_audio(content, message_id)
                        if audio_bytes:
                            st.rerun()
            else:
                # Afficher le lecteur audio (déjà généré)
                audio_bytes = st.session_state.audio_cache[message_id]
                st.audio(audio_bytes, format='audio/mp3')


def render_chat_interface():
    """Afficher l'interface de chat"""
    # Sidebar avec options
    with st.sidebar:
        st.markdown("### ⚙️ Options")
        
        # Toggle TTS avec feedback visuel
        tts_before = st.session_state.tts_enabled
        st.session_state.tts_enabled = st.checkbox(
            "🔊 Activer l'audio",
            value=st.session_state.tts_enabled,
            help="Affiche un bouton 🔊 Écouter sous chaque message de CoachBot"
        )
        
        # Afficher le statut
        if st.session_state.tts_enabled:
            st.success("✅ Audio activé - Bouton 🔊 visible!")
        else:
            st.info("ℹ️ Audio désactivé")
        
        st.markdown("---")
        
        # Info utilisateur
        user_type_display = "Joueur 🎾" if st.session_state.user_type == "player" else "Coach 🏆"
        st.markdown(f"**Rôle:** {user_type_display}")
        st.markdown(f"**Étape:** {st.session_state.agent.get_current_stage()}")
        
        st.markdown("---")
        
        if st.button("🔄 Nouvelle session"):
            # Reset
            st.session_state.user_type = None
            st.session_state.agent = None
            st.session_state.messages = []
            st.session_state.audio_cache = {}
            st.rerun()
    
    # Historique des messages
    for idx, (role, content) in enumerate(st.session_state.messages):
        message_id = f"msg_{idx}"
        render_chat_message(role, content, message_id)
    
    # Zone de saisie
    st.markdown("---")
    
    with st.form(key="message_form", clear_on_submit=True):
        user_input = st.text_input(
            "Votre message:",
            placeholder="Tapez votre réponse ici...",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            submit = st.form_submit_button("📤 Envoyer", use_container_width=True)
        
        with col2:
            if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                st.session_state.agent.save_session()
                st.success("Session sauvegardée!")
    
    # Traiter le message
    if submit and user_input:
        # Ajouter le message utilisateur
        st.session_state.messages.append(("user", user_input))
        
        # Obtenir la réponse de l'agent
        with st.spinner("CoachBot réfléchit..."):
            response = st.session_state.agent.chat(user_input)
        
        # Ajouter la réponse
        st.session_state.messages.append(("assistant", response))
        
        # Rafraîchir
        st.rerun()


# ==================== MAIN ====================

def main():
    """Application principale"""
    initialize_session()
    load_custom_css()
    render_header()
    
    # Vérifier les credentials AWS
    credentials = get_aws_credentials()
    if not credentials:
        st.error("⚠️ Credentials AWS non configurées!")
        st.info("Configure les variables d'environnement: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN")
        st.stop()
    
    # Afficher l'interface appropriée
    if st.session_state.user_type is None:
        render_role_selection()
    else:
        render_chat_interface()


if __name__ == "__main__":
    main()

