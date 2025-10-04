"""
このファイルは、画面表示に特化した関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import logging
import streamlit as st
import constants as ct


############################################################
# 関数定義
############################################################

def display_app_title():
    """
    タイトル表示
    """
    st.markdown(f"## {ct.APP_NAME}")


def display_sidebar():
    """
    サイドバーの表示
    """
    with st.sidebar:
        st.markdown(ct.CONTACT_MODE_HEADER)

        col1, = st.columns([80])
        with col1:
            st.session_state["contact_mode"] = st.selectbox(
                label=ct.CONTACT_MODE_SELECTION_TEXT,
                options=[ct.CONTACT_MODE_OFF, ct.CONTACT_MODE_ON],
                label_visibility="collapsed",
            )
        
        st.divider()

        st.markdown(ct.CONTACT_MODE_DESCRIPTION_TEXT)
        st.code(ct.CONTACT_MODE_DESCRIPTION_DETAIL_TEXT, wrap_lines=True)


def display_initial_ai_message():
    """
    AIメッセージの初期表示
    """
    with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
        st.success(ct.CONTACT_MODE_BOT_INTRODUCTION_TEXT)
        st.warning(ct.CONTACT_MODE_BOT_SPECIFICITY_TEXT, icon=ct.WARNING_ICON)


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