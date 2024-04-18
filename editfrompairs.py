from pair import AudioThumbnailPair
import ffmpeg
import random
import os

def _framenum_to_timestamp(frame:int, fps:int=30) -> str:
    print(f"{round((frame)/(fps),4)}s")
    return f"{round((frame)/(fps),4)}s"

def video_from_pairs(input_:list[AudioThumbnailPair], vid_base="videos/surfers1.mp4", fps=30, output="out.mp4") -> None:
    pairs:list[float, AudioThumbnailPair] = []
    for i in input_:
        pairs.append([float(ffmpeg.probe(i.audio)["format"]["duration"]) + 3.0, i])

    print(pairs)

    i=0
    curr_start = 0.0
    for pair in pairs:
        stream = ffmpeg.input(vid_base, ss=str(curr_start), t=str(pair[0])).filter("fps", fps=fps)


        if pair[1] is not None:
            stream = ffmpeg.filter([stream, ffmpeg.input(pair[1].image)], 'overlay', random.randint(10,70), random.randint(10,50))
            #stream.overlay(ffmpeg.input(pair[1].image))

        curr_start += pair[0]
        stream.output(f"horrible/piece{i}.mp4").run()
        i+=1

    (
        ffmpeg
        .concat(*[ffmpeg.input(f"horrible/piece{j}.mp4") for j in range(i)])
        .output(output)
        .run()
    )

    os.system("rm horrible/*")

if __name__ == "__main__":
    for i in range(30,240):
        print(str(i) + " : " + _framenum_to_timestamp(i))