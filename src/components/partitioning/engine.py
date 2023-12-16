VERTICAL = 1
HORIZONTAL = 0

TYPE = 3
VALUE = 4

POSITIVE = 5
NEGATIVE = 6

REMOVED = 7
LINES = 8
#
#
# class PartitionEngine_2:
#     @property
#     def dataset(self):
#         return self.master.dataset
#
#     @property
#     def endo(self):
#         return self.class_column
#
#     def __init__(self, master, class_x, class_y, class_column):
#         self.master = master
#         self.lines_log = []
#         self.subset = None
#         self.class_column = class_column
#         self.class_x = class_x
#         self.class_y = class_y
#         self.egzo = (class_x, class_y)
#         self.statistics = {
#             REMOVED: 0
#         }
#
#     def initialize_subset(self):
#         if self.subset is not None:
#             return
#         self.subset = self.dataset[[self.class_x, self.class_y, self.class_column]].to_dict(orient="list")
#         for c in self.egzo:
#             self.subset[c] = list(map(float, self.subset[c]))
#         # {'Aktywa': ['2.8', '3.4', ], 'Przych': ['3.2', '6.4',], 'Hrabstwo': ['ROGERS', 'HIGHLAND',]}
#
#     def new_line(self):
#         self.initialize_subset()
#
#         return self._calculate_best_new_line()
#
#     def _calculate_best_new_line(self):
#
#         fits = [(i, self._find_best_fit(c)) for i, c in zip([HORIZONTAL, VERTICAL], self.egzo)]
#         filtered_non_zero = list(filter(lambda x: x[1][1] > 0, fits))
#         if len(filtered_non_zero) == 0:
#             raise NotImplementedError("Not found any, need to remove one")
#         maximum_counter = max(map(lambda x: x[1][1], fits))
#         best = next(filter(lambda x: x[1][1] == maximum_counter, fits))
#
#         self._remove_objects_from_subset(best[1][2])
#
#         return {
#             TYPE: best[0],
#             VALUE: best[1][0],
#         }
#
#     def _remove_objects_from_subset(self, indexes):
#         indexes = set(indexes)
#         for c in [*self.egzo, self.endo]:
#             temp = []
#             for i, v in enumerate(self.subset[c]):
#                 if i not in indexes:
#                     temp.append(v)
#             self.subset[c] = temp
#
#     def _find_best_fit(self, egzo_col):
#         data = self.subset[egzo_col]
#         classes = self.subset[self.endo]
#
#         zipped_data_classes_sorted_asc = sorted(list(zip(data, classes, range(len(classes)))), key=lambda x: x[0])
#
#         best_from_left = self._best_from_left_side(zipped_data_classes_sorted_asc)
#         best_from_right = self._best_from_left_side(reversed(zipped_data_classes_sorted_asc))
#
#         if best_from_left[1] > best_from_right[1]:
#             return best_from_left
#         if best_from_left[1] <= best_from_right[1] and best_from_right[1] != 0:
#             return best_from_right
#         else:
#             raise NotImplementedError("HEHEH NOT YET")
#
#     def _best_from_left_side(self, zipped_data_classes):
#         first = None
#         last = None
#         counter = 1
#         to_be_removed = []
#         for val, cl, index in zipped_data_classes:
#
#             if first is None:  # inicjalizacja
#                 first = cl
#                 last = val
#                 to_be_removed.append(index)
#                 continue
#
#             if cl == first:  # mają takie same klasy, można dalej ciąć w prawo
#                 last = val
#                 to_be_removed.append(index)
#                 counter += 1
#             else:  # różnią się klasami
#                 if last == val:
#                     # raise NotImplementedError("same values, need to remove one point")
#                     pass
#                 return ((val + last) / 2, counter, to_be_removed)
#
#
# class PartitionEngine_3:
#     @property
#     def dataset(self):
#         return self.master.dataset
#
#     @property
#     def endo(self):
#         return self.class_column
#
#     def __init__(self, master, egzo_columns, class_column):
#         self.master = master
#         self.lines_log = []
#         self.subset = None
#         self.class_column = class_column
#         self.egzo = egzo_columns
#         self.statistics = {
#             REMOVED: 0,
#             LINES: 0,
#         }
#
#     def initialize_subset(self):
#         if self.subset is not None:
#             return
#         self.subset = self.dataset[[self.egzo + [self.class_column]]].to_dict(orient="list")
#         for c in self.egzo:
#             self.subset[c] = list(map(float, self.subset[c]))
#         # {'Aktywa': ['2.8', '3.4', ], 'Przych': ['3.2', '6.4',], 'Hrabstwo': ['ROGERS', 'HIGHLAND',]}
#
#     def new_line(self):
#         self.initialize_subset()
#
#         return self._calculate_best_new_line()
#
#     def _calculate_best_new_line(self):
#
#         fits = [(i, self._find_best_fit(c)) for i, c in enumerate(self.egzo)]
#         filtered_non_zero = list(filter(lambda x: x[1][1] > 0, fits))
#         if len(filtered_non_zero) == 0:
#             raise NotImplementedError("Not found any, need to remove one")
#         maximum_counter = max(map(lambda x: x[1][1], fits))
#         best = next(filter(lambda x: x[1][1] == maximum_counter, fits))
#
#         self._remove_objects_from_subset(best[1][2])
#         self.lines_log.append(best)
#
#         return {
#             TYPE: best[0],
#             VALUE: best[1][0],
#         }
#
#     def _remove_objects_from_subset(self, indexes):
#         indexes = set(indexes)
#         for c in [*self.egzo, self.endo]:
#             temp = []
#             for i, v in enumerate(self.subset[c]):
#                 if i not in indexes:
#                     temp.append(v)
#             self.subset[c] = temp
#
#     def _find_best_fit(self, egzo_col):
#         data = self.subset[egzo_col]
#         classes = self.subset[self.endo]
#
#         zipped_data_classes_sorted_asc = sorted(list(zip(data, classes, range(len(classes)))), key=lambda x: x[0])
#
#         best_from_left = self._best_from_left_side(zipped_data_classes_sorted_asc)
#         best_from_right = self._best_from_left_side(reversed(zipped_data_classes_sorted_asc))
#
#         if best_from_left[1] > best_from_right[1]:
#             return best_from_left
#         if best_from_left[1] <= best_from_right[1] and best_from_right[1] != 0:
#             return best_from_right
#         else:
#             raise NotImplementedError("HEHEH NOT YET")
#
#     def _best_from_left_side(self, zipped_data_classes,):
#         first = None
#         last = None
#         counter = 1
#         to_be_removed = []
#         for val, cl, index in zipped_data_classes:
#
#             if first is None:  # inicjalizacja
#                 first = cl
#                 last = val
#                 to_be_removed.append(index)
#                 continue
#
#             if cl == first:  # mają takie same klasy, można dalej ciąć w prawo
#                 last = val
#                 to_be_removed.append(index)
#                 counter += 1
#             else:  # różnią się klasami
#                 if last == val: # todo zmiana na sprawdzanie kolizji na wszystkich zmiennych
#                     # raise NotImplementedError("same values, need to remove one point")
#                     self.points_colliding.append(index)
#                     pass
#                 return ((val + last) / 2, counter, to_be_removed)


