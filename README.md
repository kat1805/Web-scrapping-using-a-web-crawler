# Web-scrapping-using-a-web-crawler
A web server has been setup at http: // comp20008-jh. eng. unimelb. edu. au: 9889/ main/ containing a number of media reports on Rugby games. The project implements a web crawler to extract information from those reports and use that information to improve an understanding of team performance.

Rugby scores
Understanding the rugby scoring system is important in order to be able to extract scores
from match reports. A rubgy score is listed as x-y where x and y are the number of points
obtained by each team. For example, the following are all valid scores:
10-8
16-0
4-12


The following set of tasks are performed and stored in a single python file:

Task 1

1) Crawl the http: // comp20008-jh. eng. unimelb. edu. au: 9889/ main/ website to find a complete list of articles available.
Produce a csv file containing the URL and headline of each the articles your crawler has found.

Task 2

For each article found in Task 1,

a) Extract the name of the first team mentioned in the article.We will assume the article is written
about that team (and only that team).
b) Extract the largest match score identified in the article using regular
expressions. We will assume this score relates to the first named
team in the article.
Produce a csv file containing the URL, headline, first team mentioned and largest complete
match score of each the articles your crawler has found.
Note: Some articles may not contain a team name and/or a match score. These articles can
be discarded.

Task 3

For each article used in Task 2, identify the absolute value of the game difference. E.g. a
14-6 score and a 5-13 score both have a game difference of 8. The value is referred to as the
game difference
Produce a csv file containing the team name and average game difference for each team that
at least one article has been written about.


Task 4

Generate a suitable plot showing the five teams that articles are most frequently written
about and the number of times an article is written about that team.

Task 5

Generate a suitable plot comparing the number of articles written about each team with their
average game difference. Ignore any teams that have no articles written about them.

Task 6 

A written report to communicate the process and activities undertaken in the project,
the analysis, and some limitations contaning - 
 A description of the crawling method and a brief summary the output for Task 1.

 A description of how you scraped data from each page, including any regular expressions
used for Task 2 and a brief summary of the output.

 An analysis of the information shown in the two plots produced for Tasks 4 & 5, including a brief summary of the data used.

 A discussion of the appropriateness of associating the first named team in the article
with the first match score. 

 At least two suggested methods for how you could figure out from the contents of the
article whether the first named team won or lost the match being reported on and a
comment on the advantages and disadvantages of each approach. 

 A discussion of what other information could be extracted from the articles to better understand team performance and a brief suggestion for how this could be done.


