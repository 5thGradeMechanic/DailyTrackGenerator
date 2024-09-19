import requests, json, os

#Create the Variables
newsKey = os.environ['newsapi']
country = "us"
url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={newsKey}"

result = requests.get(url)
data = result.json()
# print(json.dumps(data, indent=2))

#Make the GET request, send it to the URL, and format/print the response
result = requests.get(url)
data = result.json() #Saves the API response data in JSON format to a variable
#print(json.dumps(data, indent=2)) #prints the JSON response

#Print the returned data
for article in data['articles']: #iterate through the articles (key) in the API response
  print(article['title'])
  print(article['url'])
  print(article['content'])
  print()