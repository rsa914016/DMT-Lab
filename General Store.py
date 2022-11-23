from itertools import chain
import pymysql as ps
import tabulate as tb

orders = []
db_config = {'host': 'localhost', 'port': 3306, 'user': 'root',
             'password': 'meajay24062003', 'db': 'mybase'}


def ShowProducts():
    try:
        cn = ps.connect(**db_config)
        Table, cmd1, cmd2 = [], cn.cursor(), cn.cursor()

        query1 = '''select * from products'''
        query2 = '''select column_name
                        from information_schema.columns
                        where table_name=\'products\'
                        order by ordinal_position'''

        cmd1.execute(query1), cmd2.execute(query2)
        rows, vals = cmd1.fetchall(), cmd2.fetchall()
        header = list(chain.from_iterable(vals))

        for row in rows:
            val = []
            for col in row:
                val.append(col)
            Table.append(val)
        print(tb.tabulate(Table, header, tablefmt='psql'))
        cn.commit(), cn.close()

    except Exception as e:
        print(e)


def SearchById(val):
    try:
        cn = ps.connect(**db_config)
        cmd = cn.cursor()
        query = f'''select * from products where Id=\'{val}\''''
        cmd.execute(query)
        rows = cmd.fetchone()
        cn.commit(), cn.close()

        if rows:
            return True
        return False

    except Exception as e:
        print(e)


def SearchByName(val):
    try:
        cn = ps.connect(**db_config)
        cmd = cn.cursor()
        query = f'''select * from products where Name=\'{val}\''''
        cmd.execute(query)
        rows = cmd.fetchone()
        cn.commit(), cn.close()

        if rows:
            return True
        return False

    except Exception as e:
        print(e)


def Sale():
    global orders
    val = input('Enter The Name U Want To Buy ? ')

    try:
        cn = ps.connect(**db_config)
        cmd1, cmd2, cmd3 = cn.cursor(), cn.cursor(), cn.cursor()
        query1 = f'''select Id,Name,Rate from products where Name=\'{val}\''''
        query2 = f'''select Rate from products where Name=\'{val}\''''
        query3 = f'''select Stock from products where Name=\'{val}\''''
        cmd1.execute(query1), cmd2.execute(query2), cmd3.execute(query3)
        rows, rate, stock = cmd1.fetchone(), cmd2.fetchone(), cmd3.fetchone()

        if rows:
            quantity = int(input('Enter the Quantity U Need ? '))
        else:
            print('Sorry Sir! We Don\'t Have This Product')
            return 0

        if rows and quantity > stock[0]:
            print('Sorry Sir! We Don\'t Have Enough Stock')
            return 0

        elif rows:
            amount = quantity * rate[0]
            rows = rows + (quantity, amount)
            orders.append(rows)
            cmd4 = cn.cursor()
            query4 = f'''update products set Stock=
                    {stock[0] - quantity} where Name=\'{val}\''''
            cmd4.execute(query4)
            cn.commit(), cn.close()
            return amount

    except Exception as e:
        print(e)
        return 0


def Add_Stock(val, name):
    try:
        cn = ps.connect(**db_config)
        cmd1, cmd2 = cn.cursor(), cn.cursor()
        if SearchByName(name):
            query1 = f'''select Stock from products where Name=\'{name}\''''
            cmd1.execute(query1)
            stock = cmd1.fetchone()
            val = val + stock[0]
            query2 = f'''update products set Stock={val} where Name=\'{name}\''''
            cmd2.execute(query2)
            cn.commit(), cn.close()
        else:
            print('Sorry Sir! We Don\'t Have This Product To Add Stock')

    except Exception as e:
        print(e)


Total_Amount = 0
print('--------Main Menu--------')
print(' 1. Show products', '\n', '2. Search By Id')
print(' 3. Search By Name', '\n', '4. Buy')
print(' 5. Add Stock', '\n', '6. Exit')

while True:
    ch = int(input('Enter Your Choice ? '))

    if ch == 1:
        ShowProducts()
    elif ch == 2:
        key = input('Enter The Id U Want To Search ? ')
        if SearchById(key):
            print('Yes Sir! We Have Product With This Id')
        else:
            print('Sorry Sir! We Don\'t Have This Product')
    elif ch == 3:
        key = input('Enter The Name U Want To Search ? ')
        if SearchByName(key):
            print('Yes Sir! We Have Product With This Name')
        else:
            print('Sorry Sir! We Don\'t Have This Product')
    elif ch == 4:
        Total_Amount += Sale()
    elif ch == 5:
        key = input('Enter The Name U Want To Add Stock ? ')
        if SearchByName(key):
            qty = int(input('Enter The Quantity ? '))
            Add_Stock(qty, key)
        else:
            print('Sorry Sir! We Don\'t Have This Product To Add Stock')
    elif ch == 6:
        break
    else:
        print('Invalid Choice ! Choose in (1 to 5)')


def main():
    global Total_Amount, orders
    print('Thank you sir for shopping with us')
    print('Your Receipt : ')
    header = ['ID', 'NAME', 'RATE', 'QUANTITY', 'AMOUNT']
    orders.append(['Total Amount ', '', '', '', Total_Amount])
    print(tb.tabulate(orders, header, tablefmt='psql'))


if __name__ == '__main__':
    main()
