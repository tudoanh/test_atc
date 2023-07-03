import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose, TakeFirst
from crawler.items import CouncilItem
import pandas as pd


class LacitySpider(CrawlSpider):
    name = "lacity"
    allowed_domains = ["cityclerk.lacity.org"]
    start_urls = ["https://cityclerk.lacity.org"]

    # TODO: add rules to crawl all pages
    rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        """
        @url https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=20-0631
        @scrapes title url council_id data documents activities
        """
        council_item = ItemLoader(item=CouncilItem(), response=response)
        council_item.add_value("url", response.url)
        council_item.add_xpath("council_id", "//h1[@id='CouncilFileHeader']//text()",
                               MapCompose(lambda x: x.split(": ")[1]))
        
        reclabels = council_item.get_xpath(
            "//div[@id='viewrecord']//div[@class='reclabel']//text()",
        )
        rectexts = council_item.get_xpath(
            "//div[@id='viewrecord']//div[@class='rectext']//text()",
        )

        # Get file activities
        if reclabels[-1] == "File Activities":
            # get table id="inscrolltbl" then parse
            activities = council_item.get_xpath(
                "//div[@id='viewrecord']//table[@id='inscrolltbl']",
            )
            activities = pd.read_html(activities[0])
            # drop last column
            activities = activities[0].drop(activities[0].columns[-1], axis=1)
            # convert to dict
            activities = activities.to_dict(orient="records")
            # TODO: parse documents attached with JS
            council_item.add_value("activities", activities)
            # drop last from reclabels
            reclabels = reclabels[:-1]
        
        # zip reclabels and rectexts
        data = dict(zip(reclabels, rectexts))
        council_item.add_value("data", data)

        council_item.add_value("title", data["Title"])

        # Get file documents
        # id['xboxholder'] -> table id='inscrolltbl' as pandas
        documents = council_item.get_xpath(
            "//div[@id='xboxholder']/div[2]/table[@id='inscrolltbl']",
        )
        documents = pd.read_html(documents[0])

        # get all documents links
        document_links = council_item.get_xpath(
            "//div[@id='xboxholder']/div[2]/table[@id='inscrolltbl']//a/@href",
        )
        # add links to documents as a new column
        documents[0]["links"] = document_links
        # rename columns
        documents[0].columns = ["Title", "Date", "Links"]

        council_item.add_value("documents", documents[0].to_dict(orient="records"))

        return council_item.load_item()
