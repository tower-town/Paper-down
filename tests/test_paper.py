from paper.paper import Paper
import unittest
import pytest

class TestPaper(unittest.TestCase):

    def setUp(self):
        self.paper = Paper()

    def test_check_languge(self):
        
        # title = "Modal acoustic transfer vector approach in a FEM-BEM vibro-acoustic analysis"
        # title = "Modal acoustic transfer vectoradc approach in acoustic analysis"
        title = "你好"
        # title = "模态声传递向量方法在FEM-BEM纵槽分析"
        with self.assertLogs('getPaper', level='INFO') as getPaper:
            self.paper.getPaper(title)
            warn = "WARNING:getPaper:[bold yellow]the word maybe isn't supported[/]"
            self.assertEqual(getPaper.output, [warn])

    def test_check_url(self):
        title = "Modal acoustic trasfer vectoradc appreach in aco ans"
        with self.assertLogs("getUrl",level="DEBUG") as getUrl:
            self.paper.getPaper(title)
            warn = "WARNING:getUrl:[bold red]download url is blank![/]"
            self.assertEqual(getUrl.output,[warn])
        