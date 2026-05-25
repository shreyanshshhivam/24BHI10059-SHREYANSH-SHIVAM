# 24BHI10059_MongoDB-Task-2
# MongoDB Solutions and Outputs

This repository/document contains MongoDB aggregation and query solutions for the given database schema consisting of:

- Employees
- Departments
- Projects
- Assignments

Each question includes:

- MongoDB query/code
- Expected output

## Covered Topics

### Basic Queries
1. Employee name, department, and location
2. Project details with total hours
3. Employees working for a specific client
4. Departments without employees
5. Managers and direct reports

### Aggregation and Grouping
6. Average hours worked per employee
7. Departments with above-average salary
8. Clients with combined project hours > 500
9. Highest employee count by location
10. Projects with more than 5 employees

### Advanced Filtering
11. Employees working on all R&D projects
12. Departments with employees on multiple projects
13. Employees working less than 10 hours
14. Projects without assigned employees
15. Employees exceeding department salary maximum

### Date and Conditional Queries
16. Oldest project assignment date
17. Projects active in 2023
18. IFNULL equivalent using `$ifNull`
19. Top 3 departments by total hours
20. Project activity status using `$cond`

### Complex Queries
21. Employee and manager relationship mapping
22. Unique employee count per project
23. Employees assigned to the same projects as Employee 101

## File Included

- `24BHI10059_MONGODBTASK2`
  - Contains MongoDB code and corresponding outputs.

## Technologies Used

- MongoDB
- Aggregation Framework
- Lookup Operations
- Grouping and Filtering
- Conditional Operators

## Notes

- Outputs are based on the sample data provided in the assignment.
- MongoDB aggregation pipelines are used wherever joins or grouping operations are required.
- Some outputs may return empty arrays if no matching records exist in the dataset.
