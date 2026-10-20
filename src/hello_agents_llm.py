import os

from openai import OpenAI
from dotenv import load_dotenv
#eg：将env文件里的东西加载到环境变量里面，使用os来进行读取，用os。getenv来读取
from typing import List, Dict
#typing是类型提示，eg：不用的话是def add（a：int） -> int返回值和函数的类型都是int，而更复杂的Dict字典和List列表都要用模块来提示

from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class HelloAgentsLLM:
    """
    为项目封装的LLM调用类，用于调用任意的大模型，默认使用流式相应
    """
    def __init__(self, model:str = None, aipkey:str = None, baseurl:str = None, timeout:int = 60):
        """
        初始化客户端，优先使用传入参数，没有使用环境变量参数
        :param model: 模型名称，例如 gpt-3.5-turbo；不传就读取环境变量 MODEL
        :param apikey: API密钥；不传就读取环境变量 API_KEY
        :param baseurl: 接口地址；不传就读取环境变量 BASE_URL
        :param timeout: 请求超时时间，单位秒；不传就读取环境变量 TIMEOUT
        :return: 客户端实例
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        aipkey = aipkey or os.getenv("LLM_API_KEY")
        baseurl = baseurl or os.getenv("LLM_BASE_URL")
        timeout = timeout or os.getenv("LLM_TIMEOUT")
        #test
        #print(self.model, aipkey, baseurl, timeout)

        if not all([self.model, aipkey, baseurl, timeout]):
            raise ValueError("模型ID，API密钥和服务地址必须被提供或在.env文件中定义")

        self.client = OpenAI(api_key=aipkey, base_url=baseurl, timeout=timeout)

    def think(self, messages:List[Dict[str,str]], temperature:float= 0) -> str :
        """
        调用大语言模型进行思考，并返回响应
        :param messages: 对话消息列表，里面每一条是字典，包含role和content，例：[{"role":"user","content":"你好"}]
        :param temperature: 温度系数，控制回答随机性，范围0~2；越小回答越确定，越大越有创造力；不传则读取环境变量
        :return: 返回模型回答文本字符串
        """
        print(f"🧠正在调用{self.model}模型...")

        try:
            response = self.client.chat.completions.create(#type:ignore
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
        #处理流式响应
            print("✅大语言模型响应成功")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                #eg:chunk是小流式段，每个是你，第一个，然后好，delta增量，content内容
                print(content, end="", flush=True)
                #eg:flush是一个字一个字打印，end是结束，默认是换行
                collected_content.append(content)
            print()
            return "".join(collected_content)


        except Exception as e:
            print(f"❌调用LLM API时发生错误:{e}")
            return None

#客户端使用示例
if __name__ == "__main__":

    #测试用的，别的模块导入的时候不会跑
    try:
        agent = HelloAgentsLLM()

        exampleMessages = [
            {"role":"system", "content":"你是一个严谨负责的python工程师，遇到问题时会先构建一个框架，输出对应的技术文档."},
            {"role":"user", "content":"我希望将一个python代码文件有一个网页前端来调用，我该怎么做"}
        ]
        print("🧠——————调用LLM模型————————")
        responseText = agent.think(exampleMessages, temperature=1)
        if responseText:
            print("\n\n----模型响应结束----")
            #print(responseText)

    except ValueError as e:
        print(f"调用LLM模型错误：{e}")





