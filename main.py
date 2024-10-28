import urllib.request
import re
import os
from datetime import datetime

# 定义要访问的多个URL
urls = [
    'https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
    'https://raw.githubusercontent.com/Guovin/TV/gd/result.txt',
    'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
    'https://m3u.ibert.me/txt/fmml_ipv6.txt',
    'https://m3u.ibert.me/txt/ycl_iptv.txt',
    'https://m3u.ibert.me/txt/y_g.txt',
    'https://m3u.ibert.me/txt/j_home.txt',
    'https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt',
    'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
    'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
    'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt',
    'https://raw.githubusercontent.com/fenxp/iptv/main/live/tvlive.txt',
    'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
]

# 定义多个对象用于存储不同内容的行文本
sh_lines = []
ys_lines = []
ws_lines = []
ty_lines = []
dy_lines = []
dsj_lines = []
gat_lines = [] # 港澳台
gj_lines = [] # 国际台
jlp_lines = [] # 纪录片
dhp_lines = [] # 动画片
xq_lines = [] # 戏曲
js_lines = [] # 解说
cw_lines = [] # 春晚
mx_lines = [] # 明星
ztp_lines = [] # 主题片
zy_lines = [] # 综艺频道

other_lines = []

def process_name_string(input_str):
    parts = input_str.split(',')
    processed_parts = []
    for part in parts:
        processed_part = process_part(part)
        processed_parts.append(processed_part)
    result_str = ','.join(processed_parts)
    return result_str

def process_part(part_str):
    if "CCTV" in part_str:
        part_str = part_str.replace("IPV6", "")
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip():
            filtered_str = part_str.replace("CCTV", "")
        return "CCTV-" + filtered_str
        
    elif "卫视" in part_str:
        pattern = r'卫视「.*」'
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str
    
    return part_str

def process_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            text = data.decode('utf-8')
            channel_name = ""
            channel_address = ""

            lines = text.split('\n')
            for line in lines:
                if "#genre#" not in line and "," in line and ":" in line:
                    channel_name = line.split(',')[0].strip()
                    channel_address = line.split(',')[1].strip()
                    if "CCTV" in channel_name:
                        ys_lines.append(process_name_string(line.strip()))
                    elif "卫视" in channel_name:
                        ws_lines.append(process_name_string(line.strip()))
                    elif "体育" in channel_name:
                        ty_lines.append(process_name_string(line.strip()))
                    elif channel_name in dy_dictionary:
                        dy_lines.append(process_name_string(line.strip()))
                    elif channel_name in dsj_dictionary:
                        dsj_lines.append(process_name_string(line.strip()))
                    elif channel_name in sh_dictionary:
                        sh_lines.append(process_name_string(line.strip()))
                    elif channel_name in gat_dictionary:
                        gat_lines.append(process_name_string(line.strip()))
                    elif channel_name in gj_dictionary:
                        gj_lines.append(process_name_string(line.strip()))
                    elif channel_name in jlp_dictionary:
                        jlp_lines.append(process_name_string(line.strip()))
                    elif channel_name in dhp_dictionary:
                        dhp_lines.append(process_name_string(line.strip()))
                    elif channel_name in xq_dictionary:
                        xq_lines.append(process_name_string(line.strip()))
                    elif channel_name in js_dictionary:
                        js_lines.append(process_name_string(line.strip()))
                    elif channel_name in cw_dictionary:
                        cw_lines.append(process_name_string(line.strip()))
                    elif channel_name in mx_dictionary:
                        mx_lines.append(process_name_string(line.strip()))
                    elif channel_name in ztp_dictionary:
                        ztp_lines.append(process_name_string(line.strip()))
                    elif channel_name in zy_dictionary:
                        zy_lines.append(process_name_string(line.strip()))
                    else:
                        other_lines.append(line.strip())
    except Exception as e:
        print(f"处理URL时发生错误：{e}")

current_directory = os.getcwd()

def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

