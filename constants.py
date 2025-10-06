"""
このファイルは、固定の文字列や数値などのデータを変数として一括管理するファイルです。
多言語対応版
"""

############################################################
# ライブラリの読み込み
############################################################
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
import streamlit as st

############################################################
# 多言語対応の設定
############################################################

def get_language_constants():
    """
    選択された言語に応じた定数を取得
    """
    # セッション状態から言語を取得（デフォルトは日本語）
    lang = getattr(st.session_state, 'language', 'ja')
    
    if lang == 'en':
        import constants_en as lang_constants
    else:  # デフォルトは日本語
        import constants_ja as lang_constants
    
    return lang_constants

############################################################
# 言語に依存しない定数（システム設定等）
############################################################

# ==========================================
# ファイルパス系
# ==========================================
USER_ICON_FILE_PATH = "./images/user_icon.jpg"
AI_ICON_FILE_PATH = "./images/ai_icon.jpg"
LOG_DIR_PATH = "./logs"
LOGGER_NAME = "ApplicationLog"
LOG_FILE = "application.log"

# ==========================================
# LLM設定系
# ==========================================
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.5
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
TOP_K = 8
RETRIEVER_WEIGHTS = [0.5, 0.5]

# ==========================================
# トークン関連
# ==========================================
MAX_ALLOWED_TOKENS = 1000
ENCODING_KIND = "cl100k_base"

# ==========================================
# RAG参照用のデータソース系
# ==========================================
RAG_TOP_FOLDER_PATH = "./data/rag"

SUPPORTED_EXTENSIONS = {
    ".pdf": PyMuPDFLoader,
    ".xlsx": lambda path: UnstructuredExcelLoader(path, mode="elements"),
    ".xls":  lambda path: UnstructuredExcelLoader(path, mode="elements"),
}

DB_ALL_PATH = "./.db_all"
DB_COMPANY_PATH = "./.db_company"

# ==========================================
# スタイリング
# ==========================================
STYLE = """
<style>
    .stHorizontalBlock {
        margin-top: -14px;
    }
    .stChatMessage + .stHorizontalBlock {
        margin-left: 56px;
    }
    .stChatMessage + .stHorizontalBlock .stColumn:nth-of-type(2) {
        margin-left: -24px;
    }
    @media screen and (max-width: 480px) {
        .stChatMessage + .stHorizontalBlock {
            flex-wrap: nowrap;
            margin-left: 56px;
        }
        .stChatMessage + .stHorizontalBlock .stColumn:nth-of-type(2) {
            margin-left: -206px;
        }
    }
</style>
"""

############################################################
# 動的に言語定数を取得する関数
############################################################

def get_text(key):
    """
    指定されたキーの多言語テキストを取得
    """
    lang_constants = get_language_constants()
    return getattr(lang_constants, key, f"[Missing: {key}]")

def get_formatted_text(key, **kwargs):
    """
    フォーマット付きテキストを取得
    """
    text = get_text(key)
    if kwargs:
        if 'max_tokens' in text:
            kwargs['max_tokens'] = MAX_ALLOWED_TOKENS
        return text.format(**kwargs)
    return text