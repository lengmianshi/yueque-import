import unittest
from yu_que_request import request as req


class MyTestCase(unittest.TestCase):

    def test_repos_list(self):
        req.repos_list()

    def test_create_repos(self):
        node_uuid = req.create_repos(name="01")
        print(node_uuid)

    def test_create_top_dir(self):
        node_uuid = req.create_top_dir(title="01", book_id='28317312')
        print(node_uuid)

    def test_create_sub_dir(self):
        node_uuid = req.create_sub_dir(title="001", book_id='28317312', target_uuid='fg_zOMU9icfh6LiB')
        print(node_uuid)

    def test_create_top_doc(self):
        req.import_top_doc(book_id=28317312, file_url='C:\\Users\\mayn\\Desktop\\youdao\\欢迎来到全新的有道云笔记.md')

    def test_create_dir_doc(self):
        req.import_dir_doc(book_id=28317312, file_url='C:\\Users\\mayn\\Desktop\\youdao\\欢迎来到全新的有道云笔记.md',
                           node_uuid='fg_zOMU9icfh6LiB', title='01')


if __name__ == '__main__':
    unittest.main()
