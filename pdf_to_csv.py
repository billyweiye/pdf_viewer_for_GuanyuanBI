import base64
import os
import pandas as pd
from typing import Optional

def pdf_to_csv(
    input_path: str,
    output_dir: str,
    chunk_size: int = 1024,
    output_filename: Optional[str] = None
) -> str:
    """
    将PDF文件转换为分块Base64编码的CSV文件
    
    参数:
    input_path (str): 输入的PDF文件路径
    output_dir (str): 输出目录路径
    chunk_size (int): 分块大小，默认1024字符
    output_filename (str): 自定义输出文件名（可选）
    
    返回:
    str: 生成的CSV文件路径
    
    异常:
    ValueError: 当输入文件不是PDF或输出目录无效时
    """
    # 参数验证
    if not input_path.lower().endswith('.pdf'):
        raise ValueError("输入文件必须是PDF格式")
    
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成输出文件名
    file_name = output_filename or os.path.splitext(os.path.basename(input_path))[0]
    csv_path = os.path.join(output_dir, f"{file_name}.csv")
    
    # 读取并编码文件
    try:
        with open(input_path, "rb") as pdf_file:
            encoded = base64.b64encode(pdf_file.read()).decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"文件读取/编码失败: {str(e)}")
    
    # 创建并处理DataFrame
    df = pd.DataFrame({"data": [encoded]})
    df["data"] = df["data"].apply(
        lambda x: [x[i:i+chunk_size] for i in range(0, len(x), chunk_size)]
    )
    df = df.explode("data").reset_index(drop=True)
    df = df.rename_axis("order").reset_index()
    
    # 保存结果
    try:
        df.to_csv(csv_path, index=False)
    except Exception as e:
        raise RuntimeError(f"CSV保存失败: {str(e)}")
    
    return csv_path

if __name__ == "__main__":
    # 示例用法
    try:
        result_path = pdf_to_csv(
            input_path="path/to/input.pdf",
            output_dir="path/to/output",
            chunk_size=1024
        )
        print(f"转换完成，文件已保存至: {result_path}")
    except Exception as e:
        print(f"处理失败: {str(e)}")