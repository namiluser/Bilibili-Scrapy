# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os


class DtvPipeline:
    def process_item(self, item, spider):
        path = './video.csv'
        try:
            if not os.path.exists(path):
                with open('./video.csv', 'w', newline="", encoding='utf-8') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(['title','Likes', 'Playback_volume', 'Number_of_barrages', 'Number_of_coins_invested',
                                     'Collection_volume', 'Forwarding_volume'])
                    writer.writerow([item['title'],item['Likes'], item['Playback_volume'], item['Number_of_barrages'] ,
                                     item['Number_of_coins_invested'],
                                     item['Collection_volume'], item['Forwarding_volume']])
            else:
                with open(path, 'a', newline="", encoding='utf-8') as fp:
                    writer = csv.writer(fp)
                    writer.writerow([item['title'],item['Likes'], item['Playback_volume'], item['Number_of_barrages'],
                                     item['Number_of_coins_invested'],
                                     item['Collection_volume'], item['Forwarding_volume']])
        except:
            print(item['title']+'数据保存失败！')
        return item
