# Scraping Topics and Comments from the Steam Community

## Code Description
The code is a Python script designed for scraping forums on the Steam Community platform. It automates the extraction of information about specific forum topics and comments and stores this data in JSON format for later analysis or processing.

## Bibliotecas Necessárias
To run the code, you need to have the following Python libraries installed:

- `selenium`: Used for web navigation automation.
- `beautifulsoup4`: Used for web page analysis.
- `unicodedata`: Used for handling Unicode characters.
- `json`: Essential for working with data in JSON format.
- `re`: This library is used for regular expression operations, which are useful for finding and extracting specific text information.
- `time`: The time library is used to introduce delays in the script, allowing the browser enough time to load pages or for synchronization during script execution.

## Installation

Before running the project, make sure you have installed the required libraries. You can install the libraries with the following command:

```bash
pip install selenium
pip install beautifulsoup4
pip install json
pip install unicodedata
pip install re
pip install time
```

## JSON Structure

The collected data is stored in JSON files with the following structure:
```json
{
    "url": "Topic URL",
    "userNameOwnerTopic": "Author's name of the topic",
    "urlPerfilOwnerTopic": "Profile URL of the topic's author",
    "imageAutorOwnerTopic": "URL of the topic's author image",
    "initialPost": "Topic title",
    "subject": "Initial text of the topic",
    "dateCreate": "Topic creation date",
    "commentary": [
        {
            "urlReponse": "Comment URL",
            "autorResponse": "Comment author's name",
            "autorResponseUrl": "Profile URL of the comment's author",
            "autorResponseImage": "URL of the comment's author image",
            "autorResponseDateCreate": "Comment creation date",
            "autorResponseText": "Comment text"
        }
    ]
}
```

## Code Operation
The code starts by accessing a Steam Community forum and collects links to forum topics. It then enters each topic, collects information about the topic and its comments, and stores this data in a JSON file.

The code operates in two steps:

1. Collects links to forum topics in the forum.
2. For each topic link, collects information about the topic and its comments.

## How to Use

1. Install the required libraries as described above.
2. Configure the code to access the desired Steam forum by specifying the correct URL.
3. Run the code.

After execution, the collected data will be stored in a JSON file named "postAndCommentarySteam.json" for analysis.
