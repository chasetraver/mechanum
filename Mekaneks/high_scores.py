import array
hs_file = "highscores.txt"

#This function will read the high scores from "highscores.txt" using exceptions

#TODO need to display all lines from text file onto game window
def get_high_score():
    try:
        high_score_file = open("highscores.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("High score: ", high_score)
    except IOError:
        #File is empty
        print("There is not high score yet...")
    except ValueError:
        #There are contents within the file but no readable integers
        print("There are contents within the file but no readable high scores...")

    return high_score

#call this function with the filename passed in, returns an array with the 10 high scores
def read_scores(filename):
    with open(filename) as f:
        return [int(x) for x in f]


#This function will take in the new score once the game is over
#Calls read_scores which will have the high scores stored in an array
#Will sort the array in ascending order
#Checks to see if the new score is greater than the first (smallest) element in the array
#If bigger, than it will get replaced
#Will delete contents of text file and will be replaced with updated array
def save_high_score(new_high_score):
    hs_arr = read_scores(hs_file)
    hs_arr.sort()

    if new_high_score > hs_arr[0]:
        hs_arr.pop(0)
        hs_arr.append(new_high_score)
        hs_arr.sort()
        file = open(hs_file, "w")
        file.close()
        try:
            high_score_file = open(hs_file, "w")
            for element in hs_arr:
                high_score_file.write(element)
                high_score_file.write('/n')
            high_score_file.close()
        except IOError:
            #Can't write to file
            print("Unable to write to file...")






