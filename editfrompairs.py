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
        pairs.append([float(ffmpeg.probe(i.audio)["format"]["duration"]), i])

    print(pairs)

    i=0
    curr_start = 0.0
    for pair in pairs:
        stream = ffmpeg.input(vid_base, ss=str(curr_start), t=str(pair[0])).filter("fps", fps=fps)


        #if pair[1] is not None:
        stream = ffmpeg.filter([stream, ffmpeg.input(pair[1].image)], 'overlay', random.randint(10,70), random.randint(10,50))
            
        #stream = ffmpeg.concat(stream, ffmpeg.input(pair[1].audio).audio, v=1, a=1)
            #stream.overlay(ffmpeg.input(pair[1].image))

        stream.output(f"horrible/piece{i}.mp4").run(overwrite_output=True)

        os.system(f"yes | ffmpeg -i horrible/piece{i}.mp4 -i {pair[1].audio} -c copy horrible/piece_a{i}.mp4")

        curr_start += pair[0]
        i+=1
    
    with open("horrible/concat_file.txt", "w+") as file:
        file.write('\n'.join([f"file 'piece_a{l}.mp4'" for l in range(i)]))

    os.system(f"ffmpeg -safe 0 -f concat -i horrible/concat_file.txt -c copy {output}")

    os.system("rm horrible/*")
    os.system("rm img_temp/*")
    os.system("rm audio_temp/*")

if __name__ == "__main__":
    for i in range(30,240):
        print(str(i) + " : " + _framenum_to_timestamp(i))