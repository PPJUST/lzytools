import re
import subprocess
from typing import Tuple

from lzytools.common import send_data_to_socket

"""
| Code | Meaning                         | 翻译                                               |
|------|---------------------------------|--------------------------------------------------|
| 0    | No error                        | 无错误                                              |
| 1    | Warning (Non fatal error(s)).   | 警告 (非致命错误)。<br/>例如，一个或多个文件被其他某个应用程序锁定，因此它们没有被压缩。 |
| 2    | Fatal error                     | 致命错误                                             |
| 7    | Command line error              | 命令行错误                                            |
| 8    | Not enough memory for operation | 内存不足，无法进行操作                                      |
| 255  | User stopped the process        | 用户已停止该进程                                         |
"""

_PATH_7ZIP = None
_HOST = '127.0.0.1'
_PORT = '7219'


def check_7zip_path():
    """检查设置的7zip路径"""
    if not _PATH_7ZIP:
        raise Exception('未指定7Zip路径')


def subprocess_7zip_lt(command_type: str, filepath: str, password: str,
                       inside_path=None) -> subprocess.CompletedProcess:
    """外部调用7zip（l或t指令），返回结果
    :param command_type: l或t指令
    :param filepath: 测试的压缩文件路径
    :param password: 测试的解压密码
    :param inside_path: 指定测试的内部文件路径（只在t指令时使用）
    :return: 7zip调用结果"""
    check_7zip_path()

    command = [_PATH_7ZIP,
               command_type,
               filepath,
               "-p" + password]
    if command_type == 't' and inside_path:  # 在使用t指令时，指定测试的内部路径可以加快测速速度
        command.append(inside_path)
    print(f'调用7zip：{" ".join(command)}')
    process = subprocess.run(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW,
                             text=True,
                             universal_newlines=True)

    return process


def analyse_return(process: subprocess.CompletedProcess) -> Tuple[int, str]:
    """分析调用7zip的返回结果
    :param process: 7zip调用结果
    :return: 7zip返回码，返回码对应解释"""
    return_code = process.returncode
    if return_code == 0:
        return 0, 'No error'
    elif return_code == 1:
        return 1, 'Warning (Non fatal error)'
    elif return_code == 2:
        output = str(process.stderr) + str(process.stdout)
        if 'Wrong password' in output:
            return 2, 'Wrong password'
        elif 'Missing volume' in output:
            return 2, 'Missing volume'
        elif 'Cannot open the file as' in output:
            return 2, 'Cannot open the file'
        else:
            return 2, 'Unknown error'
    elif return_code == 7:
        return 7, 'Command line error'
    elif return_code == 8:
        return 8, 'Not enough memory for operation'
    elif return_code == 255:
        return 255, 'User stopped the process'
    else:
        return 2, 'Unknown error'  # 兜底


def read_stdout(process: subprocess.CompletedProcess):
    """读取返回结果中的stdout信息，提取文件列表"""
    stdout = process.stdout
    files_dict = {'filetype': None, 'paths': None}
    if stdout:
        text_splits = stdout.splitlines()
    else:
        return files_dict

    # 提取文件类型
    cut_splits = [i for i in text_splits if i.startswith('Type = ')]
    if cut_splits:
        cut_text = [i for i in text_splits if i.startswith('Type = ')][0]
        filetype = cut_text[len('Type = '):]
        files_dict['filetype'] = filetype

    # 提取内部文件路径
    start_index = None
    end_index = None
    for index, i in enumerate(text_splits):
        if i.startswith('   Date'):
            start_index = index
        if i.startswith('----------'):
            end_index = index
    if start_index or end_index:
        column_name_index = text_splits[start_index].find('Name')
        cut_text = text_splits[start_index + 2:end_index]
        paths = [i[column_name_index:] for i in cut_text if 'D....' not in i]
        files_dict['paths'] = paths

    return files_dict


def subprocess_7zip_x(filepath: str, password: str, extract_dirpath: str, filter_rule: list) -> tuple[int, str]:
    """外部调用7zip（x指令），返回结果
    :param filepath: 压缩文件路径
    :param password: 解压密码
    :param extract_dirpath: 解压路径
    :param filter_rule: 过滤器，不解压的文件规则
    :return: 7zip返回码，返回码对应解释"""
    # 同时读取stdout和stderr会导致管道堵塞，需要将两个输出流重定向至同一个管道中，使用switch：'bso1','bsp1',bse1'
    command = ([_PATH_7ZIP, 'x', '-y', filepath,
                '-bsp1', '-bse1', '-bso1',
                '-o' + extract_dirpath,
                '-p' + password]
               + filter_rule)

    print(f'调用7zip：{" ".join(command)}')
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               creationflags=subprocess.CREATE_NO_WINDOW,
                               text=True,
                               universal_newlines=True)

    # 读取输出流
    # （使用subprocess.Popen调用7zip时，返回码为2时的报错信息为"<_io.TextIOWrapper name=4 encoding='cp936'>"，
    # 无法正确判断错误事件，所以需要在实时输出的输出流中进行读取判断）
    code_text = None  # 返回码对应文本
    pre_progress = 0  # 解压进度
    is_read_stderr = True  # 是否读取stderr流，出现报错事件/读取到进度信息后不再需要读取
    is_read_progress = True  # 是否读取进度信息，出现报错事件后不再需要读取
    while True:
        try:
            output = process.stdout.readline()
            print(f'7zip实时输出文本：\n{output}')  # 测试用
        except UnicodeDecodeError:  # UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 32: illegal multibyte sequence
            output = ''
        if output == '' and process.poll() is not None:  # 读取到空文本或返回码时，结束读取操作
            break

        # 读取错误事件
        if is_read_stderr and output:
            is_wrong_password = re.search('Wrong password', output)
            is_missing_volume = re.search('Missing volume', output)
            is_cannot_open_the_file = re.search('Cannot open the file as', output)
            if is_wrong_password:
                code_text = 'Wrong password'
                is_read_stderr = False
                is_read_progress = False
            elif is_missing_volume:
                code_text = 'Missing volume'
                is_read_stderr = False
                is_read_progress = False
            elif is_cannot_open_the_file:  # 如果是为指定后缀的问题，7zip会自动尝试以正确格式进行解压，不需要停止读取
                code_text = 'Cannot open the file as'

        # 读取进度事件
        if is_read_progress and output:
            # 单文件进度输出示例：34% - 061-090；多文件进度输出示例：19% 10 - 031-060。适用正则表达式 '(\d{1,3})% *\d* - '
            # 部分压缩文件的输出示例：80% 13。适用正则表达式 '(\d{1,3})% *\d*'
            match_progress = re.search(r'(\d{1,3})% *\d*', output)
            if match_progress:
                is_read_stderr = False
                current_progress = int(match_progress.group(1))  # 提取进度百分比（不含%）
                if current_progress > pre_progress:
                    send_data_to_socket(current_progress, _HOST, _PORT)  # 使用socket传递数据
                    pre_progress = current_progress  # 更新进度

    # 结束后读取返回码
    return_code = process.poll()
    if return_code == 0:
        return 0, 'No error'
    elif return_code == 1:
        return 1, 'Warning (Non fatal error)'
    elif return_code == 2:
        if not code_text:
            code_text = 'Unknown error'  # 兜底
        return 2, code_text
    elif return_code == 7:
        return 7, 'Command line error'
    elif return_code == 8:
        return 8, 'Not enough memory for operation'
    elif return_code == 255:
        return 255, 'User stopped the process'
    else:  # 兜底
        return 2, 'Unknown error'  # 兜底
