from xblock.core import XBlock
from xblock.fields import String, Integer, Scope
import requests
import json
from web_fragments.fragment import Fragment
from xblockutils.resources import ResourceLoader
#
#for self.resource_string css, js
loader = ResourceLoader(__name__)

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
    model_type = String(
        display_name="Model Type", 
        default="llama", 
        scope=Scope.settings
    )
    deepseek_api_key = String(
        display_name="DeepSeek API Key", 
        default="<Your DeepSeek API Key>", 
        scope=Scope.settings
    )

    def student_view(self, context=None):
        context = context or {}  # 初始化 context
        context['prompt'] = self.prompt  # 从 XBlock 字段中获取 prompt  
        context['response'] = self.response  # 将 response 字段添加到 context 中 
        html = self.render_template("student_view.html", context) 
        frag = Fragment(html)
     #   frag.add_css(self.resource_string("static/css/xblock_llama.css"))
     #   frag.add_javascript(self.resource_string("static/js/xblock_llama.js"))
        frag.initialize_js('LlamaXBlock', json_args=context)  # 初始化 JavaScript
        return frag

    def studio_view(self, context=None):
        context = context or {}
        context['display_name'] = self.display_name
        context['model_type'] = self.model_type
        context['deepseek_api_key'] = self.deepseek_api_key

        html = self.render_template("studio_view.html", context)
        frag = Fragment(html)
    #    frag.add_css(self.resource_string("static/css/xblock_llama.css"))
    #    frag.add_javascript(self.resource_string("static/js/xblock_llama.js"))
        frag.initialize_js('LlamaXBlock', json_args=context)  

        return frag
    
    @staticmethod
    def js_init_fn(runtime, element):
        return ""
#        return ""
#            function LlamaXBlock(runtime, element) {
#                // ... XBlock 初始化代码 ...
#            }
#        """

    def get_llama_response(self, prompt):
        try:
            # 替换为你的 Ollama 或 Open WebUI 接口地址
            # api_url = "http://172.31.35.140:11434/api/generate"  
            api_url = "http://172.16.15.56:11434/api/generate"
            headers = {'Content-Type': 'application/json'}
            # Ollama 请求参数
            data = {
                "model": "llama2",  # 替换为你要使用的 Ollama 模型名称
                "prompt": prompt,
                "stream": False,  # 是否流式传输响应，这里设置为 False
                "options": {
                    # 可选参数，根据需要调整
                    "temperature": 0.7,
                    "max_tokens": 100
                }
            }

            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  # 检查请求是否成功

            json_data = response.json()
            # 根据 Ollama 或 Open WebUI 的返回 JSON 结构进行解析
            if "response" in json_data: # 示例：Ollama
                return json_data["response"]
            elif "choices" in json_data: # 示例：Open WebUI
                return json_data["choices"][0]["text"]
            else:
                return "Error: Could not parse response from Ollama"

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

    def get_deepseek_response(self, prompt):
        api_key = self.deepseek_api_key
        if not api_key:
            return "Error: DeepSeek API Key is not set."

        try:
            api_url = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API 地址
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            data = {
                "model": "deepseek-chat",  # DeepSeek 模型名称
                "messages": [{"role": "user", "content": prompt}]
            }

            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()

            json_data = response.json()

            # 解析 DeepSeek 返回的 JSON 数据
            if "choices" in json_data and len(json_data["choices"]) > 0:
                return json_data["choices"][0]["message"]["content"]
            else:
                return "Error: Could not parse response from DeepSeek"

        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"
        
    def get_deepseek_r1_1_5b_response(self, prompt):
        try:
            # Ollama API 地址
            # api_url = "http://172.31.35.140:11434/api/generate"  # 默认端口为 11434
            api_url = "http://172.16.15.56:11434/api/generate" 
            headers = {'Content-Type': 'application/json'}

            # Ollama 请求参数
            data = {
                "model": "deepseek-r1:1.5b",  # 指定 Ollama 模型名称
                "prompt": prompt,
                "stream": False,  # 是否流式传输响应，这里设置为 False
                "options": {
                    # 可选参数，根据需要调整
                    "temperature": 0.7,
                    "max_tokens": 100
                }
            }

            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  # 检查请求是否成功

            json_data = response.json()

            # 解析 Ollama 返回的 JSON 数据
            if "response" in json_data:
                return json_data["response"]
            else:
                return "Error: Could not parse response from Ollama"

        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"

    @XBlock.json_handler
    def get_response(self, data, suffix=''):
        prompt = data.get('prompt')
        model_type = data.get('model_type', 'llama')  # 获取选择的模型类型
        if model_type == 'llama':
            response = self.get_llama_response(prompt)
        elif model_type == 'deepseek':
            response = self.get_deepseek_response(prompt)
        elif model_type == 'deepseek-r1:1.5b':  # 添加 deepseek-r1:1.5b 模型
            response = self.get_deepseek_r1_1_5b_response(prompt)
        else:
            response = "Error: Invalid model type."
        self.response = response
        return {"response": response}    
    
    @XBlock.json_handler
    def save_display_name(self, data, suffix=''):
        display_name = data.get('display_name')
        try:
            self.display_name = display_name  # 保存 display_name
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @XBlock.json_handler
    def save_deepseek_api_key(self, data, suffix=''):
        deepseek_api_key = data.get('deepseek_api_key')
        try:
            self.deepseek_api_key = deepseek_api_key
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @XBlock.json_handler
    def save_model_type(self, data, suffix=''):
        model_type = data.get('model_type')
        try:
            self.model_type = model_type
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}                     
