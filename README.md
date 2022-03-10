# Edit and Convert Subtitle
this python module provide subtitle parse, edit and convert for srt and webvtt formats. you can  read, edit and convert any valid srt or webvtt file.

* Support UTF-8 , ANSI encoding

# Read

~~~py
from subtitle_editor import SubtitleEditor

subtitle = SubtitleEditor("yoursubtitle.srt")

subtitle.as_array # subtitle timeline as array
subtitle.as_objects # subtitle timeline as block objects
~~~

# Convert 

~~~py
subtitle.webvtt_as_bytes # webvtt file as bytes
subtitle.save_webvtt("outpath.vtt")
# or
subtitle.srt_as_bytes # srt file as bytes
subtitle.save_srt("outpath.srt")
~~~


# Edit

~~~py
subtitle.blocks # this property return block directory
subtitle.edit_block(id:int, timedelta:str, content:str) # change block by id
~~~
