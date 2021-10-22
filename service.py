import os
import subprocess
from datetime import datetime, timedelta
from uuid import uuid4

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip


def create_new_filename():
    return f'{str(uuid4())[:8]}.avi'


def get_subclip(record, start_time, end_time):
    output_filename = create_new_filename()

    record.start_time = record.start_time.replace(tzinfo=None)

    start_offset = start_time - record.start_time
    end_offset = end_time - record.start_time

    ffmpeg_extract_subclip(
        filename=f'../video-storage/media/{record.file_name}',
        t1=start_offset.total_seconds(),
        t2=end_offset.total_seconds(),
        targetname=os.path.join(output_filename)
    )

    return output_filename


def make_clip_from_two_subclips(record1, record2, start_time, end_time):
    end_of_record1 = VideoFileClip(f'media/{record1.file_name}').duration

    file1 = get_subclip(record1, start_time=start_time, end_time=end_of_record1)
    file2 = get_subclip(record2, start_time=0, end_time=end_time)

    output_filename = create_new_filename(record1.file_name)

    subprocess.call(['mkvmerge',
                     '-o',
                     f'{os.path.join(output_filename)}',
                     f'{file1}',
                     '+',
                     f'{file2}'])

    os.remove(file1)
    os.remove(file2)

    return output_filename


def get_output_file(start_time: datetime, end_time: datetime, filenames):

    files = []

    for filename in filenames:
        file = get_subclip(filename, start_time=start_time, end_time=end_time)
        files.append(file)
        # else:
        #     for rec in recs:
        #         file = get_subclip(rec, start_time=start_time, end_time=end_time)
        #         files.append(file)

    return files
