import os
import requests

baseURL = 'https://giantessworld.net'

print("Hello Macrophiles!")
print()
print("Each story has a unique ID number. This program just goes through each number and downloads the HTML file (except ID numbers of stories that were deleted).")
print("You can find a story's ID number at the end of  the URL when you're viewing that story. Example: https://giantessworld.net/viewstory.php?sid=10618")
print('To archive just that story, enter "10618" as the starting ID when prompted. The program will automatically download every chapter.')
print("If new chapters are added in the future, running the program again will only download the new chapters.")
print("To archive all stories, you need to find the ID number of the most recent published story.")
print("When browsing the site by 'most recent', look for the first result with only a single chapter. Old stories with new chapters uploaded do not have a newer ID.")
print("Then you can enter 0 as the starting ID, and the ID from the most recent story as the ending ID. ")
print("The program will make a new folder 'GTSWorld' where you are running this program. Each story will make a new folder in that. This has only been tested on Windows 10.")
print("If the program crashes before making it to the ending ID, you can start it again at the last ID that was checked.")
print("Feel free to reach out to u/storiesOfAllSizes on Reddit with any questions. I'd like to work on backing up more sites in the future.")
print()
startingID = int(input("Which story ID do you want to start at? "))
endingID = int(input("Which story ID do you want to end at? "))
#namingScheme = input("Do you want to title the stories with numbers or the title first? To sort by IDs or A-Z")

try:
    os.mkdir(f'GTSWorld')
except:
    print("Folder GTSWorld already present.")

storyID = startingID
while storyID <= endingID:
    print("Checking story ", storyID)
    
    page  = requests.get(f'{baseURL}/viewstory.php?sid={storyID}')

    print(page)

    if "This story has not been validated" in str(page.content): #checking if that story ID has a published story. the html page length with no story is 9401, a story will have more than that
        print(f'Story {storyID} does not exist.')

    else:
        try:
            os.mkdir(f'GTSWorld/Story_{storyID}')
        except:
            print(f"Folder Story_{storyID} already present")

        try:
            path = r'' #initiate the variable as a raw string, then it'll stay as a raw string even when set again
            path = f'./GTSWorld/Story_{storyID}/Story_{storyID}.html' 
            file = open(path, 'x') #open/create a new file at that path
            file.write(str(page.content)) #add the html content to the file - idk if this overwrites or appends
            file.close()

        except:
            print(f"Story_{storyID} is already downloaded.")

        if 'class="next">Next</a>' in str(page.content):
            isThereAnotherChapter = True
        else:
            isThereAnotherChapter = False

        pageNumber = 2
        while isThereAnotherChapter == True:
            page = requests.get(f'{baseURL}/viewstory.php?sid={storyID}&chapter={pageNumber}')

            print(f'Story {storyID} checking for chapter {pageNumber}')

            print(page)

            try:
                #idk if path will still be a raw string or if i need to init that again but we'll see
                path = f'./GTSWorld/Story_{storyID}/Story_{storyID}_chapter_{pageNumber}.html'
                file = open(path, 'x')
                file.write(str(page.content))
                file.close()
                
            except:
                print(f"Story_{storyID}_chapter_{pageNumber} has already been downloaded.")

            if 'class="next">Next</a>' in str(page.content):
                isThereAnotherChapter = True
            else:
                isThereAnotherChapter = False

            pageNumber = pageNumber + 1
        
    storyID = storyID + 1


