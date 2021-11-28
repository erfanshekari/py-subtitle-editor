from subtitle_editor import SubtitleEditor


subtitle = SubtitleEditor("mysubtitle.srt")

subtitle.save_webvtt("./outpath.webvtt")