depth_order = ["department", "category", "subcategory", "type"]

right_column = [
    "Department__c",
    "Category__c",
    "Sub_Category__c",
    "Type__c",
    "Quantity__c",
    "Unit_Price__c",
]

wrong_column = [
    "wrong_Department__c",
    "Category__c",
    "Sub_Category__c",
    "Type__c",
    "Quantity__c",
    "Unit_Price__c",
]

column_order = [
    "department",
    "category",
    "subcategory",
    "type",
    "quantity",
    "unit_price",
]

csv_data = [
    ["Department__c", "Category__c", "Sub_Category__c", "Type__c", "Quantity__c", "Unit_Price__c"],
    ["Support", "Tier 2", "Cat1", "TypeB", 9, 2.82],
    ["Development", "Quality Assurance", "Cat1", "TypeA", 3, 39.29],
    ["Development", "Quality Assurance", "Cat2", "TypeA", 1, 97.03],
    ["Development", "Coding", "Cat1", "TypeC", 9, 28.35],
    ["Sales", "Sales Engineering", "Cat2", "TypeB", 8, 95.96],
    ["Operations", "Human Resources", "Cat1", "TypeC", 8, 38.74],
    ["Marketing", "ABM", "Cat3", "TypeA", 9, 56.1],
    ["Operations", "Human Resources", "Cat3", "TypeC", 3, 35.5],
    ["Development", "Coding", "Cat2", "TypeB", 6, 8.53],
    ["Marketing", "ABM", "Cat3", "TypeA", 9, 68.69]
]

group_names = {}
for key in depth_order:
    group_names[key] = []
