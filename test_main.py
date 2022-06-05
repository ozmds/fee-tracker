import pytest
from decimal import Decimal
from main import (
    FeeGroup, get_row_data, get_row_fee, phrase_answer, get_structured_fees,
    add_row_to_fee_tree, is_depth_value_in_question, convert_question_to_query, query_structure
)
from test_data import depth_order, right_column, wrong_column, csv_data, column_order, group_names

# pytest --cov=. --cov-report term-missing -s


def test_empty_feegroup():
    node = FeeGroup()
    assert node.type == ""
    assert node.name == ""
    assert node.parent is None


def test_populated_feegroup():
    child_node = FeeGroup(type="hello", name="batman")
    parent_node = FeeGroup(name="thomas")
    parent_node.children["batman"] = child_node
    child_node.parent = parent_node
    assert child_node.type == "hello"
    assert child_node.name == "batman"
    assert child_node.parent.name == "thomas"
    assert len(parent_node.children.keys()) == 1


def test_get_row_data():
    row = ["fire", "water"]
    column_order = ["fifth", "seven"]
    row_data = get_row_data(row, column_order)
    assert row_data == {"fifth": "fire", "seven": "water"}


def test_get_row_fee():
    row_data = {"unit_price": 7.95, "quantity": 3}
    assert get_row_fee(row_data) == round(Decimal(23.85), 2)


def test_phase_answer():
    assert (
        phrase_answer(240, ["group1", ""], ["depth1", "depth2"])
        == "for depth1: group1, depth2: all, total is $240"
    )


def test_add_row_to_fee_tree():
    fee_root = FeeGroup()
    row_data = get_row_data(csv_data[1], column_order)
    fee_root, new_group_names = add_row_to_fee_tree(fee_root, row_data, 0, group_names, depth_order)
    assert new_group_names == {
        "department": ["Support"],
        "category": ["Tier 2"],
        "subcategory": ["Cat1"],
        "type": ["TypeB"]
    }
    assert fee_root.children["Support"].total == round(Decimal(25.38), 2)
    assert fee_root.children["Support"].children["Tier 2"].total == round(Decimal(25.38), 2)
    assert (
        fee_root.children["Support"].children["Tier 2"].children["Cat1"].total
        == round(Decimal(25.38), 2)
    )
    assert (
        fee_root.children["Support"].children["Tier 2"].children["Cat1"].children["TypeB"].total
        == round(Decimal(25.38), 2)
    )


def test_wrong_column_get_structured_fees():
    with pytest.raises(ValueError) as execinfo:
        get_structured_fees(csv_data, depth_order, wrong_column, column_order)
    assert "column names that don't match" in str(execinfo.value)


def test_get_structured_fees():
    fee_root, group_names = get_structured_fees(csv_data, depth_order, right_column, column_order)
    assert group_names == {
        "department": ["Support", "Development", "Sales", "Operations", "Marketing"],
        "category": [
            "Tier 2", "Quality Assurance", "Coding", "Sales Engineering", "Human Resources", "ABM"
        ],
        "subcategory": ["Cat1", "Cat2", "Cat3"],
        "type": ["TypeB", "TypeA", "TypeC"]
    }
    assert fee_root.children["Development"].total == round(Decimal(521.23), 2)
    assert fee_root.children["Development"].children["Coding"].total == round(Decimal(306.33), 2)
    assert (
        fee_root.children["Development"].children["Coding"].children["Cat1"].total
        == round(Decimal(255.15), 2)
    )
    assert (
        fee_root.children["Development"].children["Coding"].children["Cat1"].children["TypeC"].total
        == round(Decimal(255.15), 2)
    )


def test_in_question_is_depth_value_in_question():
    assert is_depth_value_in_question(["hello", "cannot", "find", "me"], 3, "cannot find") is True


def test_not_in_question_is_depth_value_in_question():
    assert is_depth_value_in_question(["hello", "cannot", "find", "me"], 2, "cannot find") is False


def test_convert_question_to_query():
    group_names = {
        "department": ["Support", "Development", "Sales", "Operations", "Marketing"],
        "category": [
            "Tier 2", "Quality Assurance", "Coding", "Sales Engineering", "Human Resources", "ABM"
        ],
        "subcategory": ["Cat1", "Cat2", "Cat3"],
        "type": ["TypeB", "TypeA", "TypeC"]
    }
    assert (
        convert_question_to_query("hello hello hello", group_names, depth_order)
        == ["", "", "", ""]
    )
    assert (
        convert_question_to_query("CODING CaTeGoRy", group_names, depth_order)
        == ["", "Coding", "", ""]
    )
    assert convert_question_to_query("TYPEC", group_names, depth_order) == ["", "", "", "TypeC"]


def test_query_structure():
    fee_root, group_names = get_structured_fees(csv_data, depth_order, right_column, column_order)
    assert query_structure(fee_root, ["", "Coding", "", ""]) == round(Decimal(306.33), 2)
