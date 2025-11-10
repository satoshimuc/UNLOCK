
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from fastapi_mcp import FastApiMCP

JST = timezone(timedelta(hours=9))

app = FastAPI(title="UNLOCK MCP Server")

# --- MCP wrapper ---
mcp = FastApiMCP(app, name="unlock-morning-program")
mcp.mount()

class MorningArgs(BaseModel):
    difficulty: str | None = None  # "easy" | "standard" | "hard"

def _program(difficulty: str = "standard"):
    today = datetime.now(JST).strftime("%Y-%m-%d")
    # ZEN section
    zen = {
        "title": "ZEN（3–4分）",
        "timer": "3–4分",
        "guide": [
            "姿勢：椅子に浅く座り、背骨をすっと伸ばす。両足は床にフラット。",
            "呼吸：4秒吸う→2秒止める→6秒吐く を繰り返す（鼻で）。",
            "意識：吐く息の長さと肩の脱力に注意。雑念は『ラベル付け→流す』。",
            "終了合図：最後の吐息のあと、そっと目を開けて伸び。"
        ],
        "time_cues": ["00:00 開始", "01:30 体の力みチェック", "03:00 仕上げの1呼吸"]
    }

    # Life Kinetik drill (uses household items)
    drill = {
        "name": "左右非対称タッチ＆読み上げ（ボール or お手玉1個＋紙）",
        "base": [
            "右手にボール（またはお手玉）。左手は空けておく。",
            "床にA/B/Cの文字を書いた紙を3枚置く（前・左・右）。",
            "合図：数字を1つ声に出す→その数だけ拍手→指定の文字にタッチ。",
        ],
        "easy": [
            "拍手は1回固定、文字指定は1種類のみ（例：Aだけ）。",
            "左右の手は入れ替えなし。"
        ],
        "standard": [
            "拍手は1〜3回ランダム、文字指定はA/B/Cから毎回変更。",
            "ボールを右手→左手に投げ替えてからタッチ。"
        ],
        "hard": [
            "拍手は1〜5回、文字はA/B/Cに加えて『数字の合計が偶数なら左、奇数なら右』など条件分岐を追加。",
            "タッチと同時に『色』を英語で読み上げる（例：Red/Blue/Green）。"
        ],
        "duration": "6–7分"
    }

    # choose variant by difficulty
    variant = drill["easy"] if difficulty == "easy" else drill["hard"] if difficulty == "hard" else drill["standard"]

    lk = {
        "title": "ライフキネティック（6–7分）",
        "drill_name": drill["name"],
        "how_to": drill["base"] + variant,
        "time_cues": ["00:00 ウォームアップ", "02:00 ベース動作", "04:00 バリエーション追加", "06:30 クールダウン"]
    }

    presenteeism = {
        "title": "プレゼンティズムチェック",
        "before_prompt": "開始前の自己生産性スコア（0–10）を入力してください。",
        "after_prompt": "終了後の自己生産性スコア（0–10）を入力してください。",
        "delta_note": "Δ（後−前）を計算して1文でフィードバックしてください。"
    }

    reflection = {
        "title": "Reflection",
        "ask_3gt": "『昨日の3 Good Things』を3つ書いてください。",
        "fallback": "もし書けなければ、今日の『小さなビジネスアイデア』を1つ提案します。",
        "ack": "入力を要約し、『受け取りました』と短く確認してください。"
    }

    return {
        "date": today,
        "sections": [zen, lk, presenteeism, reflection],
        "closing": "Good start! 60点で十分、明日は61点。"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@mcp.tool(name="run_morning_program", title="Run UNLOCK Morning Program")
def run_morning_program(args: MorningArgs | None = None):
    difficulty = (args.difficulty if args else None) or "standard"
    return _program(difficulty)
