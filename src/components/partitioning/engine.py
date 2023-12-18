VERTICAL = 1
HORIZONTAL = 0

TYPE = 3
VALUE = 4

POSITIVE = 5
NEGATIVE = 6

REMOVED = 7
LINES = 8

STATUS = 10
DATA = 11

UNKNOWN = 12

DELETED = 13
SELECTED = 14
CLASS = 15


class PartitionEngine:
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
        self.data_columns = None
        self.statistics = {
            REMOVED: 0,
            LINES: 0,
        }

    def initialize_subset(self):
        if self.subset is not None:
            return
        split = self.dataset[self.egzo + [self.class_column]].to_dict(orient="split")
        should_convert_to_float = [c in self.egzo for c in split['columns']]
        self.data_columns = split['columns']
        self.data_columns_mapping = {name: i
                                     for i, name in enumerate(self.data_columns)}
        self.subset = [
            [
                float(d) if should_convert_to_float[i] else d
                for i, d in enumerate(record)
            ]
            for record in split['data']]

    def new_line(self):
        self.initialize_subset()

        return self._calculate_best_new_line()

    def _calculate_best_new_line(self):
        if self._all_objects_are_in_the_same_class():
            return None

        endo_index = self.data_columns_mapping[self.endo]
        results = []
        for variable_name in self.egzo:
            variable_index = self.data_columns_mapping[variable_name]

            # sortuje elementy po kluczu tej zmiennej po ktorej sie iteruje
            sorted_records = sorted(self.subset, key=lambda x: x[variable_index])

            grouped_by_variable_value = self.group_records_to_multi_map(sorted_records, variable_index)

            collected_left, current_class_left, last_value_left, deleted_left = self.get_left_line(endo_index,
                                                                                                   grouped_by_variable_value,
                                                                                                   variable_index)

            collected_right, current_class_right, last_value_right, deleted_right = self.get_left_line(endo_index,
                                                                                                       reversed(
                                                                                                           grouped_by_variable_value),
                                                                                                       variable_index)
            vector = self.get_better_result(collected_left, current_class_left,
                                            last_value_left, deleted_left, True,
                                            collected_right, current_class_right,
                                            last_value_right, deleted_right, False)
            results.append([variable_name, vector])

        best_of_the_best = [None] * 5
        name = None
        for v_name, v in results:
            if not self.should_choose_left(*best_of_the_best, *v):
                best_of_the_best = v
                name = v_name

        orientation = self.get_orientation(name)

        if best_of_the_best is not None:
            selected = best_of_the_best[0]
            deleted = best_of_the_best[3]

            future_subset = self.subset

            if deleted is not None:
                future_subset = filter(lambda x: x not in deleted, self.subset)

            self.subset = list(filter(lambda x: x not in selected, future_subset))

            return {
                TYPE: orientation,
                SELECTED: best_of_the_best[0],
                CLASS: best_of_the_best[1],
                VALUE: best_of_the_best[2],
                DELETED: best_of_the_best[3]
            }
        else:
            raise NotImplementedError("Dodanie braku generowania krawędzi")

    def get_left_line(self, endo_index, grouped_by_variable_value, variable_index):
        collected_left = []
        last_value_left = None
        current_class = None
        deleted = None
        for records_list in grouped_by_variable_value:

            all_records_in_group_has_the_same_value = len(set(map(lambda x: x[endo_index], records_list))) == 1

            if current_class is None:
                current_class = records_list[0][endo_index]

            if all_records_in_group_has_the_same_value:
                if current_class == records_list[0][endo_index]:

                    last_value_left = records_list[0][variable_index]
                    collected_left = collected_left + records_list
                    continue
                else:
                    last_value_left = last_value_left + records_list[0][variable_index]
                    last_value_left /= 2
                    break

            else:
                if last_value_left is not None:
                    last_value_left = last_value_left + records_list[0][variable_index]
                    last_value_left /= 2
                else:
                    if current_class is None:
                        max_occurance_of_class = {
                            c: sum(cl[endo_index] == c
                                   for cl in records_list
                                   )
                            for c in set(map(lambda x: x[endo_index], records_list))
                        }
                        m = max(max_occurance_of_class.values())
                        for c, no in max_occurance_of_class.items():
                            if no == m:
                                current_class = c

                    deleted = list(filter(lambda x: x[endo_index] != current_class, records_list))
                    last_value_left = records_list[0][variable_index]
                    collected_left = collected_left + list(
                        filter(lambda x: x[endo_index] == current_class, records_list)
                    )
                    continue
                break
        return collected_left, current_class, last_value_left, deleted

    def group_records_to_multi_map(self, sorted_records, variable_index):
        grouped_by_variable_value = []
        grouped_by_variable_value_key_set = set()
        for record in sorted_records:
            record_variable_value = record[variable_index]

            if record_variable_value not in grouped_by_variable_value_key_set:
                temp_list = []
                grouped_by_variable_value.append(temp_list)
                grouped_by_variable_value_key_set.add(record_variable_value)
            else:
                temp_list = grouped_by_variable_value[-1]

            temp_list.append(record)
        return grouped_by_variable_value

    def get_better_result(self, collected_left, current_class_left, last_value_left, deleted_left,
                          direction_to_lower_left,
                          collected_right, current_class_right, last_value_right,
                          deleted_right, direction_to_lower_right, ):
        left_set = [collected_left, current_class_left, last_value_left, deleted_left, direction_to_lower_left]
        right_set = [collected_right, current_class_right, last_value_right, deleted_right, direction_to_lower_right]

        if self.should_choose_left(collected_left, current_class_left, last_value_left, deleted_left,
                                   direction_to_lower_left,
                                   collected_right, current_class_right, last_value_right, deleted_right,
                                   direction_to_lower_right):
            return left_set
        return right_set

    def should_choose_left(self, collected_left, current_class_left, last_value_left, deleted_left,
                           direction_to_lower_left, collected_right,
                           current_class_right, last_value_right, deleted_right, direction_to_lower_right):

        if last_value_left is None:
            return False

        if last_value_right is None:
            return True

        if deleted_right is not None and deleted_left is None:
            return True

        if deleted_right is None and deleted_left is not None:
            return False
        if deleted_left is not None and deleted_right is not None:

            dl_left = len(deleted_left)
            dl_right = len(deleted_right)

            if dl_left > dl_right:
                return False

            if dl_right > dl_left:
                return True

        cl_right = len(collected_right)
        cl_left = len(collected_left)

        if cl_right > cl_left:
            return False
        else:
            return True

    def get_orientation(self, name):
        return self.data_columns_mapping[name]

    def _all_objects_are_in_the_same_class(self):
        s = set(map(lambda x: x[self.data_columns_mapping[self.endo]], self.subset))
        return len(s) == 1


class PartitionEngineWithEncoding(PartitionEngine):
    def __init__(self, master, egzo_columns, class_column):
        super().__init__(master, egzo_columns, class_column)

