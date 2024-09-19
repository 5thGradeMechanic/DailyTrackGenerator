#Import Libraries
import requests, json, os
import openai
from requests.auth import HTTPBasicAuth

#Import the Secrets
newsKey = os.environ['newsapi']
openai.organization = os.environ['organizationID']
openai.api_key = os.environ['openai']
clientID = os.environ['CLIENT_ID']  #spotify
clientSecret = os.environ['CLIENT_SECRET']  #spotify


#Pull in 5 most recent local stories
def getStories():
  country = "us"
  url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={newsKey}"

  #---------- Get Today's News Stories ----------
  stories = requests.get(url)
  data = stories.json(
  )  #Saves the API response data in JSON format to a variable

  for article in data[
      'articles'][:
                  5]:  #iterate through the first 5 articles (key) in the API response
    title = article['title']
    newsURL = article['url']
    content = article['content']

    #print(f"Title: {title}\nURL: {newsURL}\nContent: {content}\n") #for testing

  return data


#Summarize each story in 2-3 words
def summarizeStories(article):
  '''
  Sends a request to OpenAI to summarize the given article URL.
  Returns the summary text or an indication that no summary could be found.
  '''
  # Initialize an empty list to accumulate choice objects
  choices = []

  counter = 0

  #Extract the 5 articles (keys) in the API response
  for article in stories['articles'][:5]:
    counter += 1
    newsURL = article['url']
    newsTitle = article['title']

    #Make the OpenAI API call
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "Please summarize the following link in 2 or 3 words:"
        },  #Prompt
        {
          "role": "user",
          "content": newsURL
        }
      ])
    #Extract the choice object from the response
    #choice = response.choices[0]

    #Extract the content from the response and append to summaries list. 
    content = response.choices[0].message.content.strip()
    #choices.append(content)
    choices.append(content)


    #Append the choice object to the choices list
    #choices.append(choice)
    '''
    #Assign the Variables 
    message_content = choice.message.content
    finish_reason = choice.finish_reason
    model_used = response.model
    total_tokens = response.usage.total_tokens

    #Print out the Summary 
    formatted_output = f"""
    Article {counter}:
    Title: {newsTitle}
    URL: {newsURL}
    Summary: {message_content}"""

    openAIMetadata = f"""
    Finish Reason: {finish_reason}
    Model Used: {model_used}
    Total Tokens Used: {total_tokens}"""

    print(formatted_output)
    #print(openAIMetadata)
    print("---")
    if counter >= 5:
      break
    '''

  return choices


#Print function for Testing purposes <-- Not needed anymore
def printStories(data, choices):
  '''Iterate through the articles (key) in the API response and print them along with their summaries'''
  print("Here are your 5 Daily Article Summaries: ")

  # Loop through the articles with their index
  '''#idx is short for index; enumerate keeps count of iterations and accesses the article, allowing you to retrieve the articles title, URL, content, etc.'''
  for idx, article in enumerate(data['articles'][:5]):
    counter = idx + 1  # Adjusted to start from 1 for display purposes
    title = article['title']
    newsURL = article['url']
    content = article['content']

    # Check if the index is within the bounds of the choices list
    if idx < len(choices):
      summary = choices[idx]  # Directly access the corresponding summary
    
    else:
      summary = 'Summary unavailable'

    formatted_output = f"""
    Article {counter}:
    Title: {title}
    URL: {newsURL}
    Summary: {summary}
    """
    print(formatted_output)


#Pass Words above to Spotify, and show a sample of each song.
def getSongs(summaries):
  #Bring in the secrets and assign them to variables
  clientID = os.environ['CLIENT_ID']
  clientSecret = os.environ['CLIENT_SECRET']
  
  #Get the article summaries to pass to Spotify
  stories = getStories()  #Assigns the 5 most recent stories (Title, URL, Content) to a variable
  summary = summarizeStories(stories)
  #testText = "Trump indictment"
  #print("Summary is here:", summary) #for testing

  #Test the Authentication
  try:
    #Setup Variables to store auth details.
    url = "https://accounts.spotify.com/api/token"  #stores the web address to connect to (that sends back the token)
    data = {
      "grant_type": "client_credentials"
    }  #creates a dictionary that communicates with the API in the correct way. It basically says to Spotify 'Send me back the credentials based in my client ID and secret. Here's a dictionary format to put them in'.
    auth = HTTPBasicAuth(
      clientID, clientSecret
    )  #uses the new HTTPBasicAuth function to send your client ID and secret to Spotify as pretty much the username and password to log you in.
    response = requests.post(
      url, data=data, auth=auth
    )  #stores the API key that will be returned by the requests function that sends Spotify the login info needed. "Talk to the URL, tell it you want your API key, and use this username/password combo"
    accessToken = response.json()["access_token"]
    #print("Success: Obtained Spotify Access Token")

  except Exception as e:
    print("Error obtaining Spotify access token:", e)
    return

  #For each summary, search on Spotify
  for summary in summaries:
    search_query = requests.utils.quote(summary)  # Ensure this is dynamic and changes with each summary.
    try:
      #Construct the Search URL
      url = "https://api.spotify.com/v1/search" 
      headers = {'Authorization': f'Bearer {accessToken}'} #enable comms with the API by adding the access token to the headers. Bearer token is a common scheme for OAuth2.0
      search = f"?q={search_query}&type=track&limit=1" #stores the search query that will be used to search for tracks
      fullURL = f"{url}{search}" #Create a full query

      #Debugging Steps
      #print(f"Searching for: {summary}")  # Debug: What summary are we searching for?
      #print(f"Query URL: {search_url}")  # Debug: What is the query URL?
  
      #Send off the search request, capture the API response, parse it to JSON.
      response = requests.get(fullURL, headers=headers)
      spotify_data = response.json()
      #print(json.dumps(spotify_data, indent=2))
  
      # Process the search results (optional: print here or process as needed)
      print(f"Results for '{summary}':")
      for track in spotify_data['tracks']['items']:
        print(f"Track Name: {track['name']} by {track['artists'][0]['name']}")
        print(f"URL: {track['external_urls']['spotify']}\n")

    except Exception as excpt:
      print(f"Error searching Spotify for '{summary}': {excpt}")
    
  songs = ""

  '''
  # Loop to prepare track listing - strip out the track names and print them
  for track in spotify_data["tracks"]["items"]:
    thisTrack = songs
    print(f"""{track['name']} by {track['artists'][0]['name']} 
    URL: {track['external_urls']['spotify']}""") #bring in the first artists of the lists name")
  '''
  

#Display the Output
stories = getStories()  #Assigns the 5 most recent stories (Title, URL, Content) to a variable
choices = summarizeStories(stories)

#Display the Output
print("OpenAI Response below:")
print("----------------------")
#printStories(stories, choices) #Prints the 5 most recent stories along with their summaries.


#print("Songs shown below:")
getSongs(choices)