from FileReader import FileReader
from FileWriter import FileWriter

data = FileReader("trivialExample.in")

videosCached = {}

cacheContents = {}

for cache in range(data.nCaches):
    filled = 0
    while True:
        bestVideo, score = None, 0
        for video in range(data.nVideos):
            videoSize = data.videoSizes[video]
            if videoSize + filled > data.cacheCapacity:
                continue
            improvement = 0
            for endpoint in data.endpoints:
                try:
                    lat = endpoint.cacheServers[cache]
                    rqn = endpoint.requests[video]
                    # TODO check the video isn't already in a closer cache
                    improvement += ( endpoint.latency - lat) * rqn
                except KeyError:
                    continue

            print(improvement)
            if improvement > score:
                bestVideo, score = video, improvement

        if bestVideo is None:
            break

        if cache in cacheContents:
            cacheContents[cache].append(bestVideo)
            filled += data.videoSizes[bestVideo]
        else:
            cacheContents[cache] = [bestVideo]

writer = FileWriter("example.out")
writer.writeData(cacheContents)
