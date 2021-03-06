import csv
import glob
import os
import pandas as pd
import numpy as np
import csv

translate = {'C':1, 'D':3, 'E':5, 'F':6, 'G':8, 'A': 10, 'B': 12, '[': 0}
adjust = {'0': 0, 'b': -1, '#':1, 'e': 0, '-':-1, ']' : 0}
chordmap = {}
beat = []

def all_chord_types(files):
    for file in files:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            all_list = list(reader)
            for a in all_list:
                if(a[5] in note):
                    note[a[5]] += 1
                else:
                    note[a[5]] = 1
                    #  perform calculation


def note_to_num_one(a):
    number = 0
    if (a[6][0] in translate.keys() and a[6][1] in adjust.keys()):
        note = translate[a[6][0]]
        adj = adjust[a[6][1]]
        #print(a[4], note, adj)
        return str(note + adj)
    if(a[6] == "note_root"): 
        return "note_root"
    else: 
        return "0"


def build_chord_map():
    with open("chordtype.csv", 'r') as f:
        reader = csv.reader(f)
        all_list = list(reader)
        for a in all_list:
            key = a[0]
            values = []
            for i in range(1, len(a)):
                if a[i] != '':
                    values.append(int(a[i]))
            chordmap[key] = values
    print(chordmap)


def chord_to_num_one(a):
    if (a[4] !='chord_root'):
        chord = a[3]
        note = a[4][0]
        adj = a[4][1]
        #print(a[4], note, adj)
        number = 0
        note2 = 0
        note3 = 0
        if note in translate.keys():
            number = translate[note] + adjust[adj]
            if chord in chordmap.keys():
                note2 = (number + chordmap[chord][0] - 1) % 12 + 1
                note3 = (number + chordmap[chord][1] - 1) % 12 + 1
            #a[4] = [number, note2, note3]
            a[4] = number
    return str(a[4]) 


def makeVector(files):
    c = 0
    for file in files:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            all_list = list(reader)
            remain = 0
            song = []
            for a in all_list:
                a[4] = chord_to_num_one(a)
                a[6] = note_to_num_one(a)
                if(a[8] != 'note_duration'):
                    count = float(a[8])
                    if(remain != 0):
                        count += remain
                        remain = 0
                    if(count == 1):
                        song.append(a)
                    while count > 1:
                        a[8] = 1
                        song.append(a)
                        count -= 1
                    if(count < 1):
                       remain = count
                #else: song.append(a)
            with open(str(c)+'.csv', 'w', newline='') as myfile:
                wr = csv.writer(myfile, delimiter=',')
                for i in range(24):
                    wr.writerow([0,0])
                for a in song:
                    wr.writerow([a[6], a[4]])
                for i in range(24):
                    wr.writerow([0,0])
        c+=1
    print(c)

        

path = 'csv_train'
note = {}
files = glob.glob(os.path.join(path, '*.csv'))

#note_to_num(files)
build_chord_map()
#chord_to_num(files)
makeVector(files)
print(beat)





print(sorted(note, key=note.get))
