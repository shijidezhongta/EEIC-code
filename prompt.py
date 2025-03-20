import requests
import json

# Dify 配置
API_SERVER = "http://localhost/v1"
WORKFLOW_ENDPOINT = "/workflows/run"
API_KEY = "app-wJj4xcTnWcczWRv01SMMzHGq"
DIFY_USER = "difyuser"

DIFY_API = f"{API_SERVER}{WORKFLOW_ENDPOINT}"

def run_dify_workflow(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {"text": text},  # 确保与工作流输入参数名一致
        "response_mode": "blocking",
        "user": DIFY_USER
    }

    try:
        response = requests.post(DIFY_API, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("完整响应数据：\n", json.dumps(result, indent=2, ensure_ascii=False)) 
        
        return result.get('data', {}).get('outputs', {}).get('outtext', '未找到输出文本') #确保与工作流输出参数名一致
    
    except requests.exceptions.RequestException as e:
        return f"API请求失败: {str(e)}"
    except Exception as e:
        return f"处理错误: {str(e)}"

if __name__ == "__main__":
    input_text = input("请输入要处理的文本: ").strip()
    if not input_text:
        print("错误：输入不能为空")
        exit()
    
    print("\n处理中...")
    output_text = run_dify_workflow(input_text)
    print(output_text)