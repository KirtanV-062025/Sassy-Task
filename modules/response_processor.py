import re
from flask import jsonify

def process_ai_response(text, token_limit_reached=False):
    lines = text.strip().split('\n')
    lines = [line for line in lines if not re.match(r'^\s*#{1,6}\s+\S+', line.strip())]

    if lines and re.search(r'(?i)(let me know|feel free|need more)', lines[-1]):
        lines.pop(-1)

    if token_limit_reached:
        clean = []
        for line in lines:
            if re.match(r'^\s*(\d+[\.\)]|[-*•])\s+\S+', line.strip()):
                clean.append(line)
            elif line.strip() == "":
                clean.append(line)
            else:
                break
        if clean:
            lines = clean

    joined = '\n'.join(lines)
    result = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', joined)
    result = re.sub(r'^\s*(\d+)[\.\)]\s+(.*)', r'<li>\2</li>', result, flags=re.MULTILINE)

    if '<li>' in result and result.count('<li>') > 1:
        result = '<ul>' + result + '</ul>'

    return result.replace('\n', '<br>')


def generate_chat_response(client, system_prompt, user_input, history):
    conversation = [system_prompt] + [
        {"role": h["role"], "content": h["content"]}
        for h in history if h["role"] in ["user", "assistant"]
    ]
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        max_tokens=200
    )

    reply_raw = response.choices[0].message.content.strip()
    finish_reason = response.choices[0].finish_reason
    reply_processed = process_ai_response(reply_raw, token_limit_reached=(finish_reason == "length"))

    return jsonify({
        "reply": reply_processed,
        "role": "assistant",
        "finish_reason": finish_reason
    })
