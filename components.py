"""
このファイルは、画面表示に特化した関数定義のファイルです。
多言語対応版
"""

############################################################
# ライブラリの読み込み
############################################################
import logging
import streamlit as st
import constants as ct
import utils

############################################################
# 関数定義
############################################################

def display_language_selector():
    """
    言語選択の表示
    """
    # 言語定数を取得
    lang_constants = ct.get_language_constants()
    
    st.markdown(lang_constants.LANGUAGE_SELECTION_HEADER)
    
    # 現在の言語を取得
    current_language = getattr(st.session_state, 'language', 'ja')
    
    # 言語選択
    selected_language = st.selectbox(
        lang_constants.LANGUAGE_SELECTION_TEXT,
        options=list(lang_constants.SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: lang_constants.SUPPORTED_LANGUAGES[x],
        index=list(lang_constants.SUPPORTED_LANGUAGES.keys()).index(current_language),
        key="language_selector"
    )
    
    # 言語が変更された場合
    if st.session_state.language != selected_language:
        st.session_state.language = selected_language
        # RAGチェーンを現在の言語で再構築
        utils.rebuild_rag_chain_for_current_language()
        st.rerun()  # ページを再読み込み

def display_theme_toggle():
    """
    ダークモード切り替えボタンの表示
    """
    st.markdown("## 🎨 テーマ切り替え")
    
    current_theme = "ダークモード" if st.session_state.get('dark_mode', False) else "ライトモード"
    
    # ボタンのテキストを現在のテーマに応じて変更
    button_text = "🌙 ダークモード" if not st.session_state.get('dark_mode', False) else "☀️ ライトモード"
    
    if st.button(button_text, key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.get('dark_mode', False)
        st.rerun()

def display_app_title():
    """
    タイトル表示
    """
    st.markdown(f"## {ct.get_text('APP_NAME')}")

def display_sidebar():
    """
    サイドバーの表示
    """
    with st.sidebar:
        # 言語選択を最初に表示
        display_language_selector()
        
        st.divider()
        
        # ダークモード切り替えボタン
        display_theme_toggle()
        
        st.divider()
        
        st.markdown(ct.get_text('CONTACT_MODE_HEADER'))
        
        col1, = st.columns([80])
        with col1:
            st.session_state["contact_mode"] = st.selectbox(
                label=ct.get_text('CONTACT_MODE_SELECTION_TEXT'),
                options=[ct.get_text('CONTACT_MODE_OFF'), ct.get_text('CONTACT_MODE_ON')],
                label_visibility="collapsed",
            )
        
        st.divider()

        st.markdown(ct.get_text('CONTACT_MODE_DESCRIPTION_TEXT'))
        st.code(ct.get_text('CONTACT_MODE_DESCRIPTION_DETAIL_TEXT'), wrap_lines=True)

def display_initial_ai_message():
    """
    AIメッセージの初期表示
    """
    with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
        st.success(ct.get_text('CONTACT_MODE_BOT_INTRODUCTION_TEXT'))
        st.warning(ct.get_text('CONTACT_MODE_BOT_SPECIFICITY_TEXT'), icon=ct.get_text('WARNING_ICON'))

def display_conversation_log(chat_message):
    """
    会話ログの一覧表示
    """
    # 会話ログの最後を表示する時のみ、フィードバック後のメッセージ表示するために「何番目のメッセージか」を取得
    for index, message in enumerate(st.session_state.messages):
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar=ct.AI_ICON_FILE_PATH):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar=ct.USER_ICON_FILE_PATH):
                st.markdown(message["content"])

