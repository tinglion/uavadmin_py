import json
import traceback


class MarkDownJsonToStandard:
    def __init__(self, markdown_json):
        self.markdown_json = markdown_json
        # self.process_markdown_json()

    """ 
     两种格式的markdown-json
     ```json
     {}
     ```

     ```json
     [
        {},
        {}
     ]
     ```

     解析失败情况
     ```json{}```
     ```json{}```
"""

    ## TODO
    def process_markdown_json(self):
        # 去除换行和空格
        self.markdown_json = self.markdown_json.strip()

        # '解析会报错，全部替换为"
        tmp_md_json = self.markdown_json.replace("'", '"')
        json_list = []
        while len(tmp_md_json) > 0:
            posi_start = tmp_md_json.find("```json")
            if posi_start < 0:
                break

            posi_end = tmp_md_json.find("```", posi_start + 7)
            if posi_end < 0:
                # break
                posi_end = len(tmp_md_json)
            json_str = tmp_md_json[posi_start + 7 : posi_end]
            # print(f"jsonstr({posi_start}, {posi_end}) {json_str} ")
            if len(json_str) > 2:
                obj = None
                try:
                    obj = json.loads(json_str)
                except Exception as e:
                    print(f"json format error ^{tmp_md_json}$")
                    if json_str.find("{") >= 0:
                        # baichuan  {},{}
                        try:
                            obj = json.loads(f"[{json_str}]")
                        except Exception as e:
                            traceback.print_exc()
                    else:
                        obj = json_str
                if obj:
                    json_list.append(obj)
                tmp_md_json = tmp_md_json[posi_end + 3 :]

        return json_list if len(json_list) != 1 else json_list[0]