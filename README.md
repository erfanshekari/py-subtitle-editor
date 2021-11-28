# Edit and Convert Subtitle
this python module provide subtitle parse and edit for srt and webvtt format. you can  read, edit and convert any valid srt or webvtt file.

# read

~~~py
from subtitle_editor import SubtitleEditor

subtitle = SubtitleEditor("yoursubtitle.srt")

subtitle.as_array # subtitle timeline as array
subtitle.as_objects # subtitle timeline as block objects
~~~
