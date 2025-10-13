"""
Tennis AI - Application d'Onboarding
Interface web Streamlit en français pour l'onboarding des Joueurs et Coachs
"""

import streamlit as st
import os
from onboarding_agent_v2 import TennisAIOnboardingAgent

# Configuration de la page - MODE CLAIR TOUJOURS
st.set_page_config(
    page_title="Tennis AI - Onboarding",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Forcer le thème clair
st.markdown("""
<style>
    /* Force light mode */
    :root {
        --background-color: #ffffff;
        --text-color: #000000;
    }
    
    /* Hide dark mode toggle */
    button[kind="header"] {
        display: none;
    }
    
    /* Main styling */
    .main {
        background-color: #ffffff;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        color: #1e88e5;
        margin-bottom: 0.5rem;
        padding: 2rem 0;
    }
    
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
        border-left: 4px solid #1e88e5;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #1e88e5;
    }
    
    .assistant-message {
        background-color: #f1f8e9;
        border-left-color: #66bb6a;
    }
    
    .message-header {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1e88e5;
    }
    
    /* Welcome boxes */
    .welcome-box {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
    }
    
    .welcome-box h3 {
        color: #1e88e5;
        margin-bottom: 1rem;
    }
    
    .welcome-box ul {
        list-style: none;
        padding-left: 0;
    }
    
    .welcome-box li {
        padding: 0.5rem 0;
        color: #424242;
    }
    
    .welcome-box li:before {
        content: "✓ ";
        color: #66bb6a;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #1e88e5;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        background-color: #1565c0;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    /* Success/Error boxes */
    .success-box {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #66bb6a;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #ffebee;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #ef5350;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #1e88e5;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session():
    """Initialiser la session Streamlit"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.agent = None
        st.session_state.messages = []
        st.session_state.user_type = None


def render_chat_message(role: str, content: str):
    """Afficher un message du chat"""
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


def main():
    """Application principale"""
    initialize_session()
    
    # En-tête principal
    st.markdown('<div class="main-header">🎾 Tennis AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Votre coach IA personnel</div>', unsafe_allow_html=True)
    
    # Si pas encore initialisé, montrer l'écran de bienvenue
    if not st.session_state.initialized:
        st.markdown("---")
        
        # Choix du rôle
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('''
            <div class="welcome-box">
                <h3>🎾 Pour les Joueurs</h3>
                <ul>
                    <li>Créez votre profil tennis</li>
                    <li>Obtenez une analyse IA de votre technique</li>
                    <li>Recevez un programme personnalisé</li>
                    <li>Suivez vos progrès</li>
                    <li>Accédez à des conseils d'experts</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("🎾 Je suis un Joueur", key="player_btn"):
                st.session_state.user_type = "player"
                st.session_state.agent = TennisAIOnboardingAgent()
                st.session_state.agent.user_type = "player"
                welcome = st.session_state.agent.start_conversation()
                st.session_state.messages.append(("assistant", welcome))
                st.session_state.initialized = True
                st.rerun()
        
        with col2:
            st.markdown('''
            <div class="welcome-box">
                <h3>👨‍🏫 Pour les Coachs</h3>
                <ul>
                    <li>Configurez votre profil coach</li>
                    <li>Gérez plusieurs élèves/équipes</li>
                    <li>Évaluations rapides</li>
                    <li>Générez des programmes ciblés</li>
                    <li>Suivez les progrès de vos élèves</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("👨‍🏫 Je suis un Coach", key="coach_btn"):
                st.session_state.user_type = "coach"
                st.session_state.agent = TennisAIOnboardingAgent()
                st.session_state.agent.user_type = "coach"
                welcome = st.session_state.agent.start_conversation()
                st.session_state.messages.append(("assistant", welcome))
                st.session_state.initialized = True
                st.rerun()
        
        # Information sur les credentials
        st.markdown("---")
        st.markdown('''
        <div class="info-box">
            <strong>ℹ️ Note:</strong> Assurez-vous que les variables d'environnement AWS sont configurées avant de commencer.
        </div>
        ''', unsafe_allow_html=True)
    
    else:
        # Mode conversation
        st.markdown("---")
        
        # Bouton recommencer dans le coin
        col1, col2, col3 = st.columns([5, 1, 1])
        with col2:
            if st.button("🔄 Recommencer"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        with col3:
            if st.button("💾 Sauvegarder"):
                st.session_state.agent.save_session()
                st.success("Session sauvegardée!")
        
        st.markdown("---")
        
        # Afficher l'historique des messages
        for role, content in st.session_state.messages:
            render_chat_message(role, content)
        
        # Zone de saisie
        st.markdown("---")
        
        with st.form(key="message_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                user_input = st.text_input(
                    "Votre réponse:",
                    key="user_input",
                    placeholder="Tapez votre message ici..."
                )
            
            with col2:
                submit_button = st.form_submit_button("📨 Envoyer")
            
            if submit_button and user_input:
                # Ajouter le message utilisateur
                st.session_state.messages.append(("user", user_input))
                
                # Obtenir la réponse de l'IA
                try:
                    response = st.session_state.agent.chat(user_input)
                    st.session_state.messages.append(("assistant", response))
                except Exception as e:
                    error_msg = f"❌ Erreur: {str(e)}"
                    st.session_state.messages.append(("assistant", error_msg))
                
                st.rerun()


if __name__ == "__main__":
    # Vérifier les credentials AWS
    if not os.getenv('AWS_ACCESS_KEY_ID'):
        st.error("""
        ⚠️ Variables d'environnement AWS non configurées!
        
        Veuillez exécuter dans votre terminal:
        ```
        export AWS_ACCESS_KEY_ID="votre_clé"
        export AWS_SECRET_ACCESS_KEY="votre_secret"
        export AWS_SESSION_TOKEN="votre_token"
        ```
        """)
    else:
        main()
