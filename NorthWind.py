import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

DATABASEPATH = "NorthWindEdit.db"
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def GetTopRevenueEmployees():
        with sqlite3.connect(DATABASEPATH) as connection:
                query = ('''
                        SELECT  FirstName || " " ||LastName as FullName,
                                SUM(Quantity) as TotalQuantitySold,
                                SUM(Quantity * Price) as TotalRevenue
                        FROM Employees

                        INNER JOIN Orders, OrderDetails, Products ON
                                Orders.EmployeeID = Employees.EmployeeID AND
                                Orders.OrderID = OrderDetails.OrderID AND
                                OrderDetails.ProductID = Products.ProductID

                        GROUP BY Employees.EmployeeID

                        ORDER BY TotalRevenue DESC
                        LIMIT 10
                        ''')

                result = pd.read_sql_query(query, connection)
        
        print(result)

        result.plot(x="FullName", y="TotalRevenue", figsize=(10,7), kind="bar", legend=False, color=COLORS)
        plt.title("Top Employees by Revenue)")
        plt.xlabel("Employees")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def GetTopRevenueProducts():
        with sqlite3.connect(DATABASEPATH) as connection:
                query = ('''
                        SELECT 	ProductName,
                                SUM(Quantity) as QuantitySold, 
                                Price as UnitPrice,
                                SUM(Quantity * Price) as TotalRevenue
                        FROM Products

                        INNER JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID

                        GROUP BY Products.ProductID

                        ORDER BY TotalRevenue DESC
                        LIMIT 10
                        ''')

                result = pd.read_sql_query(query, connection)
        
        print(result)

        result.plot(x="ProductName", y="TotalRevenue", figsize= (10,7), kind="bar", legend=False, color=COLORS)
        plt.title("Top profitable products (Based on revenue by product)")
        plt.xlabel("Product Name")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def GetRevenueClassifiedBycategories():
        with sqlite3.connect(DATABASEPATH) as connection:
                query = ('''
                        SELECT 	Categories.CategoryName,
                                SUM(OrderDetails.Quantity) as TotalQuantity,
                                SUM(OrderDetails.Quantity * Price) as TotalRevenue
                        FROM Products
                         
                        INNER JOIN OrderDetails ON OrderDetails.ProductID = Products.ProductID
                        INNER JOIN Categories ON Categories.CategoryID = Products.CategoryID
                         
                        GROUP BY Products.CategoryID
                        ORDER BY TotalRevenue DESC
                        LIMIT 5
                        ''')

                result = pd.read_sql_query(query, connection)

        print(result)

        labels=result["CategoryName"]

        total_revenue = 0
        for revenue in result["TotalRevenue"]:
                total_revenue += revenue

        sizes = []
        for revenue in result["TotalRevenue"]:
                size = revenue / total_revenue * 100
                sizes.append(size)

        explode = (0.1, 0, 0, 0, 0)
        
        def FormatLabel(percentage):
                revenue = int(percentage / 100 * total_revenue)
                return f"{percentage:.1f}%\n(${revenue:,})"

        plt.figure(figsize= (8,8))
        plt.pie(sizes, labels=labels, colors=COLORS, explode=explode, autopct=lambda percentage: FormatLabel(percentage), startangle=140, shadow=True)
        plt.title("Top profitable products (Based on revenue by product)")
        plt.tight_layout()
        plt.show()

def main():
        GetTopRevenueEmployees()
        GetTopRevenueProducts()
        GetRevenueClassifiedBycategories()

if __name__ == "__main__":
        main()