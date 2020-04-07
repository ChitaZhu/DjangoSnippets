from django.db import models

# Create your models here.
# mysite/news/models.py

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)
    # 模型显示，默认为 id
    # eg. <QuerySet [<Reporter: Smith>, <Reporter: Lily>]>
    def __str__(self):
        return self.full_name
    # 可对要存储到数据库的数据进行处理    
    def save(self, *args, **kwargs):
        super(Reporter, self).save(*args, **kwargs)
    # 序列中增加一个字段，但不会写入数据库    
    @property
    def keyword(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.headline