import argparse
import os
import hashlib

mapDirs = {}  # for directories -c
mapFiles = {}  # for files -c
mapDirName = {}  # for directories -n
mapFileName = {}  # for files -n
mapFileSizes = {}  # for files size
mapDirSizes = {}  # for dirs size {path|size}


# generates an hash value for files
def hashGenerate(fileName, size=65536):
    hashValue = hashlib.sha256()
    with open(fileName, "rb") as f:
        ch = f.read(size)
        while ch:
            hashValue.update(ch)
            ch = f.read(size)

    return hashValue.hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument('listOfDirs', metavar='N', type=str, nargs='*', help='paths to traverse')
parser.add_argument('-d', action='store_true')
parser.add_argument('-f', action='store_true')
parser.add_argument('-c', action='store_true')
parser.add_argument('-n', action='store_true')
parser.add_argument('-s', action='store_true')
args = parser.parse_args()


# takes two dictionaries (which are for contents and names) and creates a new dictionary for -cn option
def mergeDicts(dict1, dict2):  # dict1 is for contents , dict2 is for names
    newDict = {}
    reverseDict1 = {}  # with reverse keys and values
    reverseDict2 = {}
    for hashC, listC in dict1.items():
        for pathC in listC:
            reverseDict1[pathC] = hashC

    for hashN, listN in dict2.items():
        for pathN in listN:
            reverseDict2[pathN] = hashN

    for path, hashValue in reverseDict1.items():
        if (hashValue, reverseDict2[path]) in newDict:
            newDict[(hashValue, reverseDict2[path])].append(path)
        else:
            newDict[(hashValue, reverseDict2[path])] = [path]

    return newDict


# for -c argument and with given directory name, places all contents of it in appropiate maps and positions
def solution_c(dirname):
    listAll = os.listdir(dirname)
    listFiles = []
    listDirs = []
    dirsHashes = []
    filesHashes = []

    for elements in listAll:
        abspth = os.path.join(dirname, elements)
        if os.path.isdir(abspth):
            listDirs.append(abspth)
        else:
            listFiles.append(abspth)

    for files in listFiles:
        flHash = hashGenerate(files)
        filesHashes.append(flHash)
        if (flHash in mapFiles) and (files not in mapFiles[flHash]):
            mapFiles[flHash].append(files)
        elif flHash not in mapFiles:
            mapFiles[flHash] = [files]

    for dirs in listDirs:
        dirsHashes.append(solution_c(dirs))

    newList = dirsHashes + filesHashes
    newList.sort()
    hashes = ""
    for strs in newList:
        hashes += strs
    ultimateHashValue = hashlib.sha256(hashes.encode('utf-8')).hexdigest()
    if (ultimateHashValue in mapDirs) and (dirname not in mapDirs[ultimateHashValue]):
        mapDirs[ultimateHashValue].append(dirname)
    elif ultimateHashValue not in mapDirs:
        mapDirs[ultimateHashValue] = [dirname]
    return ultimateHashValue


# for -n argument and with given directory name, places all contents of it in appropiate maps and positions
def solution_n(dirname):
    listAll = os.listdir(dirname)
    listFiles = []
    listDirs = []
    dirsHashes = []
    filesHashes = []
    for elements in listAll:
        abspth = os.path.join(dirname, elements)
        if os.path.isdir(abspth):
            listDirs.append(abspth)
        else:
            listFiles.append(abspth)

    for files in listFiles:
        flHash = hashlib.sha256((os.path.basename(files)).encode('utf-8')).hexdigest()
        filesHashes.append(flHash)
        if (flHash in mapFileName) and (files not in mapFileName[flHash]):
            mapFileName[flHash].append(files)
        elif flHash not in mapFileName:
            mapFileName[flHash] = [files]

    for dirs in listDirs:
        drHash = hashlib.sha256((os.path.basename(dirs)).encode('utf-8')).hexdigest()
        dirsHashes.append(drHash)

    newList = dirsHashes + filesHashes
    newList.sort()
    hashes = ""
    for strs in newList:
        hashes += strs
    hashes = hashlib.sha256((os.path.basename(dirname)).encode('utf-8')).hexdigest() + hashes
    ultimateHashValue = hashlib.sha256(hashes.encode('utf-8')).hexdigest()
    if (ultimateHashValue in mapDirName) and (dirname not in mapDirName[ultimateHashValue]):
        mapDirName[ultimateHashValue].append(dirname)
    elif ultimateHashValue not in mapDirName:
        mapDirName[ultimateHashValue] = [dirname]
    for dirss in listDirs:
        solution_n(dirss)


# places all contents of a given directory name in a dictionary with respect ot their values
def solutionSizes(dirname):
    listAll = os.listdir(dirname)
    listFiles = []
    listDirs = []
    for elements in listAll:
        abspth = os.path.join(dirname, elements)
        if os.path.isdir(abspth):
            listDirs.append(abspth)
        else:
            listFiles.append(abspth)
    totalSize = 0
    for files in listFiles:
        fileSize = os.path.getsize(files)
        totalSize += fileSize
        if files not in mapFileSizes:
            mapFileSizes[files] = fileSize

    for dirs in listDirs:
        totalSize += solutionSizes(dirs)

    if dirname not in mapDirSizes:
        mapDirSizes[dirname] = totalSize

    return totalSize


# by using global dictionary variables (mapFiles, mapDirs ...) prints necessary file or directory paths
def printPaths(pathList):
    curr = os.path.abspath(".")
    for paths in pathList:
        solution_c(os.path.join(curr, paths))
        solution_n(os.path.join(curr, paths))
        solutionSizes(os.path.join(curr, paths))
    if not args.n:  # look for files contents with sizes or without sizes
        if not args.d:
            mapToUse = mapFiles
        else:
            mapToUse = mapDirs
    elif args.n and (not args.c):
        if not args.d:
            mapToUse = mapFileName
        else:
            mapToUse = mapDirName
    else:
        if not args.d:
            mapToUse = mergeDicts(mapFiles, mapFileName)
        else:
            mapToUse = mergeDicts(mapDirs, mapDirName)
    listWithSize = []
    for key, value in mapToUse.items():
        if len(value) > 1:
            value.sort()
            if not args.d:
                size = mapFileSizes[value[0]]
            else:
                size = mapDirSizes[value[0]]
            if args.s:
                listWithSize.append((size, value))
            else:
                listWithSize.append(value)
    if args.s:  # checks if -s argument is used or not
        listWithSize.sort(key=lambda x: x[1])
        listWithSize.sort(reverse=True, key=lambda x: x[0])
        for size, elements in listWithSize:
            for pats in elements:
                if args.c or not args.n:
                    print(pats, "\t", size)
                else:  # ignores -s argument and doesn't print sizes if -n and -s arguments are used together
                    print(pats)
            print("")
    else:
        listWithSize.sort()
        for elements in listWithSize:
            for pats in elements:
                print(pats)
            print("")


pathlist = args.listOfDirs
if len(pathlist) == 0:
    pathlist = [""]  # if no path is printed on console as argument, program works with current directory
printPaths(pathlist)

