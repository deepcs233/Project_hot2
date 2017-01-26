#! /bin/sh
export PATH=$PATH:/usr/local/bin  
cd /home/ubuntu/project_hot2/naive-scrapy-master
scrapy crawlall >> /home/ubuntu/scrapy.log 2>&1 
python /home/ubuntu/project_hot2/processdata.py >> /home/ubuntu/processdata.log 2>&1