# InfoTrie Exercise
## Periodic Web Crawler to fetch latest news from FinSents

This program is a crawler to fetch latest articles from http://www.finsents.com/Home/GetDashBoardData .
It runs every 10 seconds, sends an HTTP POST request to webpage, and process fetched result.  
A datetime pointer will be stored to detect latest article datetime, therefore, any old articles will not be stored duplicate.

Fetched results are stored in InfoTrie_latest_news.txt . Every line is a piece of article. This ways allow scalable article storage. New articles will be appended at the end of the file. A sample of the result file is in the repository.
