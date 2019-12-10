#!/usr/bin/env python
# coding=utf-8
"""
Gopher Timetable v0.0.1
by Paweł Abramowicz
WTFPL
"""

from copy import deepcopy
from random import shuffle
import math

def d(day, hour):
    return (day - 1) * 24 + hour

def imionka(gophers):
    return [g.name for g in gophers]

class Gopher:
    def __init__(self, idx, name, arrv, dept, hours = 0, av4h = 4):
        self.id = idx
        self.name = name
        self.busy = []
        self.av4h = av4h
        self.arrv = arrv
        self.dept = dept
        self.hours = 0
        self.limit = 12

    def is_busy(self, timestamp):
        return len([time for time in self.busy if time <= timestamp]) % 2 == 1

    def hours_since_last_free(self, timestamp):
        self.reduce_overlap_from_to()
        if len([time for time in self.busy if time < timestamp]) % 2 == 1: # jest w trakcie dyżuru, tak, < musi być nie <=
            return timestamp - max([time for time in self.busy if time < timestamp])
        else: #jest wolny
            return 0

    def is_available(self, timestamp):
        return timestamp >= self.arrv \
            and timestamp < self.dept \
            and not self.is_busy(timestamp) \
            and not self.hours_since_last_free(timestamp) >= self.av4h \
            and self.hours < self.limit

    def available_until(self, time_from):
        if self.is_available(time_from):
            busy_after = [time for time in self.busy if time > time_from]
            if busy_after:
                return min([time_from + 2, min(busy_after)])
            else:
                return time_from + 2
        else:
            return None

    def add_duty(self, from_time, to_time):
        print (self.name, from_time, to_time, self.hours, to_time - from_time, self.hours_since_last_free(from_time))
        self.busy.append(from_time)
        self.busy.append(to_time)
        self.hours += to_time - from_time

    def reduce_overlap_from_to(self):
        new_busy = []
        for hour in self.busy:
            if not hour in new_busy:
                new_busy.append(hour)
            else:
                new_busy.remove(hour)
        self.busy = new_busy

class Timetable:
    def __init__(self, gophers, data = {}):
        self.gophers = gophers
        self.data = data

    def add_lane(self, name):
        self.data[name] = {0: False}

    def lane(self, name):
        return self.data[name]

    def lanes(self):
        return self.data

    def duty(self, lane_name, time):
        i = max([k for k in self.data[lane_name].keys() if k <= time])
        return self.data[lane_name][i]

    def next_duty_at(self, lane_name, time):
        next_duty_time = min([k for k in self.data[lane_name].keys() if k > time])
        return next_duty_time

    def mark_not_needed(self, lane_name, from_time, to_time = None):
        self.data[lane_name][from_time] = True
        #dangerous: if its after another timepoint, it will shorten its duty
        if to_time is not None:
            if not to_time in self.data[lane_name]:
                self.data[lane_name][to_time] = False
        else:
            self.data[lane_name][float("inf")] = True

    def assign(self, gopher_id, lane_name, from_time, max_to_time):
        gopher = filter(lambda gopher: gopher.id == gopher_id, self.gophers)[0]
        available_until = min([gopher.available_until(from_time), max_to_time])
        self.data[lane_name][from_time] = gopher
        if not available_until in self.data[lane_name]:
            self.data[lane_name][available_until] = False
        gopher.add_duty(from_time, available_until)


    def valid(self):
        for lane in self.lanes():
            lane = self.lane(lane);
            for duty in lane:
                if lane[duty] == False and not self.available_gophers(duty):
                    return False
        return True

    def full(self):
        for lane in self.lanes():
            lane = self.lane(lane);
            for duty in lane:
                if lane[duty] == False:
                    return False
        return True

    def pick_duty(self):
        for lane_name in self.lanes():
            lane = self.lane(lane_name);
            for duty in lane:
                if lane[duty] == False:
                    return lane_name, duty
        return True

    def available_gophers(self, duty):
        return [g for g in self.gophers if g.is_available(duty)]

    def dump(self):
        for lane_name in self.lanes():
            lane = self.lane(lane_name);
            duties = sorted(lane.keys());
            for duty in duties:
                if type(lane[duty]) == bool:
                    print (lane_name, duty, lane[duty])
                else:
                    print (lane_name, duty, lane[duty].name)

    def rozstaw(self):
        if self.valid():
            if self.full():
                print("FULL! Znaleziono rozwiązanie")
                self.dump()
                return self
            else:
                lane, duty = self.pick_duty()
                # print(lane, duty)

                # lista możliwych kroków
                available_gophers = self.available_gophers(duty)
                shuffle(available_gophers)

                # wybierz krok i rozstaw self.deepcopy
                # zbierz wynik, jeśli wyrzucił, to super, jak nie, to wybierz kolejny krok
                for gopher in available_gophers:
                    tt = Timetable(deepcopy(self.gophers), deepcopy(self.data))
                    tt.assign(gopher.id, lane, duty, tt.next_duty_at(lane, duty))
                    works = tt.rozstaw()
                    if works:
                        return works

                # jeśli zabrakło kroków:
                print("ZABRAKŁO. Szukamy dalej.")
                self.dump()
                return None
        else:
            print("INVALID. Szukamy dalej.")
            self.dump()
            return None

g = []
g.append(Gopher(0, "Ultras z Niedzieli", d(3, 0), d(3, 24)))
g.append(Gopher(1, "Leszek", d(1, 8), d(3, 20)))
g.append(Gopher(2, "Staszek", d(1, 0), d(3, 24)))
g.append(Gopher(3, "Staszek 2.0", d(1, 0), d(3, 24)))
g.append(Gopher(4, "Sobotni nocny marek", d(2, 17), d(2, 24)))

# Ultras z niedzieli chce być na prelce 3 dnia od 9 do 12
g[0].busy = [d(3, 9), d(3, 12)]

tt = Timetable(g)

tt.add_lane("animce")
tt.mark_not_needed("animce", d(1,  0), d(1, 9))
tt.mark_not_needed("animce", d(1, 21), d(2, 9))
tt.mark_not_needed("animce", d(2, 21), d(3, 9))
tt.mark_not_needed("animce", d(3, 21))

tt.rozstaw()
