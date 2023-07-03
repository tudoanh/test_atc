# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from lacity.models import Council, Document, Voter, Vote, Activity


class CrawlerPipeline:
    def process_item(self, item, spider):
        print(item)
        if not Council.objects.filter(council_id=item["council_id"]).exists():
            council = Council.objects.create(
                council_id=item["council_id"],
                title=item["title"],
                url=item["url"],
                data=item["data"],
            )
            for document in item["documents"]:
                Document.objects.create(
                    council=council,
                    date=document["Date"],
                    title=document["Title"],
                    url=document["Links"],
                    data=document,
                )
            for activity in item["activities"]:
                Activity.objects.create(
                    council=council,
                    date=activity["Date"],
                    activity=activity["Activity"],
                )
        return item
