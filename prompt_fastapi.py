from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel

app = FastAPI(title="Dify 工作流代理服务")

# 允许跨域请求（根据前端地址调整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为具体域名
    allow_methods=["POST"]
)

# Dify 配置
DIFY_API = "http://localhost/v1/workflows/run"
API_KEY = "app-wJj4xcTnWcczWRv01SMMzHGq"
DIFY_USER = "difyuser"

# 定义请求体模型（自动校验和生成文档）
class RequestData(BaseModel):
    text: str

@app.post("/process")
async def process_text(data: RequestData):
    """
    处理文本并返回 Dify 工作流结果
    
    - **text**: 需要处理的文本内容
    """
    try:
        # 调用 Dify API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {"text": data.text},
            "response_mode": "blocking",
            "user": DIFY_USER
        }
        
        response = requests.post(DIFY_API, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        output = result.get('data', {}).get('outputs', {}).get('outtext', '')
        
        # 打印结果（服务端日志）
        print(f"\n处理结果：{output}")
        
        return {"status": "success", "result": output}
    
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Dify API 错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)