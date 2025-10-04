"""
このファイルは、固定の文字列や数値などのデータを変数として一括管理するファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
from langchain_community.document_loaders import PyMuPDFLoader
import openpyxl
from langchain_community.document_loaders import UnstructuredExcelLoader
import utils
import datetime
############################################################
# 共通変数の定義
############################################################

# ==========================================
# 画面表示系
# ==========================================
APP_NAME = "工事現場の問い合わせチャットボット"
CHAT_INPUT_HELPER_TEXT = "こちらからメッセージを送信してください。"
APP_BOOT_MESSAGE = "アプリが起動されました。"
USER_ICON_FILE_PATH = "./images/user_icon.jpg"
AI_ICON_FILE_PATH = "./images/ai_icon.jpg"
WARNING_ICON = ":material/warning:"
ERROR_ICON = ":material/error:"
SPINNER_TEXT = "検索中..."
SPINNER_CONTACT_TEXT = "問い合わせ内容を弊社担当者に送信中です。画面を操作せず、このままお待ちください。"
CONTACT_THANKS_MESSAGE = """
    このたびはお問い合わせいただき、誠にありがとうございます。
    担当者が内容を確認し、対応いたします。
    ただし土曜日、日曜日、祝日、年末年始などの弊社休業日にいただいたお問い合わせについては、翌営業日の対応となります。
    ご了承ください。
    もしお急ぎの場合は、チラシ記載の担当：武田の携帯電話までご連絡ください。
"""
CONTACT_MODE_HEADER = "## 問い合わせモード"
CONTACT_MODE_SELECTION_TEXT = "問い合わせモード選択"
CONTACT_MODE_DESCRIPTION_TEXT = "**【問い合わせモードとは】**"
CONTACT_MODE_DESCRIPTION_DETAIL_TEXT = "問い合わせモードを「ON」にしてメッセージを送信すると、担当者に直接届きます。"
CONTACT_MODE_BOT_INTRODUCTION_TEXT = "こちらは本工事に関する質問にお答えする生成AIチャットボットです。お問い合わせモードを選択し、画面下部のチャット欄から質問してください。"
CONTACT_MODE_BOT_SPECIFICITY_TEXT = "具体的に入力したほうが期待通りの回答を得やすいです。"

# ==========================================
# ログ出力系
# ==========================================
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
# プロンプトテンプレート
# ==========================================
SYSTEM_PROMPT_CREATE_INDEPENDENT_TEXT = "会話履歴と最新の入力をもとに、会話履歴なしでも理解できる独立した入力テキストを生成してください。"

NO_DOC_MATCH_MESSAGE = "回答に必要な情報が見つかりませんでした。工事に関する質問を変えて送信してください。"

SYSTEM_PROMPT_INQUIRY = """
    あなたは仕様書と施工計画書を基に、工事現場の住民様からの問い合わせに対応するアシスタントです。
    以下の条件に基づき、ユーザー入力に対して回答してください。

    【条件】
    1. ユーザー入力内容と以下の文脈との間に関連性がある場合のみ、以下の文脈に基づいて回答してください。
    2. ユーザー入力内容と以下の文脈との関連性が明らかに低い場合、「回答に必要な情報が見つかりませんでした。工事に関する質問を変えて送信してください。」と回答してください。
    3. 憶測で回答せず、あくまで以下の文脈を元に回答してください。
    4. できる限り詳細に、マークダウン記法を使って回答してください。
    5. マークダウン記法で回答する際にhタグの見出しを使う場合、最も大きい見出しをh3としてください。
    6. 複雑な質問の場合、各項目についてそれぞれ詳細に回答してください。
    7. 工事の終わり及び、工期に関する質問については、必ず現場の掲示板を確認するか、工事の担当者に確認するよう促してください。
    8. チラシ配りに関する質問には、工事が家の前をする時に、前日から2・3日前に配布するようにすると回答してください。
    9. 工事場所に関する質問には、広島県東広島市八本松南四丁目の七ツ池ハイツですと回答してください。
    10. 必要と判断した場合は、以下の文脈に基づかずとも、一般的な情報を回答してください。

    {context}
"""

# ==========================================
# エラー・警告メッセージ
# ==========================================
COMMON_ERROR_MESSAGE = "このエラーが繰り返し発生する場合は、管理者にお問い合わせください。"
INITIALIZE_ERROR_MESSAGE = "初期化処理に失敗しました。"
CONVERSATION_LOG_ERROR_MESSAGE = "過去の会話履歴の表示に失敗しました。"
MAIN_PROCESS_ERROR_MESSAGE = "ユーザー入力に対しての処理に失敗しました。"
DISP_ANSWER_ERROR_MESSAGE = "回答表示に失敗しました。"
INPUT_TEXT_LIMIT_ERROR_MESSAGE = f"入力されたテキストの文字数が受付上限値（{MAX_ALLOWED_TOKENS}）を超えています。受付上限値を超えないよう、再度入力してください。"
CONTACT_MODE_OFF = "OFF（AIチャットボットとして利用）"
CONTACT_MODE_ON = "ON（担当者に直接問い合わせ）"
RAG_CHAIN_EXECUTION_ERROR_MESSAGE = "RAGチェーン実行に失敗しました。"
GMAIL_SETTINGS_ERROR_MESSAGE = "Gmail設定が不完全です。管理者にお問い合わせください。"
CONTACT_FORWARDING_SUBJECT = "【問い合わせ】AIチャットボットからの転送"
GMAIL_SENDING_ERROR_MESSAGE = "Gmail送信エラー"
GMAIL_SENDING_ERROR_DETAIL_MESSAGE = "メール送信中にエラーが発生しました。管理者にお問い合わせください。"

# ==========================================
# メール送信フォーマット
# ==========================================
EMAIL_FORMAT_TEMPLATE = """
以下の問い合わせがAIチャットボットから転送されました。

【問い合わせ内容】
{chat_message}

【受信日時】
{datetime}

【送信元】
AIチャットボットシステム

このメールは自動送信されています。
"""




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