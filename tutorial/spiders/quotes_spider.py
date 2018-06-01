import scrapy
from scrapy import signals
import sys
from scrapy import Spider

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains=['www.sicredi.com.br']
    tree = {}
    root = None

    def start_requests(self):
        
        urls = [
           'https://www.sicredi.com.br/html/para-voce'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)

        if self.root is not None:
            self.print_tree(self.root,'','')
        
        

    def print_tree(self,node,space,result):
       
        print  u''.join((space,node.data,'[',node.type,']')).encode('utf-8')
        space = space + ' '
        node.checked = True
        for child in node.children:
            if not child.checked:
                self.print_tree(child,space,'')
            else:
                print space+' '+ u''.join((space,node.data,'[',node.type,']')).encode('utf-8')

     
    def parse(self, response):
        try:
            if 'text/html' in response.headers['Content-Type']:
                selectors =  (response.selector.xpath('//a/@href')+
                                response.selector.xpath('//applet/@codebase')+
                                response.selector.xpath('//area/@href')+
                                response.selector.xpath('//base/@href')+
                                response.selector.xpath('//blockquote/@cite')+
                                response.selector.xpath('//body/@background')+
                                response.selector.xpath('//del/@cite')+
                                response.selector.xpath('//form/@action')+
                                response.selector.xpath('//frame/@longdesc')+
                                response.selector.xpath('//frame/@src')+
                                response.selector.xpath('//head/@profile')+
                                response.selector.xpath('//iframe/@longdesc')+
                                response.selector.xpath('//iframe/@src')+
                                response.selector.xpath('//img/@longdesc')+
                                response.selector.xpath('//img/@src')+
                                response.selector.xpath('//img/@usemap')+
                                response.selector.xpath('//input/@src')+
                                response.selector.xpath('//input/@usemap')+
                                response.selector.xpath('//ins/@cite')+
                                response.selector.xpath('//link/@href')+
                                response.selector.xpath('//object/@classid')+
                                response.selector.xpath('//object/@codebase')+
                                response.selector.xpath('//object/@data')+
                                response.selector.xpath('//object/@usemap')+
                                response.selector.xpath('//q/@cite')+
                                response.selector.xpath('//script/@src')+
                                response.selector.xpath('//audio/@src')+
                                response.selector.xpath('//button/@formaction')+
                                response.selector.xpath('//command/@icon')+
                                response.selector.xpath('//embed/@src')+
                                response.selector.xpath('//html/@manifest')+
                                response.selector.xpath('//input/@formaction')+
                                response.selector.xpath('//source/@src')+
                                response.selector.xpath('//track/@src')+
                                response.selector.xpath('//video/@poster')+
                                response.selector.xpath('//video/@src')+
                                response.selector.xpath('//source/@srcset')+
                                response.selector.xpath('//object/@archive')+
                                response.selector.xpath('//applet/@archive')+
                                response.selector.xpath('//image/@href')
                                )
                
                for selector in selectors:
                    url = selector.extract()

                    if 'javascript' not in url:
                        if self.insert_node(response, url) and self.allowed_domains[0] in url:
                            yield scrapy.Request(url, callback=self.parse)
            self.update_type(response)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    def insert_node(self, response, url_child):
        result = False
   
        try:
            url_parent = response.url

            parent_node = self.tree.get(url_parent)
            child_node = self.tree.get(url_child)

            if parent_node is None:
                parent_node = Tree()
                parent_node.data = url_parent
                parent_node.type = 'PAGE'
                self.tree[url_parent] = parent_node

            if child_node is None:
                child_node = Tree()
                child_node.data = url_child
                self.tree[url_child] = child_node
                result = True

            parent_node.children.append(child_node)

            if self.root is None:
                self.root = parent_node
            return result
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def update_type(self,response):

        node = self.tree.get(response.url)
        if node is not None:
            node.type = response.headers['Content-Type']
       

class Tree(object):
    def __init__(self):
        self.children = []
        self.data = None
        self.type = ''
        self.checked = False
