import requests as req
import json
import uuid
from config import config

"""
官方文档：https://www.yuque.com/yuque/developer/api
"""


class Request:
    def __init__(self):
        self.session = config['_yuque_session']

    def base_header(self):
        return {
            'authority': 'www.yuque.com', 'accept': 'application/json', 'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'cookie': '_yuque_session={0};'.format(self.session),
            'origin': 'https://www.yuque.com', 'referer': 'https://www.yuque.com/new',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
            # 'x-csrf-token': 'pRoCjgPUZv3R8f9sT_4YF-gA', 'x-requested-with': 'XMLHttpRequest'
        }

    def create_repos(self, name):
        """创建知识库"""
        params = {
            'name': name,
            'type': 'Book',
            'public': 0,
            'slug': str(uuid.uuid4()).split('-')[0],
            'description': '',
            'template': '',
            'cover': '',
            'layout': 'Book',
            'source': ''
        }

        url = 'https://www.yuque.com/api/books'
        res = req.post(url, headers=self.base_header(), data=json.dumps(params))
        # print(res.text)
        book_id = res.json()['data']['id']
        if book_id is None:
            print('创建知识库失败：' + res.text)

        return book_id

    def create_top_dir(self, book_id, title):
        """创建一级目录"""
        params = {
            'book_id': book_id,
            'format': 'list',
            'action': 'insert',
            'title': title
        }

        url = 'https://www.yuque.com/api/catalog_nodes'
        res = req.put(url, headers=self.base_header(), data=json.dumps(params))
        # print(res.text)
        node_uuid = res.json()['meta']['node_uuid']
        if node_uuid is None:
            print('创建一级目录失败：' + res.text)
        return node_uuid

    def create_sub_dir(self, book_id, target_uuid, title):
        """创建子级目录"""
        # 第1步，创建目录
        params = {
            'book_id': book_id,
            'format': 'list',
            'target_uuid': target_uuid,
            'action': 'insert',
            'type': 'TITLE'
        }

        url = 'https://www.yuque.com/api/catalog_nodes'
        res = req.put(url, headers=self.base_header(), data=json.dumps(params))
        # print(res.text)
        node_uuid = res.json()['meta']['node_uuid']

        # 第2步：更新目录标题
        params = {
            'book_id': book_id,
            'format': 'list',
            'node_uuid': node_uuid,
            'action': 'edit',
            'title': title
        }

        url = 'https://www.yuque.com/api/catalog_nodes'
        res = req.put(url, headers=self.base_header(), data=json.dumps(params))
        # print(res.text)
        data_list = res.json()['data']
        length = len(data_list)
        if data_list is None or length == 0:
            print('创建子目录失败:' + res.text)
            return None
        return res.json()['meta']['node_uuid']

    def import_top_doc(self, book_id, file_url):
        """直接在知识库下导入文档"""
        params = {
            'insert_to_catalog': 'true',
            'action': 'prependChild',
            'book_id': book_id,
            'type': 'markdown',
            'import_type': 'create',
            'options': '{"enableLatex":1,"isGBK":"false"}',
            'filename': 'file'
        }

        url = 'https://www.yuque.com/api/import'

        headers = self.base_header()
        headers.pop('content-type')

        with open(file_url, 'rb') as f:
            files = {'file': f}
            res = req.post(url, headers=headers, data=params, files=files)
            try:
                doc_id = res.json()['data']['id']
                if doc_id is None:
                    print('导入文档失败：' + res.text)
            except Exception as e:
                print('导入文档失败：' + res.text)
            return doc_id

    def import_dir_doc(self, book_id, file_url, node_uuid, title):
        """在目录下导入文档"""
        params = {
            'toc_node_uuid': node_uuid,
            'toc_node_title': title,
            'insert_to_catalog': 'true',
            'action': 'prependChild',
            'target_uuid': node_uuid,
            'book_id': book_id,
            'type': 'markdown',
            'import_type': 'create',
            'options': '{"enableLatex":1,"isGBK":"false"}',
            'filename': 'file'
        }

        url = 'https://www.yuque.com/api/import'

        headers = self.base_header()
        headers.pop('content-type')

        with open(file_url, 'rb') as f:
            files = {'file': f}
            res = req.post(url, headers=headers, data=params, files=files)
            try:
                doc_id = res.json()['data']['id']
                if doc_id is None:
                    print('导入文档失败：' + res.text)
            except Exception as e:
                print('导入文档失败：' + res.text)
            return doc_id


request = Request()
