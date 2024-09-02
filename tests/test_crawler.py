import unittest
from unittest.mock import patch, MagicMock
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from server import Crawler, handle_crawl

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()

    @patch('aiohttp.ClientSession.get')
    async def test_crawl_single_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text.return_value = '<html><body><a href="/page1">Link 1</a></body></html>'
        mock_get.return_value.__aenter__.return_value = mock_response

        sitemap = await self.crawler.crawl('http://example.com')
        self.assertIn('example.com', sitemap)
        self.assertIn('- /', sitemap)
        self.assertIn('- /page1', sitemap)

    @patch('aiohttp.ClientSession.get')
    async def test_crawl_multiple_pages(self, mock_get):
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            mock_response.status = 200
            if url == 'http://example.com':
                mock_response.text.return_value = '<html><body><a href="/page1">Link 1</a><a href="/page2">Link 2</a></body></html>'
            elif url == 'http://example.com/page1':
                mock_response.text.return_value = '<html><body><a href="/page3">Link 3</a></body></html>'
            else:
                mock_response.text.return_value = '<html><body></body></html>'
            return mock_response

        mock_get.side_effect = lambda url, **kwargs: MagicMock(__aenter__=MagicMock(return_value=side_effect(url)))

        sitemap = await self.crawler.crawl('http://example.com')
        self.assertIn('example.com', sitemap)
        self.assertIn('- /', sitemap)
        self.assertIn('- /page1', sitemap)
        self.assertIn('- /page2', sitemap)
        self.assertIn('- /page3', sitemap)

class TestHandleCrawl(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.router.add_get('/crawl', handle_crawl)
        return app

    @unittest_run_loop
    @patch('server.Crawler.crawl')
    async def test_handle_crawl(self, mock_crawl):
        mock_crawl.return_value = "example.com\n- /\n  - /page1\n  - /page2"
        resp = await self.client.get('/crawl?url=http://example.com')
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertIn('example.com', text)
        self.assertIn('- /', text)
        self.assertIn('- /page1', text)
        self.assertIn('- /page2', text)

if __name__ == '__main__':
    unittest.main()