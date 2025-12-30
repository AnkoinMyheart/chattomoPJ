from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import csv

app = FastAPI(title="Chattomo Mini API", version="0.2")

class MoodEnum(str, Enum):
    very_good = "very_good"
    good = "good"
    ok = "ok"
    tired = "tired"
    bad = "bad"

# ログを保存するCSVファイルのパス
LOG_PATH = Path("chattomo_logs.csv")

class MoodRequest(BaseModel):
    """
    クライアント（Power Apps / Swagger など）から受け取る入力の型。
    language:
      - "ja" 日本語モード
      - "en" 英語モード
      - それ以外 or 未指定 の場合は "en" として扱う
    """
    mood_text: MoodEnum | None = None
    comment: str | None = ""
    user_id: str | None = "honoka"
    language: str | None = None




# ---------- 感情判定ロジック ----------


def detect_mood(text: str, language: str) -> str:
    """
    テキストと言語から、ざっくり気分ラベルを返す。
    戻り値: "tired" / "anxious" / "happy" / "neutral"
    """
    t = (text or "").lower()
    lang = language.lower() if language else "en"


    if lang == "ja":
        tired_words = ["しんど", "疲れ", "つかれ", "だる", "もう無理", "燃え尽き"]
        anxious_words = ["不安", "怖い", "こわい", "心配", "やば", "どうしよう"]
        happy_words = ["嬉し", "うれし", "楽しい", "たのし", "最高", "幸せ", "やった"]
    else:  # English
        tired_words = ["tired", "exhausted", "drained", "burned out", "burnt out", "no energy"]
        anxious_words = ["anxious", "anxiety", "worried", "scared", "afraid", "nervous", "panic"]
        happy_words = ["happy", "excited", "great", "awesome", "fun", "fantastic", "amazing"]


    if any(w in t for w in tired_words):
        return "tired"
    if any(w in t for w in anxious_words):
        return "anxious"
    if any(w in t for w in happy_words):
        return "happy"
    return "neutral"




def mood_score(label: str, text: str) -> int:
    """
    ラベル＋強めのワードから気分スコアを -3〜+3 で算出。
    Power BI 用に数値化しておく。
    """
    base = {"tired": -2, "anxious": -1, "neutral": 0, "happy": 2}.get(label, 0)


    strong_down = [
        "ほんまに無理", "限界", "最悪", "死ぬほど",  # 日本語
        "terrible", "awful", "really bad", "hate this", "breaking down"  # 英語
    ]
    strong_up = [
        "神", "優勝", "最高すぎ", "幸せすぎ",  # 日本語
        "amazing", "awesome", "so happy", "super excited", "best day"  # 英語
    ]


    t = (text or "").lower()
    if any(w in t for w in strong_down):
        base -= 1
    if any(w in t for w in strong_up):
        base += 1


    # -3〜+3 にクリップ
    return max(-3, min(3, base))



# ---------- タグ抽出ロジック ----------


def extract_tags(text: str, language: str) -> list[str]:
    """
    テキストと言語から、ざっくりテーマタグを抽出。
    例: ["work", "people", "sleep", ...]
    """
    t = (text or "").lower()
    lang = language.lower() if language else "en"
    tags: list[str] = []


    if lang == "ja":
        if any(w in t for w in ["仕事", "残業", "案件", "客", "プロジェクト"]):
            tags.append("work")
        if any(w in t for w in ["上司", "先輩", "同僚", "人間関係"]):
            tags.append("people")
        if any(w in t for w in ["眠", "寝", "不眠", "睡眠"]):
            tags.append("sleep")
        if any(w in t for w in ["体調", "腹", "胃", "頭痛", "腰", "痛い"]):
            tags.append("health")
        if any(w in t for w in ["お金", "給料", "収入", "貯金", "生活費"]):
            tags.append("money")
        if any(w in t for w in ["将来", "ワーホリ", "海外", "キャリア", "不安"]):
            tags.append("future")
        if any(w in t for w in ["自信ない", "自己嫌悪", "自分なんて"]):
            tags.append("self-esteem")
        if any(w in t for w in ["恋", "恋愛", "彼氏", "彼女", "デート", "好き"]):
            tags.append("love")
    else:
        if any(w in t for w in ["work", "job", "project", "client", "deadline"]):
            tags.append("work")
        if any(w in t for w in ["boss", "manager", "coworker", "colleague", "people"]):
            tags.append("people")
        if any(w in t for w in ["sleep", "tired", "insomnia", "can't sleep", "fell asleep"]):
            tags.append("sleep")
        if any(w in t for w in ["health", "headache", "stomach", "back pain", "sick", "ill"]):
            tags.append("health")
        if any(w in t for w in ["money", "salary", "income", "bills", "rent"]):
            tags.append("money")
        if any(w in t for w in ["future", "career", "abroad", "visa", "move overseas", "plan"]):
            tags.append("future")
        if any(w in t for w in ["hate myself", "no confidence", "worthless", "not good enough"]):
            tags.append("self-esteem")
        if any(w in t for w in ["love", "crush", "boyfriend", "girlfriend", "date", "romantic"]):
            tags.append("love")


    return tags or ["general"]




