for %i in (scene1Frames/*.png) do ffmpeg -hide_banner -loglevel quiet -i scene1Frames/%i -s 1920x1080 scene1FramesComp/%i
