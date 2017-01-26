#! /bin/sh
export PATH=$PATH:/usr/local/bin  
cd /home/ubuntu/project_hot2/naive-scrapy-master
echo '-------------------------------------------' >> /home/ubuntu/scrapy.log
echo '-------------------------------------------' >> /home/ubuntu/processdata.log
date +%Y-%m-%d-%Hh-%Mm-%Ss  >> /home/ubuntu/scrapy.log
date +%Y-%m-%d-%Hh-%Mm-%Ss  >> /home/ubuntu/processdata.log
echo '-------------------------------------------' >> /home/ubuntu/scrapy.log
echo '-------------------------------------------' >> /home/ubuntu/processdata.log

#scrapy crawlall >> /home/ubuntu/scrapy.log 2>&1 
python /home/ubuntu/project_hot2/processdata.py >> /home/ubuntu/processdata.log 2>&1
