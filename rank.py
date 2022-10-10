import os

songs = {} # name -> count
for filename in os.listdir('.'):
    filename = filename.lower()
    if not filename.endswith('.mp3'):
        continue
    song = filename[8:] # strip yyyy-mm-
    songs[song] = songs.get(song, 0) + 1

counts = [(count, song) for (song, count) in songs.items()]
counts.sort()
if 0:
    for count, song in counts[:10]:
        print(count, song)
    print('...')
for count, song in counts[-10:]:
    print(count, song)
print()


