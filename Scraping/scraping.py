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


#url = 'https://steamcommunity.com/discussions/forum/27/3877095833478995953/'

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
def getPageSource(url, maxscroll = 1):
    navegador.get(url)

    sleep(5)
    for i in range(0, maxscroll):
            
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(10)

    
    html_content = navegador.page_source
    
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup
    
def acessAndGetLinksInPerfil(url):
    
    soup = getPageSource(url, 1)

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

    soup = getPageSource(url, 1)
    
    html_content = navegador.page_source
    
    soup = BeautifulSoup(html_content, 'html.parser')

    #Get userurl
    
    #Get userimage
    
    imageAndPerfil = soup.find('div', class_=re.compile(r'forum_op_avatar playerAvatar.*'))

    if imageAndPerfil:
        a_tag = imageAndPerfil.find('a')

        if a_tag:
            urlPerfilOwnerTopic = a_tag['href']
        else:
            print("Tag 'a' não encontrada na div.")
    else:
        print("Div com a classe especificada não encontrada.")
    
    imageAutor = imageAndPerfil.find('img')
    imageAutorOwnerTopic = imageAutor['src']

    #Get username
    
    userNameOwnerTopic = soup.find('a', class_='hoverunderline forum_op_author')

    #Get title of Topic
    topic = soup.find('div', class_='topic')

    #Get text init of topic
    subjectTopic = navegador.find_element(By.XPATH, xpath)
    
    element_html = subjectTopic.get_attribute("outerHTML")

    textInitialTopic = BeautifulSoup(element_html, 'html.parser')
    
    #Get date
    dateCreate = soup.find('span', class_='date')

    #Get reposts
    
    repostsTopic = soup.find_all('div', class_='commentthread_comment responsive_body_text')

    commentary = {}
    
    info = {}
    
    info['url'] = url
    
    if userNameOwnerTopic:
        
        userNameOwnerTopic = userNameOwnerTopic.text
        info['userNameOwnerTopic'] = userNameOwnerTopic
    else:
        info['userNameOwnerTopic'] = 'false'
    
    if urlPerfilOwnerTopic:
        info['urlPerfilOwnerTopic'] = urlPerfilOwnerTopic
    else:
        info['urlPerfilOwnerTopic'] = 'false'
    
    if imageAutorOwnerTopic:
        info['imageAutorOwnerTopic'] = imageAutorOwnerTopic
    else:
        info['imageAutorOwnerTopic'] = 'false'
        
    if topic:
        topic = topic.text
        info['initialPost'] = topic 
    else:
        info['initialPost'] = 'false' 

    if textInitialTopic:
        textPost = textInitialTopic.get_text()
        info['subject'] = textPost 
    else:
        info['subject'] = 'false' 

    if dateCreate:
    # Acesse o atributo "title" para obter o texto desejado
        dateCreate = dateCreate['title']
        info['dateCreate'] = dateCreate 
    else:
        info['dateCreate'] = 'false' 
    
    info['commentary'] = []
    
    vector = []
    for response in repostsTopic:
        
        autorResponse = response.find('a', class_='hoverunderline commentthread_author_link')
        
        autorResponseLinkAndImage = response.find('div', class_=re.compile(r'commentthread_comment_avatar playerAvatar.*'))
        
        if autorResponseLinkAndImage:
            a_tag = autorResponseLinkAndImage.find('a')

            if a_tag:
                autorResponseUrl = a_tag['href']
    
        autorResponseImage = autorResponseLinkAndImage.find('img')
        autorResponseImage = autorResponseImage['src']

        autorResponseDateCreate = response.find('span', class_='commentthread_comment_timestamp')
        
        autorResponseText = response.find('div', class_='commentthread_comment_text')

        if autorResponse:
            autorResponse = autorResponse.text
            commentary['autorResponse'] = autorResponse
        else:
            commentary['autorResponse'] = 'false'
        
        if autorResponseImage:
            commentary['autorResponseImage'] = autorResponseImage
        else:
            commentary['autorResponseImage'] = 'false'
        
        if autorResponseUrl:
            commentary['autorResponseUrl'] = autorResponseUrl
        else:
            commentary['autorResponseUrl'] = 'false'
            
        if autorResponseDateCreate:
            autorResponseDateCreate = autorResponseDateCreate['title']
            commentary['autorResponseDateCreate'] = autorResponseDateCreate
        else:
            commentary['autorResponseDateCreate'] = 'false'
        
        if autorResponseText:
            autorResponseText = autorResponseText.text
            commentary['autorResponseText'] = autorResponseText
        else:
            commentary['autorResponseText'] = 'false'
        
        
        info['commentary'].append(commentary.copy())
        
    jsonImport(info)    
 
def main():
    
    getInitialInf = 1
    
    url = 'https://steamcommunity.com/discussions/forum/27/?fp={getInitialInf}'
    
    match = re.search(r'/forum/(\d+)/', url)

    if match:
        numberForum = match.group(1)
    
    xpathNumber = f'//*[@id="forum_General_4009259_{numberForum}_pagelinks"]/a[7]'
    
    soup = getPageSource(f'https://steamcommunity.com/discussions/forum/27/?fp={getInitialInf}', 1)

    numberMax = navegador.find_element(By.XPATH, xpathNumber)
    
    numberMax = numberMax.get_attribute("outerHTML")

    numberMax = BeautifulSoup(numberMax, 'html.parser')

    if numberMax:
        numberMax = int(numberMax.text)

    print("1 Step: ")
    
    for indice in range(1, numberMax+1):
        url = f'https://steamcommunity.com/discussions/forum/27/?fp={indice}'
        
        sleep(5)
        
        acessAndGetLinksInPerfil(url)
    
    print("2 Step: ")
    
    for link in unique_links_post:
        getData(link)

main()
