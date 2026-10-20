from dotenv import load_dotenv
import os

# 当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# .dev 和py同目录
env_path = os.path.join(BASE_DIR,"..", ".env")
# 规范化路径
env_path = os.path.normpath(env_path)

print(f"🔍 环境文件完整路径：{env_path}")
print(f"📄 文件是否存在：{os.path.exists(env_path)}")

# 如果文件存在，打印文件原始内容，直接看读到了什么！
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        raw_content = f.read()
    print("\n===== .dev 文件原始内容 =====")
    print(repr(raw_content))  # repr会显示看不见的换行/空格
    print("===========================\n")

# 加载环境
result = load_dotenv(env_path)
print(f"load_dotenv 返回值（是否成功加载）：{result}")

# 读取变量
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("MODEL")
print(f"OPENAI_API_KEY = {repr(api_key)}")
print(f"OPENAI_BASE_URL = {repr(base_url)}")
print(f"MODEL = {repr(model)}")
