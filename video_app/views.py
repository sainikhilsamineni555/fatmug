import ffmpeg
from django.shortcuts import render, redirect
from .models import Video, Subtitle
from .forms import VideoForm
from django.core.files.storage import FileSystemStorage

import os
import ffmpeg
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Video, Subtitle
from .forms import VideoForm

import os
import ffmpeg
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Video, Subtitle
from .forms import VideoForm

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            video_path = video.video_file.path
            subtitle_path_srt = os.path.join(settings.MEDIA_ROOT, f'subtitles/{video.title}.srt')
            subtitle_path_vtt = os.path.join(settings.MEDIA_ROOT, f'subtitles/{video.title}.vtt')
            os.makedirs(os.path.dirname(subtitle_path_srt), exist_ok=True)
            ffmpeg.input(video_path).output(subtitle_path_srt).run()
            ffmpeg.input(subtitle_path_srt).output(subtitle_path_vtt).run()
            save_subtitles(video, subtitle_path_srt)

            return redirect('list_videos')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})

def save_subtitles(video, subtitle_path):
    with open(subtitle_path, 'r') as f:
        content = f.readlines()

    start_time, end_time, subtitle_content = None, None, ''
    for line in content:
        if '-->' in line:
            start_time, end_time = [convert_timecode(tc) for tc in line.split(' --> ')]
        elif line.strip().isdigit():
            continue
        elif line.strip():
            subtitle_content += line.strip() + ' '
        else:
            if start_time and end_time and subtitle_content:
                # Save each subtitle entry in the database
                Subtitle.objects.create(
                    video=video,
                    start_time=start_time,
                    end_time=end_time,
                    content=subtitle_content.strip()
                )
            start_time, end_time, subtitle_content = None, None, ''
            
def convert_timecode(tc):
    h, m, s = tc.replace(',', '.').split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)




def list_videos(request):
    videos = Video.objects.all()
    return render(request, 'list_videos.html', {'videos': videos})

from django.db.models import Q

from django.db.models import Q
from django.conf import settings

def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    subtitles = video.subtitles.all()
    sub = []
    query = request.GET.get('q')
    if query:
        sub = subtitles.filter(Q(content__icontains=query))
    
    # Generate subtitle track URL
    subtitle_track = f'{settings.MEDIA_URL}subtitles/{video.title}.vtt'
    
    return render(request, 'video_detail.html', {
        'video': video,
        'subtitles': sub,
        'subtitle_track': subtitle_track
    })


