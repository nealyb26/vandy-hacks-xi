from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.IntegerField(default = 0xFFFFFF)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    product_name = models.CharField(max_length=200)

    location_name = models.CharField(max_length = 200)
    location_street_address = models.CharField(max_length = 200)
    location_lat = models.FloatField(default = 36.1446206)
    location_long = models.FloatField(default = -86.8032659)

    info_text = models.CharField(max_length = 500)
    score = models.IntegerField(default = 0)
    post_date = models.DateTimeField("date posted")

    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.product_name}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body_text = models.CharField(max_length=1000)
    post_date = models.DateTimeField("date posted")

    def __str__(self) -> str:
        return f"Post: {self.post}; Text: \"{self.body_text:.20}\""