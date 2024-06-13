import tiktoken

class TokenCalculate:
    def __init__(self,model) -> None:
        self.model = model
    def token_count(self,string):
        encoding = tiktoken.encoding_for_model(self.model)   #gpt-4/gpt-3.5-turbo
        token_num = len(encoding.encode(string))
        return token_num
    def calculate_price(self,input_tokens, output_tokens):
       
        # 检查模型是否在价格信息中
        if self.model not in price_info:
            return "请检查使用的模型是否在价格表中"
        # 获取模型的价格信息
        model_info = price_info[self.model]
        # 计算输入和输出价格
        input_price = input_tokens / 1000 * model_info["input_price_per_1k_tokens"]
        output_price = output_tokens / 1000 * model_info["output_price_per_1k_tokens"]
        # 总价格
        total_price = input_price + output_price
        return total_price
# calculate = TokeCalculate("gpt-3.5-turbo")
# str = """
# {'开始日期': '2017-04', '结束日期': '2017-09-22', '药品通用名': ['培美曲塞', '顺铂', 'DP']}
# """
# token_in = calculate.token_count(str)
# print(token_in)