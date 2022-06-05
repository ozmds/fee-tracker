expected_column = [
    "\ufeffId",
    "Name",
    "Description__c",
    "Department__c",
    "Category__c",
    "Sub_Category__c",
    "Type__c",
    "Quantity__c",
    "Unit_Price__c",
]

column_order = [
    "id",
    "name",
    "description",
    "department",
    "category",
    "subcategory",
    "type",
    "quantity",
    "unit_price",
]

depth_order = ["department", "category", "subcategory", "type"]

dept_surcharge = {
    "marketing": 0.10,
    "sales": 0.15,
    "development": 0.20,
    "operations": -0.15,
    "support": -0.05,
}
