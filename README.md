# discord-foodbot
Discord bot that integrates into a cooking-themed server.  
Note that the following variables must be added to a .env file in the same folder:  
+ DISCORD_TOKEN={your token here}  
+ DISCORD_GUILD={your guild name here}  
<!-- end of the list -->  
The bot will confirm connection to the server and return a list of the current members.  
Upon a new member joining, the bot will direct message them a welcome message.  

Client-side commands:  
+ "!recipe {dish}" - returns a url to the top result of that dish from allrecipes.com.  
+ "!temp {meat}" - returns the recommended internal temperature of a meat.  
+ "!isolate {url}" - returns lines consisting only of ingredient list and directions from a given allrecipes.com URL, using a BeautifulSoup-based web scraper.  
+ "!milk" - begins a series of prompts requesting user input regarding milk quality metrics. If a value is unknown, imputes the value with the appropriate measure. These variables are fed into a previously-trained milk quality classifier, with the predicted grade returned to the requestor. 
<!-- end of the list -->  
More on the classifier: 
+ An ensemble approach combining naive Bayes, random forest, and logistic regression. 
+ Scikit-learn models were used, with training and testing data from: https://www.kaggle.com/datasets/cpluzshrijayan/milkquality
+ A prediction accuracy of 99% was attained.
<!-- end of the list -->  
