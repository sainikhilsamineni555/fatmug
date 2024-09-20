from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    start_time = models.DecimalField(max_digits=12, decimal_places=3)
    end_time = models.DecimalField(max_digits=12, decimal_places=3)
    content = models.TextField()

    def __str__(self):
        return f"{self.video.title}: {self.content[:50]}"
