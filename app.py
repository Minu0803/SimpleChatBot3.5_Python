import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI

# OpenAI API 클라이언트 설정
client = OpenAI(api_key='')  # 본인의 API 키를 입력하세요.

# 시스템 메시지 초기화
system_message = "You are a helpful assistant."

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"에러가 발생했습니다: {e}"

def send_message():
    user_input = user_entry.get()
    if not user_input.strip():
        return
    chat_log.insert(tk.END, f"당신: {user_input}\n", "user")
    user_entry.delete(0, tk.END)

    response = generate_response(user_input)
    chat_log.insert(tk.END, f"챗봇: {response}\n\n", "bot")
    chat_log.see(tk.END)  # 스크롤을 맨 아래로 이동

def save_chat_log():
    try:
        with open("chat_log.txt", "w", encoding="utf-8") as file:
            file.write(chat_log.get("1.0", tk.END).strip())
        chat_log.insert(tk.END, "\n[시스템] 채팅 로그가 chat_log.txt 파일에 저장되었습니다.\n", "system")
    except Exception as e:
        chat_log.insert(tk.END, f"\n[시스템] 채팅 로그 저장 중 에러 발생: {e}\n", "system")

def clear_chat_log():
    chat_log.delete("1.0", tk.END)
    chat_log.insert(tk.END, "[시스템] 채팅 로그가 초기화되었습니다.\n", "system")

def suggest_prompt():
    examples = [
        "오늘의 날씨는 어때?",
        "파이썬 프로그래밍 언어에 대해 설명해줘.",
        "GPT란 무엇인가?",
        "간단한 요리법을 추천해줘.",
        "하루를 잘 보내기 위한 팁이 있을까?"
    ]
    suggestion = "\n".join([f"{i+1}. {ex}" for i, ex in enumerate(examples)])
    chat_log.insert(tk.END, f"\n[추천 질문]\n{suggestion}\n", "system")

def set_topic():
    global system_message
    topic = user_entry.get().strip()
    if not topic:
        chat_log.insert(tk.END, "\n[시스템] 토픽을 입력해주세요.\n", "system")
        return
    system_message = f"You are an assistant knowledgeable about {topic}."
    chat_log.insert(tk.END, f"\n[시스템] 대화 주제가 '{topic}'(으)로 설정되었습니다.\n", "system")
    user_entry.delete(0, tk.END)

# GUI 초기 설정
root = tk.Tk()
root.title("OpenAI 챗봇")
root.geometry("700x800")
root.configure(bg="#2c3e50")

# 채팅 로그 표시 영역
chat_frame = tk.Frame(root, bg="#ecf0f1", padx=10, pady=10)
chat_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

chat_log = scrolledtext.ScrolledText(
    chat_frame, wrap=tk.WORD, bg="#ffffff", fg="#2c3e50",
    font=("Arial", 12), padx=10, pady=10, relief=tk.FLAT
)
chat_log.pack(fill=tk.BOTH, expand=True)
chat_log.tag_config("user", foreground="#2980b9", font=("Arial", 12, "bold"))
chat_log.tag_config("bot", foreground="#16a085", font=("Arial", 12))
chat_log.tag_config("system", foreground="#e67e22", font=("Arial", 12, "italic"))

# 사용자 입력 필드
input_frame = tk.Frame(root, bg="#2c3e50")
input_frame.pack(padx=15, pady=10, fill=tk.X)

user_entry = tk.Entry(
    input_frame, bg="#ffffff", fg="#2c3e50",
    font=("Arial", 14), relief=tk.FLAT, highlightthickness=1, highlightbackground="#95a5a6"
)
user_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
user_entry.bind("<Return>", lambda event: send_message())

# 버튼 설정
def on_hover(event, button):
    button.configure(bg="#2980b9", fg="#000000")

def on_leave(event, button):
    button.configure(bg="#3498db", ffg="#000000")

send_button = tk.Button(
    input_frame, text="전송", bg="#3498db", fg="#000000",
    font=("Arial", 12, "bold"), padx=20, pady=5, relief=tk.FLAT,
    command=send_message
)
send_button.pack(side=tk.RIGHT, padx=5, pady=5)
send_button.bind("<Enter>", lambda e: on_hover(e, send_button))
send_button.bind("<Leave>", lambda e: on_leave(e, send_button))

save_button = tk.Button(
    input_frame, text="저장", bg="#27ae60", fg="#000000",
    font=("Arial", 12, "bold"), padx=10, pady=5, relief=tk.FLAT,
    command=save_chat_log
)
save_button.pack(side=tk.RIGHT, padx=5, pady=5)

clear_button = tk.Button(
    input_frame, text="초기화", bg="#e74c3c", fg="#000000",
    font=("Arial", 12, "bold"), padx=10, pady=5, relief=tk.FLAT,
    command=clear_chat_log
)
clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

suggest_button = tk.Button(
    input_frame, text="추천 질문", bg="#f39c12", fg="#000000",
    font=("Arial", 12, "bold"), padx=10, pady=5, relief=tk.FLAT,
    command=suggest_prompt
)
suggest_button.pack(side=tk.RIGHT, padx=5, pady=5)

topic_button = tk.Button(
    input_frame, text="토픽 설정", bg="#8e44ad", fg="#000000",
    font=("Arial", 12, "bold"), padx=10, pady=5, relief=tk.FLAT,
    command=set_topic
)
topic_button.pack(side=tk.RIGHT, padx=5, pady=5)

# GUI 실행
root.mainloop()