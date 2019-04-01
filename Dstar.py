#!/usr/bin/env python3
#__*__ coding: utf-8 __*__

manhattan_dis = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])

class Dstar:

    def __init__(self):
        self.open_list = []
        self.h_dict = dict()
        self.k_dict = dict()
        self.father_point = dict()
        self.close_list = []
        self.tabu_table = []
        self.route = []
        return

    def clear_history(self):
        self.open_list.clear()
        self.h_dict.clear()
        self.k_dict.clear()
        self.father_point.clear()
        self.close_list.clear()
        self.tabu_table.clear()
        self.route.clear()
        return

    def recall_route(self, strt_position, terminal_position):
        route = [strt_position]
        point_tmp = tuple(strt_position)
        while True:
            point_tmp = self.father_point[point_tmp]
            route.append(list(point_tmp))
            if point_tmp == tuple(terminal_position):
                break
            # print(point_tmp)
        self.route = route
        return

    def add_change_point(self, new_black, new_white):
        # print(new_black, new_white)
        for point in new_black:
            point_t = tuple(point)
            if self.h_dict.__contains__(point_t):
                self.h_dict[point_t] = int(1e4)
                self.open_list_insert(point_t)
                if point_t in self.close_list:
                    self.close_list = [self.close_list[idx] for idx in \
                                       range(self.close_list.index(point_t))]

        for point in new_white:
            point_t = tuple(point)
            if self.h_dict.__contains__(point_t):
                self.h_dict[point_t] = self.k_dict[point_t]
                self.open_list_insert(point_t)
                if point_t in self.close_list:
                    self.close_list = [self.close_list[idx] for idx in \
                                       range(self.close_list.index(point_t))]


        print(self.close_list)

        return

    def D_star_search(self, strt_position, terminal_position, tabu_table):
        self.tabu_table = tabu_table
        self.open_list.append(tuple(terminal_position))
        self.h_dict[tuple(terminal_position)] = 0
        while True:
            choose_point = self.open_list.pop(0) # self.open_list[0]
            # print(choose_point)
            self.close_list.append(choose_point)
            if choose_point == tuple(strt_position):
                return

            x, y = choose_point[0], choose_point[1]
            neighbour = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

            for unit in neighbour:
                # print('C', list(choose_point), 'N', list(unit), 'S', strt_position)
                if unit in self.close_list:
                    continue
                elif unit[0] > 31 or unit[0] < 0 or unit[1] > 23 or unit[1] < 0:
                    continue
                elif unit in self.open_list:
                    new_k_value = 1 + self.h_dict[choose_point]
                    if self.father_point[unit] == choose_point:
                        self.k_dict[unit] = new_k_value
                        self.h_dict[unit] = int(1e4) if list(unit) in self.tabu_table \
                            else self.k_dict[unit]
                        self.father_point[unit] = choose_point
                        self.open_list.remove(unit)
                        self.open_list_insert(unit)

                    elif new_k_value < self.k_dict[unit]:
                        self.k_dict[unit] = new_k_value
                        self.h_dict[unit] = int(1e4) if list(unit) in self.tabu_table \
                            else self.k_dict[unit]
                        self.father_point[unit] = choose_point
                        self.open_list.remove(unit)
                        self.open_list_insert(unit)

                else:
                    # print(unit, choose_point)
                    # print(self.h_dict[choose_point])
                    k_value = 1 + self.h_dict[choose_point]
                    self.k_dict[unit] = k_value
                    self.h_dict[unit] = int(1e4) if list(unit) in self.tabu_table \
                        else self.k_dict[unit]
                    self.father_point[unit] = choose_point
                    self.open_list_insert(unit)

                # print(self.open_list)


    def open_list_insert(self, new_unit):
        idx = 0
        for idx in range(len(self.open_list)):
            unit = self.open_list[idx]
            # print(unit, self.k_dict[unit])
            if self.h_dict[new_unit] < self.h_dict[unit]:
                break
        self.open_list.insert(idx, new_unit)

    def __route__(self):
        return self.route










        return