class PartitionEngine_4:
    @property
    def dataset(self):
        return self.master.dataset

    @property
    def endo(self):
        return self.class_column

    def __init__(self, master, egzo_columns, class_column):
        self.master = master
        self.lines_log = []
        self.subset = None
        self.class_column = class_column
        self.egzo = egzo_columns
        self.points_colliding = []
        self.statistics = {
            REMOVED: 0,
            LINES: 0,
        }

    def initialize_subset(self):
        if self.subset is not None:
            return
        self.subset = self.dataset[self.egzo + [self.class_column]].to_dict(orient="list")
        for c in self.egzo:
            self.subset[c] = list(map(float, self.subset[c]))
        # {'Aktywa': ['2.8', '3.4', ], 'Przych': ['3.2', '6.4',], 'Hrabstwo': ['ROGERS', 'HIGHLAND',]}

    def new_line(self):
        self.initialize_subset()

        return self._calculate_best_new_line()

    def _calculate_best_new_line(self):

        fits = [(i, self._find_best_fit(c)) for i, c in enumerate(self.egzo)]
        filtered_non_zero = list(filter(lambda x: x[1] is not None and x[1][1] > 0, fits))
        if len(filtered_non_zero) == 0:
            raise NotImplementedError("Not found any, need to remove one")
        maximum_counter = max(map(lambda x: x[1][1], fits))
        best = next(filter(lambda x: x[1][1] == maximum_counter, fits))

        self._remove_objects_from_subset(best[1][2])
        self.lines_log.append(best)

        return {
            TYPE: best[0],
            VALUE: best[1][0],
        }

    def _remove_objects_from_subset(self, indexes):
        indexes = set(indexes)
        for c in [*self.egzo, self.endo]:
            temp = []
            for i, v in enumerate(self.subset[c]):
                if i not in indexes:
                    temp.append(v)
            self.subset[c] = temp

    def _find_best_fit(self, egzo_col):
        data = self.subset[egzo_col]
        other_data = [self.subset[c] for c in self.egzo if c != egzo_col]
        classes = self.subset[self.endo]

        zipped_data_classes_sorted_asc = list(sorted((zip(data, classes, range(len(classes)),zip(*other_data))), key=lambda x: x[0]))

        best_from_left = self._best_from_left_side(zipped_data_classes_sorted_asc)
        best_from_right = self._best_from_left_side(reversed(zipped_data_classes_sorted_asc))

        if best_from_left is None and best_from_right is not None:
            return best_from_right

        if best_from_left is not None and best_from_right is None:
            return best_from_left

        if best_from_left is None and best_from_right is None:
            return None

        if best_from_left[1] > best_from_right[1]:
            return best_from_left
        if best_from_left[1] <= best_from_right[1] and best_from_right[1] != 0:
            return best_from_right
        else:
            raise NotImplementedError("HEHEH NOT YET")

    def _best_from_left_side(self, zipped_data_classes,):
        first = None
        last = None
        counter = 1
        to_be_removed = []
        points_colliding = []
        for val, cl, index,other_data in zipped_data_classes:

            if first is None:  # inicjalizacja
                first = cl
                last = val
                to_be_removed.append(index)
                continue

            if cl == first:  # mają takie same klasy, można dalej ciąć w prawo
                last = val
                to_be_removed.append(index)
                counter += 1
            else:  # różnią się klasami
                if last == val: # todo zmiana na sprawdzanie kolizji na wszystkich zmiennych
                    # raise NotImplementedError("same values, need to remove one point")
                    # self.points_colliding.append(index)
                    points_colliding.append(index)
                    continue
                    pass
                return ((val + last) / 2, counter, to_be_removed,points_colliding)
