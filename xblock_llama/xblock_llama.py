from xblock.core import XBlock
from xblock.fields import String, Integer, Scope
import requests
import json

class LlamaXBlock(XBlock):
    display_name = String(
        display_name="Llama XBlock", 
        default="Llama", 
        scope=Scope.settings
    )
    prompt = String(
        display_name="Prompt", 
        default="Enter your prompt here", 
        scope=Scope.user_state
    )
    response = String(
        display_name="Response", 
        default="", 
        scope=Scope.user_state
    )

    def student_view(self, context=None):
        return self.render_template("student_view.html", context)

    def studio_view(self, context=None):
        return self.render_template("studio_view.html", context)

    @XBlock.json_handler
    def get_response(self, data, suffix=''):
        prompt = data.get('prompt')
        response = self.get_llama_response(prompt) 
        self.response = response
        return {"response": response}

    def get_llama_response(self, prompt):
        try:
            # 替换为你的 Ollama 或 Open WebUI 接口地址
            api_url = "http://localhost:11434/api/generate"  
            headers = {'Content-Type': 'application/json'}
            data = {"model": "deepseek-r1:1.5b", "prompt": prompt} # 根据你的 API 调整
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  # 检查请求是否成功

            json_data = response.json()
            # 根据 Ollama 或 Open WebUI 的返回 JSON 结构进行解析
            if "response" in json_data: # 示例：Ollama
                return json_data["response"]
            elif "choices" in json_data: # 示例：Open WebUI
                return json_data["choices"][0]["text"]
            else:
                return "Error: Could not parse response"

        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"

    def render_template(self, template_name, context):
        import os
        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'templates', 
            template_name
        )
        with open(template_path, 'r') as f:
            template = f.read()
        return template.format(**context)
    
    @XBlock.json_handler
    def save_display_name(self, data, suffix=''):
        display_name = data.get('display_name')
        try:
            self.display_name = display_name  # 保存 display_name
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}    