import pandas as pd
import re
import ast  # 用于安全地将字符串转换为 Python 对象

# 读取CSV文件
df = pd.read_csv('try1.csv', header=None)

# 提取 "Keypoints": 到 ,"KeypointConfidence" 之间的内容
def extract_keypoints(text):
    match = re.search(r'"Keypoints"\s*:\s*(\[.*?\])\s*,\s*"KeypointConfidence"', text)
    return match.group(1) if match else None

# 新增列：提取 Keypoints 原始字符串
df['ExtractedKeypoints'] = df[1].apply(extract_keypoints)

# 将 JSON 字符串转为 Python 列表并提取第 27、28、30 个 keypoint
def get_keypoint(json_str, index):
    try:
        keypoints = ast.literal_eval(json_str)
        return keypoints[index] if index < len(keypoints) else None
    except:
        return None

# 提取面部关键点（索引：26、27、29）
df['面部1'] = df['ExtractedKeypoints'].apply(lambda x: get_keypoint(x, 26))
df['面部2'] = df['ExtractedKeypoints'].apply(lambda x: get_keypoint(x, 27))
df['面部3'] = df['ExtractedKeypoints'].apply(lambda x: get_keypoint(x, 29))

# 保存新表格
df.to_csv('output.csv', index=False)