import sys
import csv
from decimal import Decimal
from settings import expected_column, column_order, depth_order, dept_surcharge


def read_csv(file_path):
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


class FeeGroup:
    def __init__(self, type="", name="", parent=None):
        self.type = type
        self.name = name
        self.parent = parent
        self.children = {}
        self.total = 0


def get_row_data(row, column_order):
    row_data = {}
    for index, cell_value in enumerate(row):
        row_data[column_order[index]] = cell_value
    return row_data


def get_row_fee(row_data):
    return round(Decimal((row_data["unit_price"])) * int(row_data["quantity"]), 2)


def add_row_to_fee_tree(node, row_data, index, group_names, depth_order):
    row_fee = get_row_fee(row_data)
    node.total += row_fee
    if index < len(depth_order):
        group_name = row_data[depth_order[index]]
        if group_name not in node.children.keys():
            new_child = FeeGroup(type=depth_order[index], name=group_name, parent=node)
            node.children[group_name] = new_child
            if group_name not in group_names[depth_order[index]]:
                group_names[depth_order[index]].append(group_name)
        add_row_to_fee_tree(
            node.children[group_name], row_data, index + 1, group_names, depth_order
        )
    return node, group_names


def get_structured_fees(csv_data, depth_order, expected_column, column_order):
    if csv_data[0] != expected_column:
        raise ValueError("csv has column names that don't match expected values")
    fee_root = FeeGroup()
    group_names = {}
    for key in depth_order:
        group_names[key] = []
    for row in csv_data[1:]:
        row_data = get_row_data(row, column_order)
        fee_root, group_names = add_row_to_fee_tree(fee_root, row_data, 0, group_names, depth_order)
    return fee_root, group_names


def is_depth_value_in_question(question_words, index, possible_group):
    possible_group_split = possible_group.lower().split()
    for word_index, word in enumerate(possible_group_split):
        if word != question_words[index - len(possible_group_split) + word_index]:
            return False
    return True


def convert_question_to_query(question, group_names, depth_order):
    query = []
    question_words = question.lower().split()
    for level in depth_order:
        next_match = ""
        possible_match = ""
        for possible_group in group_names[level]:
            if level in question_words:
                index = question_words.index(level)
                if is_depth_value_in_question(question_words, index, possible_group):
                    next_match = possible_group
                    break
            if possible_group.lower() in question.lower():
                possible_match = possible_group
        if not next_match and possible_match:
            next_match = possible_match
        query.append(next_match)
    return query


def query_structure(node, query):
    if not any(query):
        return node.total
    if query[0]:
        if query[0] in node.children.keys():
            return query_structure(node.children[query[0]], query[1:])
        return 0
    total = 0
    for child in node.children.keys():
        total += query_structure(node.children[child], query[1:])
    return total


def phrase_answer(total, query, depth_order):
    answer = "for "
    for index, depth in enumerate(depth_order):
        if query[index]:
            answer += f"{depth}: {query[index]}, "
        else:
            answer += f"{depth}: all, "
    answer += f"total is ${total}"
    return answer


def question_loop(root, group_names, depth_order, dept_surcharge):
    while True:
        question = input("Please ask any question about total fees:")
        query = convert_question_to_query(question, group_names, depth_order)
        total = query_structure(root, query)
        if query[0].lower() in dept_surcharge.keys():
            total = round(total * Decimal(1 + dept_surcharge[query[0].lower()]), 2)
        print(phrase_answer(total, query, depth_order))


if __name__ == "__main__":
    csv_path = sys.argv[1]
    csv_data = read_csv(csv_path)
    root, group_names = get_structured_fees(csv_data, depth_order, expected_column, column_order)
    question_loop(root, group_names, depth_order, dept_surcharge)
