import os
import requests
import ollama
import openai

# Abstract base class for AI response generation
class AIService:
    def generate_response(self, prompt):
        raise NotImplementedError("This method should be implemented by subclasses.")

# Local AI Model (Ollama)
class OllamaService(AIService):
    def generate_response(self, prompt):
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

# Cloud-based AI Model (Claude - Anthropic API)
class ClaudeService(AIService):
    def generate_response(self, prompt):
        ANTHROPIC_API_KEY = os.getenv("CLAUDE_API_KEY")
        CLAUDE_URL = "https://api.anthropic.com/v1/complete"
        
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "model": "claude-2",
            "prompt": prompt,
            "max_tokens_to_sample": 200
        }
        response = requests.post(CLAUDE_URL, headers=headers, json=data)
        return response.json()["completion"]

# Cloud-based AI Model (OpenAI - GPT-4 API)
class OpenAIService(AIService):
    def generate_response(self, prompt):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        openai.api_key = OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

# Factory function to dynamically select AI model
def get_ai_service():
    ai_provider = os.getenv("AI_PROVIDER", "ollama").lower()
    
    if ai_provider == "ollama":
        return OllamaService()
    elif ai_provider == "claude":
        return ClaudeService()
    elif ai_provider == "openai":
        return OpenAIService()
    else:
        raise ValueError(f"Unknown AI provider: {ai_provider}")
