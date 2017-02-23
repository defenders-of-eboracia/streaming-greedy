import sys

from FileReader import FileReader
from FileWriter import FileWriter

file = sys.argv[1]

data = FileReader(file)

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
            
            if cache in cacheContents and video in cacheContents[cache]:
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