dy_dictionary = read_txt_to_array('电影.txt')
dsj_dictionary = read_txt_to_array('电视剧.txt')
sh_dictionary = read_txt_to_array('shanghai.txt')
gat_dictionary = read_txt_to_array('港澳台.txt')
gj_dictionary = read_txt_to_array('国际台.txt')
jlp_dictionary = read_txt_to_array('纪录片.txt')
dhp_dictionary = read_txt_to_array('动画片.txt')
xq_dictionary = read_txt_to_array('戏曲频道.txt')
js_dictionary = read_txt_to_array('解说频道.txt')
cw_dictionary = read_txt_to_array('春晚.txt')
mx_dictionary = read_txt_to_array('明星.txt')
ztp_dictionary = read_txt_to_array('主题片.txt')
zy_dictionary = read_txt_to_array('综艺频道.txt')

for url in urls:
    print(f"处理URL: {url}")
    process_url(url)

def extract_number(s):
    num_str = s.split(',')[0].split('-')[1]
    numbers = re.findall(r'\d+', num_str)
    return int(numbers[-1]) if numbers else 999

def custom_sort(s):
    if "CCTV-4K" in s:
        return 1
    elif "CCTV-8K" in s:
        return 2
    else:
        return 0

version = datetime.now().strftime("%Y%m%d") + ",http://39.135.138.59:18890/PLTV/88888910/224/3221225622/index.m3u8"

# 根据内容生成 all_lines，只包含有内容的分类
all_lines = ["更新时间,#genre#"] + [version] + ['\n']

if sh_lines:
    all_lines += ["上海频道,#genre#"] + sorted(set(sh_lines)) + ['\n']
if ys_lines:
    all_lines += ["央视频道,#genre#"] + sorted(sorted(set(ys_lines), key=lambda x: extract_number(x)), key=custom_sort) + ['\n']
if ws_lines:
    all_lines += ["卫视频道,#genre#"] + sorted(set(ws_lines)) + ['\n']
if ty_lines:
    all_lines += ["体育频道,#genre#"] + sorted(set(ty_lines)) + ['\n']
if dy_lines:
    all_lines += ["电影频道,#genre#"] + sorted(set(dy_lines)) + ['\n']
if dsj_lines:
    all_lines += ["电视剧频道,#genre#"] + sorted(set(dsj_lines)) + ['\n']
if mx_lines:
    all_lines += ["明星,#genre#"] + sorted(set(mx_lines)) + ['\n']
if ztp_lines:
    all_lines += ["主题片,#genre#"] + sorted(set(ztp_lines)) + ['\n']
if gat_lines:
    all_lines += ["港澳台,#genre#"] + sorted(set(gat_lines)) + ['\n']
if gj_lines:
    all_lines += ["国际台,#genre#"] + sorted(set(gj_lines)) + ['\n']
if jlp_lines:
    all_lines += ["纪录片,#genre#"] + sorted(set(jlp_lines)) + ['\n']
if dhp_lines:
    all_lines += ["动画片,#genre#"] + sorted(set(dhp_lines)) + ['\n']
if xq_lines:
    all_lines += ["戏曲频道,#genre#"] + sorted(set(xq_lines)) + ['\n']
if js_lines:
    all_lines += ["解说频道,#genre#"] + sorted(set(js_lines)) + ['\n']
if zy_lines:
    all_lines += ["综艺频道,#genre#"] + sorted(set(zy_lines)) + ['\n']
if cw_lines:
    all_lines += ["春晚,#genre#"] + sorted(set(cw_lines))

output_file = "merged_output.txt"
others_file = "others_output.txt"
othersA_file = "othersa_output.txt"

try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    print(f"合并后的文本已保存到文件: {output_file}")

    with open(others_file, 'w', encoding='utf-8') as f:
        for line in other_lines:
            f.write(line + '\n')
    print(f"Others已保存到文件: {others_file}")

    # 将 all_lines 和 other_lines 合并写入 othersA_file
    with open(othersA_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    print(f"OthersA已保存到文件: {othersA_file}")
except Exception as e:
    print(f"保存文件时发生错误：{e}")
