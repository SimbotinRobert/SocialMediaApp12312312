from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    post_name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    post_content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/',blank=True,null=True)
    def __str__(self):
        return self.post_name

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Unic:
    unique_together = ('user', 'post')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    def __str__(self):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',default='profile_pics/default.jpg',blank=True)
    def __str__(self):
        return f'Profilul lui {self.user.username}'

class Vote(models.Model):
    Vote_choices = (
        (1,'Like'),
        (-1,'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=Vote_choices)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name='Vot'
        verbose_name_plural='Voturi'

    def __str__(self):
        return f'{self.user.username} a votat {self.post.post_name} ({self.value})'