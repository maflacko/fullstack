import scrapy
from scrapy import Request
from musicscrawler.items import ArtistItem


class ArtistsFmSpider(scrapy.Spider):
    name = 'artistsFM'
    allowed_domains = ['last.fm']
   #URL 10 pages rnb et 10 pages pop
    
    start_urls = [
        f'https://www.last.fm/tag/rnb/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/pop/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/hip-hop/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/alternative/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/blues/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/jazz/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/jazz/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/indie/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/80s/artists?page={page}' for page in range(1, 11)
    ]+[
        f'https://www.last.fm/tag/rap/artists?page={page}' for page in range(1, 11)
    ]
    
    ##start_urls = [ 'https://www.last.fm/tag/rap/artists']
    
    
    def parse(self, response):
        genre = response.url.split('/')[-2]  #Extrait le genre dans l'url
        for artist in response.css('.big-artist-list-item'):
            artist_name = artist.css('.big-artist-list-title a::text').get()
            listeners = artist.css('.big-artist-list-listeners::text').get()
            artist_url = artist.css('.big-artist-list-title a::attr(href)').get()
            #requête à la page artiste pour avoir des infos supplémentaires
            yield Request(response.urljoin(artist_url), 
                          callback=self.parse_artist_page, 
                          meta={'artist_name': artist_name, 'genre': genre, 'listeners': listeners})

    def parse_artist_page(self, response):
        top_albums = response.css('h3.artist-top-albums-item-name a::text').getall()
        top_songs = response.css('td.chartlist-name a::text').getall()
        tags = []
        #ajoute nouvelles meta
        response.meta.update({
            'top_albums': top_albums,
            'top_songs': top_songs
        })
    
        #URL pour "View all tags"
        tags_url = response.urljoin(response.css('a.tags-view-all::attr(href)').get())

        yield scrapy.Request(tags_url, callback=self.parse_tags,  meta=response.meta)



    def parse_tags(self, response):
        #Scraper page "View all tags"
        tags = response.css('h3.big-tags-item-name a::text').getall()
            
        yield ArtistItem(
            artist_name=response.meta['artist_name'],
            genre=response.meta['genre'],
            listeners=response.meta['listeners'],
            top_albums=response.meta['top_albums'],
            top_songs=response.meta['top_songs'],
            tags=tags
        )

      
