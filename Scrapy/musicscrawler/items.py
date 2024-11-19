import scrapy


class ArtistItem(scrapy.Item):
    artist_name = scrapy.Field()
    genre = scrapy.Field()
    listeners = scrapy.Field()
    top_albums = scrapy.Field()
    top_songs = scrapy.Field()
    tags = scrapy.Field()

    pass
