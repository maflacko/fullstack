FROM python:3.9

WORKDIR /scrapy

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


#lance le spider et insère les données dans la bdd Mongo grâce à la pipeline 
CMD ["scrapy", "crawl", "artistsFM"] 

#ligne à commenter si on ne veut pas scraper de nouveau et inserer dans la bdd
#CMD ["tail", "-f", "/dev/null"]
