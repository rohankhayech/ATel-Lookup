from bs4 import BeautifulSoup

"""
Gets the file content of a HTML

:param fileName: The name of HTML file
:return: HTML file content
"""
def getFileContent(fileName):
    return open(fileName, 'r').read()

"""
Gets the title of ATel from file content

:param fileContent: HTML file content
:return: Title of ATel
"""
def getTitle(fileContent):
    soup = BeautifulSoup(fileContent,'html.parser')
    return soup.find('h1', {'class': 'title'}).get_text()


"""
Outputs ATel title

:param atelNum: ATel number
:param title: Title of ATel number
"""
def outputTitle(atelNum, title):
    print ('Title for ATel #' + atelNum + ': ' + title)

# Main
outputTitle('14620', getTitle(getFileContent('atel14620.html')))
outputTitle('14621', getTitle(getFileContent('atel14621.html')))
outputTitle('14622', getTitle(getFileContent('atel14622.html')))
