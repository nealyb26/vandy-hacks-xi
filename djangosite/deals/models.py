from django.db import models

class Post(models.Model):
    product_name = models.CharField(max_length=200)
    location = models.CharField(max_length = 200) # TODO: Change to location info
    info_text = models.CharField(max_length = 500)
    upvotes = models.IntegerField(default = 0)
    downvotes = models.IntegerField(default = 0)
    post_date = models.DateTimeField("date posted")

    def __str__(self) -> str:
        return f"{self.product_name}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body_text = models.CharField(max_length=1000)
    post_date = models.DateTimeField("date posted")

    def __str__(self) -> str:
        return f"Post: {self.post}; Text: \"{self.body_text:.20}\""