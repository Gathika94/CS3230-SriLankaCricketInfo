import scrapy
import json


class CricketSpider(scrapy.Spider):
    name = "cricket"

    start_urls = [
        'https://island-cricket.com/cricket-news'
    ]

    for i in range(1, 170):
        start_urls.append("https://island-cricket.com/cricket-news?page=" + str(i))



    def parse(self,response):
        newsItems = ['div.views-row.views-row-1.views-row-odd.views-row-first',
                     'div.views-row.views-row-2.views-row-even',
                     'div.views-row.views-row-3.views-row-odd',
                     'div.views-row.views-row-4.views-row-even',
                     'div.views-row.views-row-5.views-row-odd',
                     'div.views-row.views-row-6.views-row-even',
                     'div.views-row.views-row-7.views-row-odd',
                     'div.views-row.views-row-8.views-row-even',
                     'div.views-row.views-row-9.views-row-odd',
                     'div.views-row.views-row-10.views-row-even'
                     ]
        for item in newsItems:
            href = response.css('div.view.view-page-news-2014.view-id-page_news_2014.view-display-id-page_1.view-dom-id-1').css(item).css('div.views-field-title').css('span.field-content').css('a::attr(href)').extract_first()
            yield response.follow(href, self.parse_news_page)


    def parse_news_page(self,response):
        title = response.css('h1::text').extract_first()
        submittimeDetails = response.css('span.submitted::text').extract();
        print()
        year=""
        month=""
        date = ""
        time = ""
        if(len(submittimeDetails)>1):
            timeDetails= submittimeDetails[1]
            splittedTimeDetails = timeDetails.split()
            month = splittedTimeDetails[1]
            date = splittedTimeDetails[2]
            year = splittedTimeDetails[3]
            time = splittedTimeDetails[5]

        description = response.css('div.field.field-type-text.field-field-news-summary').css('div.field-items').css('div.field-item.odd::text').extract_first()
        origin_url = response.css('div.field.field-type-link.field-field-source').css('div.field-items').css('div.field-item.odd').css('a::attr(href)').extract_first()

        output = {
            'title': title,
            'description': description,
            'origin_url': origin_url,
            'year':year,
            'month' : month,
            'date' : date,
            'time' : time

        }

        data_file = open("cricket_data.json", "a+")
        data_file.write(json.dumps(output, indent=2, sort_keys=True))
        data_file.write(",\n")
        data_file.close()

        yield {
            'title': title,
            'description': description,
            'origin_url': origin_url,
            'year':year,
            'month' : month,
            'date' : date,
            'time' : time
        }