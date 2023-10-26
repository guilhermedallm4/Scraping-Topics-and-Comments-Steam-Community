from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options
import json
import unicodedata

# mode headless
chrome_options = Options()
chrome_options.add_argument('--headless')

# Create a conjunt for unique URLS 
unique_links = set()
unique_links_post = set()

data = []

#Settings driver Chrome 
navegador = webdriver.Chrome(options=chrome_options)

#url = 'https://steamcommunity.com/discussions/forum/27/?fp=1'
url = 'https://steamcommunity.com/discussions/forum/27/3877095833478995953/'

def jsonImport(info):
    dados_existentes = []
    archive = 'postAndCommentarySteam.json'
    try:
        with open(archive, 'r', encoding="utf-8") as arquivo:
            dados_existentes = json.load(arquivo)
        dados_existentes.append(info)

    except FileNotFoundError:
        dados_existentes = [info]

    with open(archive, 'w', encoding="utf-8") as arquivo:
        json.dump(dados_existentes, arquivo, ensure_ascii=False)
        
    dados_existentes.clear()

def clean_text(text): 
    return ''.join(char for char in text if unicodedata.name(char).isascii())

# init = 0 start scraping with function getLinks, init = 1 other call of the function
def getPageSource(url, init = 0, maxscroll = 1):
    navegador.get(url)

    sleep(5)
    for i in range(0, maxscroll):
            
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(10)

    
    html_content = navegador.page_source
    
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
#    with open('htmlTopic.txt', 'w', encoding='utf-8') as arquivo:
#            arquivo.write(soup.prettify())
#    exit(0)
    return soup
    
def acessAndGetLinksInPerfil(url):
    
    soup = getPageSource(url, 1, 1)

    links = soup.find_all('a', class_='forum_topic_overlay')
    
    #pattern = re.compile(r'^/@.+/.+$')

    for link in links:
        href = link.get('href')
        if href is not None:
            unique_links_post.add(href)
                
    try:
        
        with open('linkofTopics.txt', 'w', encoding='utf-8') as arquivo:
            for link in unique_links_post:
                arquivo.write(link + '\n')
    except:
        print("Error save in file")
    
def getData(url):
    
    match = re.search(r'/(\d+)/?$', url)
    if match:
        idTopic = match.group(1)
    else:
        print("false")

    xpath = f'//*[@id="forum_op_{idTopic}"]/div[3]'

    soup = getPageSource(url, 1, 1)
    
    html_content = navegador.page_source
    
    soup = BeautifulSoup(html_content, 'html.parser')

    topic = soup.find('div', class_='topic')

    subjectTopic = navegador.find_element(By.XPATH, xpath)
    
    element_html = subjectTopic.get_attribute("outerHTML")

    textInitialTopic = BeautifulSoup(element_html, 'html.parser')
   
    dateCreate = soup.find('span', class_='date')

    info = {}
    
    info['url'] = url
    if topic:
        topic = topic.text
        info['topic'] = topic 
    else:
        info['initialPost'] = 'false' 

    if textInitialTopic:
        textPost = textInitialTopic.get_text()
        info['initialPost'] = textPost 
    else:
        info['initialPost'] = 'false' 

    if dateCreate:
    # Acesse o atributo "title" para obter o texto desejado
        dateCreate = dateCreate['title']
        info['dateCreate'] = dateCreate 
    else:
        info['dateCreate'] = 'false' 
    
    print(info)

    exit(0)
    #dateCreate = dateCreate['title']
    #print(dateCreate)
    #clap = soup.find('div', class_=re.compile(r'pw-multi-vote-count.*')) 
    
    #responses = soup.find('span', class_=re.compile(r'pw-responses-count.*'))
    
    #autorName = soup.find('a', {'data-testid': 'authorName'})
    
    #followers = soup.find('span', class_=re.compile(r'pw-follower-count.*'))
    
    #imageAutor = soup.find('img', {'data-testid': 'authorPhoto'})
    
    #timeForRead = soup.find('span', {'data-testid': 'storyReadTime' })
    
    #dateCreate = soup.find('span', {'data-testid': 'storyPublishDate'})
    
    #post = soup.find_all('p', class_=re.compile(r'pw-post-body-paragraph.*'))
    
    
    info['link'] = url
    if title:
        title = title.text
        title = clean_text(title)
        info['title'] = title 
       
    else:
        info['title'] = 'false' 
    
    if subtitle:
        subtitle = subtitle.text
        subtitle = clean_text(subtitle)
        info['subtitle'] = subtitle
       
    else:
        info['subtitle'] = 'false'
    
    if autorName:
        autorName = autorName.text
        autorName = clean_text(autorName)
        info['autorName'] = autorName
    
    else:
        info['autorName'] = 'false'
        
    if imageAutor:
        imageAutor = imageAutor['src']
        info['imageAutor'] = imageAutor
       
    else:
        info['imageAutor'] = 'false'
        
    if clap:
        clap = clap.text
        clap = clean_text(clap)
        info['clap'] = clap
        
    else:
        info['clap'] = 'false'

    if responses:
        responses = responses.text
        responses = clean_text(responses)
        info['response'] = responses
        
    else:
        info['response'] = 'false'
    
    if timeForRead:
        timeForRead = timeForRead.text
        timeForRead = clean_text(timeForRead)
        info['timeForRead'] = timeForRead
        
    else:
        info['timeForRead'] = 'false'
        
    if dateCreate:
        dateCreate = dateCreate.text
        dateCreate = clean_text(dateCreate)
        info['dateCreate'] = dateCreate
        
    else:
        info['dateCreate'] = 'false'
    
    if post:
        text_list = []

        for tag in post:
            stringAppend = clean_text(tag.text)
            
            text_list.append(stringAppend+'\n')

        info['text'] = text_list.copy()

        text_list.clear()
    else:
        info['text'] = 'false'
    
    
    jsonImport(info)
 
def main(url):
    print("1 Step: ")
    #sleep(5)
    #acessAndGetLinksInPerfil(url)
    #print("2 Step: ")
    #for acessPost in unique_links_post:
    getData(url)

main(url)
#getPageSource('https://steamcommunity.com/discussions/forum/27/3877095833478995953/')
