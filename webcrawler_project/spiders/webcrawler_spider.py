import scrapy
from scrapy import signals
import sys
from scrapy import Spider
from ..helpers import printer

class WebcrawlerSpider(scrapy.Spider):

    #Nome do crawler a ser executado
    name = "webcrawler"

    #Lista de dominios que podem ser percorridos
    allowed_domains=['www.sicredi.com.br']

    #Estrutura em arvore que mantera a relacao entre os links
    tree = {}

    #Referencia para o primeiro nodo da arvore
    root = None

    def start_requests(self):
        
        #Lista de URLs que iniciarao o processo
        urls = [
           'https://www.sicredi.com.br/'
        ]

        #Chamada feita para cada URL, iniciando o processo de busca
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    #Esse metodo cria um listener para eventos da spider. Nesse caso, espera por um sinal de closed ( que indica a finalizacao da execucao).
    #Ao receber o sinal, chama o metodo spider_closed .
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(WebcrawlerSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    #Solicita a criacao do arquivo 
    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)

        if self.root is not None:
            printer.save_tree(self.root)
        
        

    #Metodo chamado para cada pagina percorrida com sucesso (processa o retorno do carregamento da pagina)     
    def parse(self, response):
        try:
            #Verifica se a pagina perrcorrida continha conteudo text/html
            if 'text/html' in response.headers['Content-Type']:
                #Lista de tags e atributos a serem considerados para filtro. Concatena as listas retornadas
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
                
                #Percorre a lista de URLs retornadas e as extrai
                for selector in selectors:
                    url = selector.extract()

                    #Verifica se a URL tem um '/', evitando que chamadas javascripts, ou possivelmente outros valores, sejam considerados
                    if '/' in url:
                        #Insere o nodo e verifica se o dominio na URL faz parte dos permitidos
                        if self.insert_node(response, url) and self.check_allowed_domains(url):
                            yield scrapy.Request(url, callback=self.parse)
            #Atualiza o tipo da pagina com o que foi retornado na resposta do crawler
            self.update_type(response)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    #Percorre a lsita de allowed_domains para verificar se a url passa por parametro se encaixa
    def check_allowed_domains(self, url):
        for domain in self.allowed_domains:
            if domain in url:
                return True
        return False

    #Insere o nodo na arvore que representa a relacao entre as URLs
    def insert_node(self, response, url_child):

        #Defini se o nodo filho deve ser percorrido. False indica que nao foi encontrado na arvore e, por este motivo, deve ser percorrido
        result = False
    
        try:
            #Extrai a URL da pagina pai
            url_parent = response.url

            #Procura na arvore pelo nodo pai
            parent_node = self.tree.get(url_parent)
            #Procura pelo nodo filho na arvore
            child_node = self.tree.get(url_child)

            #Caso o pai nao exista, um novo nodo e criado e colocado na arvore
            if parent_node is None:
                parent_node = Tree()
                parent_node.data = url_parent
                self.tree[url_parent] = parent_node

            #Caso o filho nao exista, um novo nodo e criado e colocado na arvore
            if child_node is None:
                child_node = Tree()
                child_node.data = url_child
                self.tree[url_child] = child_node
                result = True

            #Estabelece a relacao hierarquica entre o nodo e pai
            parent_node.children.append(child_node)

            #Caso a referencia para o primeiro nodo da arvore nao tenha sido preenchida
            if self.root is None:
                self.root = parent_node
            return result
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    #Baseado no conteudo do response, popula o type do nodo
    def update_type(self,response):

        node = self.tree.get(response.url)
        if node is not None:
            node.type = response.headers['Content-Type']
       

#Definicao da estrutura de arvore
class Tree(object):
    def __init__(self):
        self.children = []
        self.data = None
        self.type = 'Static'
        self.checked = False
