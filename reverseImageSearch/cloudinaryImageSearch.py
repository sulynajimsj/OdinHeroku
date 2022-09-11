from serpapi import GoogleSearch
import json
import webbrowser
import os
import cloudinary
import cloudinary.uploader
from Transcripts import ytranscripts
from Transcripts import TextCompare
def searchAPI(image_url):

    #Reverse Image search: Google only
    params = {
    "api_key": "50cfe7c0b41e0651f3b69227fa667c7af236e6c3104c2acb000b787786ce53d1",
    "engine": "google_reverse_image",
    "google_domain": "google.com",
    "q": "",
    "image_url": image_url,
    "tbm": "shop"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # Using a JSON string
    with open('result.json', 'w') as fp:
        json.dump(results, fp, indent=4)
    print("The results")
    
    theResults = results["image_results"]
    resultLink = results["search_metadata"]["google_reverse_image_url"]
    

    thetitles = []
    for i in range(0, len(theResults)):
        title = theResults[i]['title']
        print(title + '\n')
        thetitles.append(title)

    # The title[3] is because second last usually at this point is the most relevant results
    
    if (len(thetitles)>=3):
        query = thetitles[2]
    else:
        try:
            query = thetitles[1]
        except:
            query = thetitles[0]
            
    params2 = {
        "engine": "youtube",
         "search_query": query,
         "api_key": "50cfe7c0b41e0651f3b69227fa667c7af236e6c3104c2acb000b787786ce53d1"
    }

    search2 = GoogleSearch(params2)
    results2 = search2.get_dict()
    with open('resultYoutube.json', 'w') as fp:
        json.dump(results2, fp, indent=4)
    print("The results")
    aLink = results2['search_metadata']['youtube_url']
    


    #Get speechtotext

    #Get all transcripts
    ytVideos = results2['video_results']

    for video in ytVideos:
        print(video['link'])
        try:
            ytranscripts.getYoutubeTranscript(video['link'])
            
        except:
            with open('op.txt', 'w') as opf:
                opf.write("ERROR Error aEr")
            print("Transcript ERROR")
        
        
        # Compare the videos 
        theVideoLink = video['link']
        textComp = TextCompare.textCompare(r"transcript.txt", r"op.txt")

        isMatch = textComp.compare()
        if (isMatch):
            print('MATCH FOUND')
           
            
            return video
    return "nomatch"
            
            
            





        

            
        


def list_file_name(path):
    fileList = os.listdir(path)
    return(fileList)

def inputImages(path):
    allFiles = list_file_name(path)
    allurls = []
    for name in allFiles:
        upload = cloudinary.uploader.upload("frames/"+name)
        url = upload['url']
        searchResult = searchAPI(url)
        if (searchResult != "nomatch"):
            return searchResult
    return "nofound"