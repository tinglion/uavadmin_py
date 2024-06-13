)
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser,ResponseSchema
from langchain_core.prompts import PromptTemplate
import datetime
import openai
import json
import os
import sys
import json
from dotenv import load_dotenv
import logging
import warnings
from uavadmin.utils.markdown_json import MarkDownJsonToStandard
OPENAI_API_BASE = "http://10.19.53.220:9501/api/v1/0d198701463ca262"
logger = logging.getLogger(__name__)
# GPT_MODEL = "gpt-4-0613"
# GPT_MODEL = "gpt-3.5-turbo-16k"
# GPT_MODEL = (
#     "gpt-4-1106-preview" if datetime.date.today() <= datetime.date(2025, 9, 15) else "gpt-4"
# )
# from logging import logger
import os
from openai import OpenAI

# openai.api_key = key
client = OpenAI(
    # This is the default and can be omitted
    # api_key=os.environ.get("OPENAI_API_KEY"),   
    api_key=key
)
import re
def extract_json_from_markdown(markdown_string):
    # 从 Markdown 字符串中提取 JSON 内容
    json_match = re.search(r'```json\n(.*)\n```', markdown_string, re.DOTALL)
    if json_match:
        json_content = json_match.group(1)
        content = json.loads(json_content)
        return content
    else:
        return None
def open_ask_llm_by_str(prompt):
    model_name = 'gpt-4o'  # 使用 text-davinci-003 模型代替 gpt-4-turbo
    try:
        logger.info(f"{len(prompt)}-提取中")
        # 创建聊天完成请求
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
            temperature=0.95
        )
        # breakpoint()
        logger.info(f"{len(prompt)}-提取完成")
        output = completion.choices[0].message.content
        standard_json = MarkDownJsonToStandard(output).process_markdown_json()
     
    except Exception as e:
        logger.error("openai.run 异常{}".format(e))
        standard_json = None  # 设置为 None，表示提取失败
    return standard_json, model_name

def open_ask_llm_by_str_beautiful(prompt):
    model_name = 'gpt-4o'  
    try:
        logger.info(f"{len(prompt)}-提取中")
        # 创建聊天完成请求
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
        )
        logger.info(f"{len(prompt)}-提取完成")
        # breakpoint()
        output = completion.choices[0].message.content
    except Exception as e:
        logger.error("openai.run 异常{}".format(e))
        output = None  # 设置为 None，表示提取失败
    return output, model_name
# API_URL = "http://172.17.53.219:9501/api/v1/856e6fce9c2a9f2a"
# OPENAI_API_BASE = "http://172.17.53.219:9501/api/v1/856e6fce9c2a9f2a"

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
# load_dotenv(dotenv_path="key.env")
# warnings.filterwarnings("ignore")
os.environ["OPENAI_API_KEY"] = key
   
llm = ChatOpenAI(
temperature=0.1,
model='gpt-4-turbo',
openai_api_base=OPENAI_API_BASE,
streaming=True,
)
      
def ask_llm(input, schemas, template):
        output_parser = StructuredOutputParser.from_response_schemas(schemas)
        format_instructions = output_parser.get_format_instructions()
        prompt = PromptTemplate(
            template=template,
            input_variables=["input"],
            partial_variables={"format_instructions": format_instructions},
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        try:
            output = chain.run(input)
        except Exception as e:
            # logger.error("chain.run 异常{}".format(e))
            print("chain.run 异常{}".format(e))
        
        return output

def ask_llm_by_str(prompt):
    model_name = 'gpt-4-turbo'
    llm_openai = ChatOpenAI(model=model_name, openai_api_base=OPENAI_API_BASE, temperature=0, streaming=True)
    try:
        logger.info(f"{len(prompt)}-提取中")
        output = llm_openai.invoke(prompt)
        logger.info(f"{len(prompt)}-提取完成")
        
        standard_json = MarkDownJsonToStandard(output.content).process_markdown_json()
        if not standard_json:  # gpt3.5直接json，gpt4输出markdown json
            standard_json = json.loads(output.content)
    except Exception as e:
        logger.error("chain.run 异常{}".format(e))
    return standard_json, model_name

def ask_llm_by_str_beautiful(prompt):
    model_name = 'gpt-4-turbo'
    llm_openai = ChatOpenAI(model=model_name, openai_api_base=OPENAI_API_BASE, temperature=0, streaming=True)
    try:
        logger.info(f"{len(prompt)}-提取中")
        output = llm_openai.invoke(prompt)
        logger.info(f"{len(prompt)}-提取完成")
    except Exception as e:
        logger.error("chain.run 异常{}".format(e))
    return output.content


# if __name__ == "__main__":
#     txts="""多发性骨髓瘤
#     本品可联合美法仑和泼尼松（MP方案）用于既往未经治疗的且不适合大剂量化疗和骨髓抑制的多发性骨髓瘤患者的治疗；或单药用于至少接受过一种或一种以上治疗后复发的多发性骨髓瘤患者的治疗。
#     套细胞淋巴瘤
#     本品可联合利妥昔单抗、环磷酰胺、多柔比星和泼尼松，用于既往未经治疗的并且不适合接受造血干细胞移植的套细胞淋巴瘤成人患者；或用于复发或难治性套细胞淋巴瘤患者的治疗，患者在使用本品前至少接受过一种治疗。"""

# schemas=[ResponseSchema(name="疾病名称",description="若有多个疾病以列表形式输出",type="string")]
# res = ask_llm(txts,schemas,template)
# json_res = MarkDownJsonToStandard(res).process_markdown_json()
# print(json_res)

