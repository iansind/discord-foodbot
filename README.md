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
<!-- end of the list -->  
