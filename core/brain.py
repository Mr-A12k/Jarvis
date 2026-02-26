import requests
import json
import re
from core.system_prompt import SYSTEM_PROMPT

class Brain:
    def __init__(self, model="llama3:8b"):
        self.model = model
        self.memory = []
        self.max_memory = 6

    def extract_json(self, text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return None
    
    def evaluate_confidence(self, structured_output):
        threshold = 0.65
        return structured_output["confidence"] >= threshold

    def think(self, user_input):

        self.memory.append({"role": "User", "content": user_input})

        if len(self.memory) > self.max_memory:
            self.memory.pop(0)

        conversation = ""
        for msg in self.memory:
            conversation += f'{msg["role"]}: {msg["content"]}\n'

        full_prompt = f"{SYSTEM_PROMPT}\n\nConversation:\n{conversation}\nJarvis:"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False
            }
        )

        raw_output = response.json()["response"].strip()

        json_text = self.extract_json(raw_output)

        if not json_text:
            return {
                "intent": "error",
                "confidence": 0.0,
                "requires_action": False,
                "response": "No valid JSON detected."
            }

        try:
            structured_output = json.loads(json_text)

            self.memory.append({
                "role": "Jarvis",
                "content": structured_output["response"]
            })
            
            if not self.evaluate_confidence(structured_output):
                structured_output["response"] += "\n\n[⚠️ Low confidence response]"

            return structured_output

        except json.JSONDecodeError:
            return {
                "intent": "error",
                "confidence": 0.0,
                "requires_action": False,
                "response": "JSON parsing failed."
            }