# ---------- コメント生成（Chattomoの“声”） ----------


def build_comment(label: str, score: int, tags: list[str], language: str) -> str:
    """
    気分ラベル・スコア・タグ・言語から、
    Chattomo Mini が返すメッセージを作る。
    """
    lang = language.lower() if language else "en"


    if lang == "ja":
        # 日本語モード（自分用・開発用）
        if label == "tired":
            if "work" in tags:
                return "今日も仕事おつかれさま。かなり頑張りすぎてそうやから、今日は“回復デー”って決めてもいいレベルやで。"
            return "だいぶ疲れてそうやね…。まずは自分を責めずに、休む時間をちゃんと確保しよ。"
        if label == "anxious":
            if "future" in tags:
                return "将来のこと、不安になるのめっちゃ分かる。でも全部を一気に解こうとせずに、今できる一歩だけ一緒に決めよ。"
            return "不安が大きそうやね…。今すぐコントロールできることと、いったん手放していいことを分けてみよっか。"
        if label == "happy":
            if "love" in tags:
                return "なんか恋バナの匂いがするぞ…？その嬉しい気持ち、ちゃんと覚えとこ。あとで振り返ったときのエネルギーになるからね。"
            return "いい感じやん！何が良かったのか一言メモしておくと、あとで“再現レシピ”として使えるで。"
        # neutral
        return "了解。今の状態をちゃんとことばにできてるのがすでに強みやで。もう少しだけ状況教えてくれる？"


    # ここから英語モード（ポートフォリオ / デモ用）
    if label == "tired":
        if "work" in tags:
            return (
                "You sound really drained from work today. "
                "It's totally okay to treat today as a recovery day instead of pushing yourself harder."
            )
        return (
            "You seem pretty exhausted. Don't blame yourself for feeling this way. "
            "Let’s make rest your first priority today."
        )


    if label == "anxious":
        if "future" in tags:
            return (
                "It's completely natural to feel anxious about the future. "
                "Instead of solving everything at once, let's pick just one small step you can take now."
            )
        return (
            "I can feel your anxiety. Let's separate what you can control right now "
            "from what you can safely put aside for later."
        )


    if label == "happy":
        if "love" in tags:
            return (
                "Ooh, this sounds like romance energy. 😏 "
                "Try to capture what made you feel this happy—it's a great memory to come back to later."
            )
        return (
            "Love this mood! If you note down what went well today, "
            "it becomes a recipe you can reuse on tough days."
        )


    # neutral
    return (
        "Got it. The fact that you can put your current state into words is already a strength. "
        "If you’re okay with it, tell me a bit more so I can understand you better."
    )

def detect_language_from_text(text: str) -> str:
    """
    入力テキストから超ざっくり言語判定。
    日本語の文字（ひらがな／カタカナ／漢字）が1つでもあれば "ja"、
    それ以外は "en" とみなす。
    """
    if not text:
        return "en"


    for ch in text:
        # ひらがな
        if "\u3040" <= ch <= "\u309F":
            return "ja"
        # カタカナ
        if "\u30A0" <= ch <= "\u30FF":
            return "ja"
        # CJK統合漢字
        if "\u4E00" <= ch <= "\u9FFF":
            return "ja"


    return "en"



# ---------- CSV ログ保存 ----------


def append_log(row: dict) -> None:
    """
    ログを chattomo_logs.csv に追記保存。
    ファイルがなければヘッダー付きで新規作成。
    """
    is_new = not LOG_PATH.exists()
    with LOG_PATH.open("a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "user_id",
                "mood_text",
                "comment",
                "mood_label",
                "mood_score",
                "tags",
                "language"
            ],
        )
        if is_new:
            writer.writeheader()
        writer.writerow(row)


# ---------- エンドポイント本体 ----------

@app.post("/analyze")
def analyze(req: MoodRequest):
    raw_mood = (req.mood_text.value if req.mood_text is not None else "")      # ← セルフ申告（選択肢）
    raw_comment = req.comment or ""     # ← 実際の出来事・気持ち

    combined = (raw_mood + " " + raw_comment).strip()


    # 言語は自動判定（さっきのロジック）
    lang_hint = (req.language or "").lower()
    if lang_hint in ("en", "ja"):
        lang = lang_hint
    else:
        lang = detect_language_from_text(combined)


    # ★スコアリングにどのテキストを使うか決める
    # 　comment があれば comment を優先、なければ mood_text も使う
    analysis_text = raw_comment or raw_mood


    label = detect_mood(analysis_text, lang)
    score = mood_score(label, analysis_text)
    tags = extract_tags(analysis_text, lang)
    comment = build_comment(label, score, tags, lang)


    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_id": req.user_id or "honoka",
        "mood_text": raw_mood,        # ← セルフ申告
        "comment": raw_comment,       # ← テキスト詳細
        "mood_label": label,
        "mood_score": score,
        "tags": "|".join(tags),
        "language": lang,
    }
    append_log(row)


    return {
        "language": lang,
        "mood_label": label,
        "mood_score": score,
        "tags": tags,
        "comment": comment,
    }

# chattomo 起動
#  python -m uvicorn chattomo_api:app --reload