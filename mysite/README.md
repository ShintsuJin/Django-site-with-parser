# My first django site with parser and asyncio parser
+ ### Description:
    This site has a **parser** which parsing some data from this [site](https://mignews.com/), after that **parser** sends data by post requests to rest-API.
    Rest-API *serializes* that data and displays news on site in category 'parser'.
    So you can run that script which has named 'parser' and it'll be work. By the way you could build docker image and run it with the command **[sudo docker run -p 8000:8000 django3]**
    **In new release added asyncio parser which parse data asynchronously, just run it through the app 'asyncparser'**
>**P.S: If you are from Russia, unfortunately, you have to use VPN before run parser, otherwise it won't work, due to site was blocked** 