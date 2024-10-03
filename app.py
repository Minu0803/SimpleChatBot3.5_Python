from openai import OpenAI

client = OpenAI(api_key='Yout-api-Key')

# OpenAI API 키 설정 (발급받은 API 키로 교체)

def generate_response(prompt):
    try:
        # ChatCompletion API를 사용한 대화 생성
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # 또는 비용을 줄이기 위해 'gpt-3.5-turbo-0301' 모델도 사용 가능
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,  # 응답의 최대 토큰 수
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"에러가 발생했습니다: {e}"

def chat():
    print("OpenAI 챗봇에 오신 것을 환영합니다! (종료하려면 '잘 가'라고 입력하세요.)")
    while True:
        user_input = input("당신: ")
        if user_input.lower() in ["잘 가", "종료"]:
            print("챗봇: 안녕히 가세요!")
            break
        response = generate_response(user_input)
        print(f"챗봇: {response}")

if __name__ == "__main__":
    chat()