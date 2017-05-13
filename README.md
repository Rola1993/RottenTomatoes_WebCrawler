# RottenTomatoes WebCrawler

## Project Abstract:
The program involves the text file processing, string manipulation and regular expression which the class IS452 has taught us. 
It lets the user input the name of some actor or actress, like ‘Ziyi Zhang’, and writes the the information of the highest and 
lowest rated movies of that actor/actress on Rotten Tomatoes into different txt files including the movie’s title, introduction, 
director, rating and genre. Then it generates a new txt file which contains the critic reviews and audience reviews of each movie. 
Finally, it creates an output txt file to analyze the word frequency in the movie reviews. The program could help to find 
if there is some pattern in the comments of a movie star’s best and worst works.

## Expected Deliverables:
1. Two txt files including the information of the highest and lowest rated movies of that actor.
2. Two txt files containing the reviews of the highest and lowest rated movies of that actor.
3. Two txt files analyzing the word frequency of the comments of the actor’s best and worst works.


## Steps:
1.	Get the actor/actress tag from the input and match it with the url like https://www.rottentomatoes.com/celebrity/zhang_ziyi. 
2.	Analyze the html structure and obtain the links of the best movies of that actor/actress. Go to each movie’s web page using the links and read it. Then open a new txt file to grab the movie information.
3.	Write the comments into an another txt file while looping each movie’s web page.
4.	Choose the appropriate method to analyze the word frequency of the movies’ comments. Generate a txt file to show the results.
5.	Do the same thing for the actor’s worst movies.
