# webcrawler

Este projeto foi desenvolvido com o objetivo de demonstrar a minha estrutura para um projeto. Utilizei a lista de tags HTML que poderiam conter uma URL para realizas o filtro dos links a serem percorridos.

## Detalhes

[Python](https://www.python.org/) - Linguagem de Programação

[Scrapy](https://scrapy.org/) - Framework para extração de dados de web sites

[Elementary OS](https://elementary.io/) - Sistema operacional utilizado para desenvolvimento

## Estratégia para desenvolvimento

Abaixo encontra-se o passo-a-passo utilizado durante o desenvolvimento:

1. Definição da linguagem de programação: Decidi utilizar python por ser uma linguagem que permite a criação de projetos de forma rápida, sem que muita configuração seja feita, e também pela facilidade de utilização de bibliotecas;
2. Pesquisa sobre biblioteca para crawler: Como dito na descrição do desafio, busquei tecnologias atuais para o desenvolvimento, sem que fosse necessário "reinventar a roda". Dessa forma, busquei bibliotecas que auxiliassem no desenvolvimento em python, e encontrei muitas referências a Scrapy;
3. Implementação de uma prova de conceito inicial: A partir da documentação da biblioteca, iniciei um processo para implementar uma prova de conceito que me daria o conhecimento sobre a linguagem necessário para o desenvolvimento;
4. Primeira prova de conceito concluída: Após ter concluído uma primeira prova de conceito, a partir do caso de uso mais básico (extração de links de uma dada página), passei a incrementar o mesmo projeto, para atingir o objetivo final;
5. Refinamento do resultado final: A partir do momento em que obtive um resultado satisfatório, passei a refinar a execução do programa, tentando extrair o máximo dos crawlers, de forma que a verificação do resultado final fosse facilitada;
6. Documentação: Comentários adicionados ao código, juntamente com a criação do README.md.

## Execução

### Linux
1. Instale Python 2.7+
3. Instale o pip
4. Instale o Scrapy
5. Vá até a pasta do projeto e execute 

```
scrapy crawl webcrawler
```

6. Após a execução, um arquivo chamado sitemap.txt será criado na pasta do projeto.

OBS: Para melhor visualização da execução, mantive o nível de log em DEBUG. Caso seja necessário modificá-lo, adicionar a linha LOG_LEVEL='INFO' no arquivo settings.py .

## Pontos adicionais
* Melhor Categorização das páginas: No estado atual, o sistema percorre as páginas e as adiciona a um dicionário. Durante esse processo, também é criada a árvore que representa a estrutura do site. O tipo de cada página (html, pdf, ...), é definido em um estado futuro, no momento em que dada página é também percorrida. Visto que somente é utilizado o valor presente no header 'Content-Type' para que este tipo seja definido, acredito que seria interessante uma real categorização entre elementos estáticos e páginas html, de forma que possibilitaria uma estruturação de site map mais limpa e clara.

* Melhoria do sitemap gerado: A aplicação gera um arquivo com uma estrutura hierarquica de URLs, onde cada novo nível representa o caminho percorrido até determinada URL. Porém, a visualização dos elementos não é simples, tendo o usuário que prestar muita atenção para encontrar a URL procurada. Idealmente, em uma versão futura, eu modificaria o programa para que somente listasse os níveis diferentes que estão sendo percorridos
```
sicredi.com.br
|html
||para-voce
|||credito
||||carta-fianca
||||imagem.png
```

Da forma como o programa foi desenvolvido, onde estamos reaproveitando o processo de extração para criar a árvore, assim como fazer o carregamento da próxima página, tomaria um pouco mais de tempo para fazer a quebra da URL nesses níveis (e achei que seria melhor focar na funcionalidade nesse momento).

* Geração de um sitemap em HTML: Como temos páginas que se repetem, optei por utilizar '\*\*' para indicar uma página que já havia sido visitada porém, novamente, essa estratégia não permite que o usuário tenha uma ideia clara da execução de forma simples. Ao invés, eu optaria pela geração de um HTML, com anchors que nos levassem para o passo onde a página foi visitada pela primeira vez, facilitando a interação do usuário com a mesma. Isso também poderia ser utilizado para demonstrar páginas que, apesar de presentes nas páginas, não estão funcionando, ao incluir uma cor determinada para essas.

* Revisão dos links: Para garantir que todos os links estão sendo visitados, desenvolveria um método que, dado a lista final de links, geraria um documento que deixasse destacados àqueles que foram encontrados durante o processo de crawling, facilitando a identificação de links que, por algum motivo, não foram cobertos.

* Exposição da aplicação na nuvem: Da forma como desenvolvida, a aplicação utiliza URLs iniciais que não são dinamicamente definidas. Criaria uma página simples que, ao receber uma URL, juntamente com os domínios permitidos, retornaria uma página HTML para o usuário (não sendo então necessária a configuração local para execução).

* Utilização de threads: Para que o tempo de espera do usuário seja diminuído, distribuiria o processamento em threads (possivelmente baseado no número de páginas encontradas em cada passo do crawler). Visto que estamos utilizando um dicionário para manter os dados, esse seria compartilhado entre as threads.

* Diferentes formatos de sitemap: Inclusão de diferentes formatos de sitemap gerados (JSON, HTML, XML,...).

* Pesquisa sobre outras estratégias para extração de dados: Pesquisaria sobre outras formas de listar o que precisa ser extraído da página. Atualmente, utilizo um XPath genérico para definir de que atributos extrair as URLs, porém fico curioso sobre a performance do mesmo, dado que, por ser genérico, o programa precisa percorrer todos os níveis da página em busca dos atributos solicitados.

* Scrapy Allowed Domains: Do modo como é descrito, o atributo de cada Spider chamado Allowed_Domains, deveria fazer o filtro dos domains que seriam percorridos automaticamente (impossibilitando a execução de uma chamada da classe Request). Porém, durante a execução, ele não estava atendendo essa necessidade, apesar de todas as necessidades listadas na documentação terem sido atendidas. Pesquisaria melhor o motivo pelo qual esse filtro não funcionou, e evitaria fazer esse controle manualmente.

* Melhor definição do que uma URL deve ser: Nesse momento estamos considerando que somente URLs com / devem ser consideradas. Apesar de fazer sentido, do ponto de vista da estrutura de uma URL, o código fica muito engessado. Pesquisaria melhor formas de fazer o mesmo.
