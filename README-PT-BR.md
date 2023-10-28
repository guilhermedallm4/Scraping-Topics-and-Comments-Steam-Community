# Scraping Commentary Forum Steam

## Descrição do Código
O código é um script em Python projetado para fazer o scraping de fóruns na plataforma Steam Community. Ele automatiza a extração de informações sobre tópicos e comentários em fóruns específicos e armazena esses dados em um formato JSON para posterior análise ou processamento.

## Bibliotecas Necessárias
Para executar o código, você precisa ter as seguintes bibliotecas Python instaladas:

- `selenium`: Usado para automação de navegação.
- `beautifulsoup4`: Utilizado para análise de páginas da web.
- `unicodedata`: Usado para lidar com caracteres Unicode.
- `json`: Essencial para trabalhar com dados em formato JSON.
- `re`: Essa biblioteca é utilizada para operações de expressões regulares, o que é útil para encontrar e extrair informações específicas de texto.
- `time`: A biblioteca time é usada para introduzir atrasos no script, permitindo que o navegador tenha tempo suficiente para carregar as páginas ou para sincronização durante a execução do script.

## Instalação

Antes de executar o projeto, certifique-se de ter instalado as bibliotecas necessárias. Você pode instalar as bibliotecas com o seguinte comando:

```bash
pip install selenium
pip install beautifulsoup4
pip install json
pip install unicodedata
pip install re
pip install time
```

## Estrutura do JSON

Os dados coletados são armazenados em arquivos JSON com a seguinte estrutura:
```json
{
    "url": "URL do tópico",
    "userNameOwnerTopic": "Nome do autor do tópico",
    "urlPerfilOwnerTopic": "URL do perfil do autor do tópico",
    "imageAutorOwnerTopic": "URL da imagem do autor do tópico",
    "initialPost": "Título do tópico",
    "subject": "Texto inicial do tópico",
    "dateCreate": "Data de criação do tópico",
    "commentary": [
        {
            "urlReponse": "URL do comentário",
            "autorResponse": "Nome do autor do comentário",
            "autorResponseUrl": "URL do perfil do autor do comentário",
            "autorResponseImage": "URL da imagem do autor do comentário",
            "autorResponseDateCreate": "Data de criação do comentário",
            "autorResponseText": "Texto do comentário"
        }
    ]
}
```

## Funcionamento do Código
O código inicia acessando um fórum do Steam Community e coleta os links para os tópicos. Em seguida, ele entra em cada tópico, coleta informações sobre o tópico e seus comentários e armazena esses dados em um arquivo JSON.

O código funciona em duas etapas:

1. Coleta os links dos tópicos no fórum.
2. Para cada link de tópico, coleta informações sobre o tópico e seus comentários.

# Como Usar
1. Instale as bibliotecas necessárias conforme descrito acima.
2. Configure o código para acessar o fórum Steam desejado, especificando a URL correta.
3. Execute o código.

Após a execução, os dados coletados serão armazenados em um arquivo JSON chamado "postAndCommentarySteam.json" para análise.
