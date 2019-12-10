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
# g.append(Gopher(0, "Ultras z Niedzieli", d(3, 0), d(3, 24)))
# g.append(Gopher(1, "Leszek", d(1, 8), d(3, 20)))
# g.append(Gopher(2, "Staszek", d(1, 0), d(3, 24)))
# g.append(Gopher(4, "Sobotni nocny marek", d(2, 17), d(2, 24)))
# g[0].busy = [d(3, 9), d(3, 12)]

g.append(Gopher(0, "Karolina 'karolincia' Gross", d(1, 9), d(3, 18)))
g.append(Gopher(1, "Ordyński 'blindpriest' Jakub", d(1, 19), d(3, 15)))
g.append(Gopher(2, "Anna 'Anek12' Kłakulak", d(1, 22), d(3, 19)))
g.append(Gopher(3, "Abdullaeva 'evangelie' Kamila", d(1, 6), d(3, 18)))
g.append(Gopher(4, "Zuzanna 'Toperz' Brygier", d(1, 9), d(3, 23)))
g.append(Gopher(5, "Alicja 'wlazło' Wlazło", d(1, 12), d(3, 16)))
g.append(Gopher(6, "Agnieszka 'Soraka' Zatorska", d(1, 13), d(3, 13)))
g.append(Gopher(7, "Pasek 'pasio' Jakub", d(1, 6), d(3, 13)))
g.append(Gopher(8, "Marta 'Imponderabilia' Wejman", d(1, 14), d(3, 17)))
g.append(Gopher(9, "Oliwia 'tychilo' Gertych", d(1, 14), d(3, 17)))
g.append(Gopher(10, "Katarzyna 'Chocolat' Domańska", d(1, 9), d(3, 23)))
g.append(Gopher(11, "Magdalena 'Kuroś96' Kurowska", d(1, 11), d(3, 17)))
g.append(Gopher(12, "Agata 'RebelTigera' Mikulska", d(1, 9), d(3, 23)))
g.append(Gopher(13, "Julia 'Lowkey' Konefał", d(1, 9), d(3, 15)))
g.append(Gopher(14, "Pakulska 'Paku' Karolina", d(1, 12), d(3, 20)))
g.append(Gopher(15, "Łukasz 'Sileanth' Magnuszewski", d(1, 19), d(3, 16)))
g.append(Gopher(16, "Ola 'Molfii' Myślińska", d(1, 8), d(3, 18)))
# g.append(Gopher(17, "Weronika 'trombaj' Dylewska", d(1, 19), d(3, 16)))
# g.append(Gopher(18, "Paweł 'Cron' Kalka", d(1, 16), d(3, 12)))
# g.append(Gopher(19, "Dominik 'LesNY_Pablo' Pawlicki", d(1, 18), d(3, 15)))
# g.append(Gopher(20, "Nicolas 'nico130kk' Grdeń", d(1, 12), d(3, 14)))
# g.append(Gopher(21, "Figarska 'Bernardita_Ramos' Blanka", d(1, 16), d(3, 16)))
# g.append(Gopher(22, "Klaudia 'Silmaril' Nowacka", d(1, 10), d(3, 18)))
# g.append(Gopher(23, "Joanna 'beidak' Marzewska", d(1, 12), d(3, 18)))
# g.append(Gopher(24, "Zuzanna 'Zuz' Politowicz", d(1, 16), d(3, 17)))
# g.append(Gopher(25, "Dominiak 'Licia' Oliwia", d(1, 16), d(3, 12)))
# g.append(Gopher(26, "Kasia 'Sarenka' Chojnowska", d(1, 17), d(3, 15)))
# g.append(Gopher(27, "Martyna 'Lokiana' Płatek", d(1, 12), d(3, 17)))
# g.append(Gopher(28, "Adam 'Kaszczu' Kaszczyszyn", d(1, 10), d(3, 15)))
# g.append(Gopher(29, "Justyna 'Faniel' Grudniewska", d(1, 8), d(3, 18)))
# g.append(Gopher(30, "Sierakowska 'Kaviria.Praxus' Martyna", d(1, 9), d(3, 17)))

tt = Timetable(g)

tt.add_lane("polnoc_a")
tt.mark_not_needed("polnoc_a", d(1, 0), d(1, 10))
tt.mark_not_needed("polnoc_a", d(1, 23), d(2, 9))
tt.mark_not_needed("polnoc_a", d(2, 23), d(3, 9))
tt.mark_not_needed("polnoc_a", d(3, 19))

tt.add_lane("polnoc_b")
tt.mark_not_needed("polnoc_b", d(1, 0), d(1, 10))
tt.mark_not_needed("polnoc_b", d(1, 23), d(2, 9))
tt.mark_not_needed("polnoc_b", d(2, 23), d(3, 9))
tt.mark_not_needed("polnoc_b", d(3, 19))


tt.add_lane("wschod_a")
tt.mark_not_needed("wschod_a", d(1, 0), d(1, 10))
tt.mark_not_needed("wschod_a", d(1, 23), d(2, 9))
tt.mark_not_needed("wschod_a", d(2, 23), d(3, 9))
tt.mark_not_needed("wschod_a", d(3, 19))

tt.add_lane("wschod_b")
tt.mark_not_needed("wschod_b", d(1, 0), d(1, 10))
tt.mark_not_needed("wschod_b", d(1, 23), d(2, 9))
tt.mark_not_needed("wschod_b", d(2, 23), d(3, 9))
tt.mark_not_needed("wschod_b", d(3, 19))

tt.add_lane("wschod_c")
tt.mark_not_needed("wschod_c", d(1, 0), d(1, 10))
tt.mark_not_needed("wschod_c", d(1, 23), d(2, 9))
tt.mark_not_needed("wschod_c", d(2, 23), d(3, 9))
tt.mark_not_needed("wschod_c", d(3, 19))

tt.add_lane("wschod_d")
tt.mark_not_needed("wschod_d", d(1, 0), d(1, 10))
tt.mark_not_needed("wschod_d", d(1, 23), d(2, 9))
tt.mark_not_needed("wschod_d", d(2, 23), d(3, 9))
tt.mark_not_needed("wschod_d", d(3, 19))


# tt.add_lane("czternastka_a")
# tt.mark_not_needed("czternastka_a", d(1, 0), d(1, 14))
# tt.mark_not_needed("czternastka_a", d(3, 18))

# tt.add_lane("czternastka_b")
# tt.mark_not_needed("czternastka_b", d(1, 0), d(1, 14))
# tt.mark_not_needed("czternastka_b", d(3, 18))


# tt.add_lane("pietnastka_a")
# tt.mark_not_needed("pietnastka_a", d(1, 0), d(1, 14))
# tt.mark_not_needed("pietnastka_a", d(2, 0), d(2, 9))
# tt.mark_not_needed("pietnastka_a", d(3, 0), d(3, 9))
# tt.mark_not_needed("pietnastka_a", d(3, 18))

# tt.add_lane("pietnastka_b")
# tt.mark_not_needed("pietnastka_b", d(1, 0), d(1, 14))
# tt.mark_not_needed("pietnastka_b", d(2, 0), d(2, 9))
# tt.mark_not_needed("pietnastka_b", d(3, 0), d(3, 9))
# tt.mark_not_needed("pietnastka_b", d(3, 18))

# Leci w dolnym terminalu


tt.rozstaw()