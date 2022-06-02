import os
import re
from pathlib import Path
from config import config
from yu_que_request import request as req

# 不在知识库下的文档迁到默认的知识库下
default_book_id = None


def scan_file(home_dir, top_dir, book_id=None, node_uuid=None, dir_name=None):
    """
    扫描目录和文件并上传
    :param home_dir: 要遍历的目录
    :param top_dir: 有道云笔记根目录
    :param book_id: 知识库id
    :param node_uuid: 目录uuid，即文档所在的目录
    :param dir_name: 目录名
    :return:
    """
    files = os.listdir(home_dir)

    for f in files:
        if 'youdaonote-images' in f or f.endswith('.note'):
            continue

        url = os.path.join(home_dir, f)

        if os.path.isfile(url):
            # 替换图片链接
            with open(url, 'r+', encoding='utf-8') as ff:
                text = ff.read()
                text = re.sub(r'!\[\]\((.*(youdaonote-images/.*))\)',
                              lambda m: '![](' + config['image_domain'] + m.group(2) + ')', text)

                ff.seek(0)  # 跳到文件头开始写
                ff.truncate()
                ff.write(text)

            # 上传文档
            print('正在上传：' + url)
            try:
                if str(Path(Path(url).parent).parent) == top_dir:
                    # 在知识库下上传文档
                    req.import_top_doc(book_id, url)
                else:
                    if book_id is not None:
                        # 在目录下上传文档
                        req.import_dir_doc(book_id, url, node_uuid, dir_name)
                    else:
                        # 放在默认知识库
                        global default_book_id
                        if default_book_id is None:
                            default_book_id = req.create_repos('未归档')
                        req.import_top_doc(default_book_id, url)
            except Exception as e:
                print('导入文档出错：', e)

        elif os.path.isdir(url):
            book_id2 = None
            node_uuid2 = None

            if str(Path(url).parent) == top_dir:
                # 顶层目录，创建知识库
                print('正创建知识库：' + f)
                book_id2 = req.create_repos(f)
            elif str(Path(Path(url).parent).parent) == top_dir:
                # 知识库下的一级目录
                print('正创建一级目录：' + f)
                node_uuid2 = req.create_top_dir(book_id, f)
            else:
                # 子目录
                print('正创建子目录：' + f)
                node_uuid2 = req.create_sub_dir(book_id, node_uuid, f)
            scan_file(url, top_dir,
                      (book_id if book_id2 is None else book_id2),
                      (node_uuid if node_uuid2 is None else node_uuid2), f)


if __name__ == '__main__':
    home_dir = config['dir']
    scan_file(home_dir, top_dir=str(Path(home_dir)))
    print('上传完成')
