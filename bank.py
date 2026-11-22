
from db_connection import get_connection
import mysql.connector


class Bank:

    
    def __init__(self, id, name, username, password, email, bal):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.bal = bal

    
    @classmethod
    def signup(cls):

        con = None
        cur = None

        try:
            name = input("Enter your name: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            email = input("Enter your email: ")

            bal = int(input("Enter your initial balance: "))

            if bal < 0:
                raise ValueError("Balance cannot be negative.")

            con = get_connection()

            if con is None:
                return

            cur = con.cursor()

            query = """
            INSERT INTO customers
            (name, username, password, email, balance)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = (name, username, password, email, bal)

            cur.execute(query, values)
            con.commit()

            print("Registration successful!")

        except ValueError as e:
            print("Invalid input:", e)

        except mysql.connector.IntegrityError:
            print("Username already exists.")

        except mysql.connector.Error as e:
            print("Database error:", e)

        finally:
            if cur:
                cur.close()

            if con and con.is_connected():
                con.close()

    
    @classmethod
    def signin(cls):

        con = None
        cur = None

        try:
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            con = get_connection()

            if con is None:
                return

            cur = con.cursor()

            query = """
            SELECT id, name, username, password, email, balance
            FROM customers
            WHERE username = %s AND password = %s
            """

            cur.execute(query, (username, password))

            person = cur.fetchone()

            if person:

                user = cls(
                    person[0],
                    person[1],
                    person[2],
                    person[3],
                    person[4],
                    person[5]
                )

                print(f"Welcome {user.name}!")

                cur.close()
                cur = None

                con.close()
                con = None

                user.dashboard()

            else:
                print("Invalid username or password.")

        except mysql.connector.Error as e:
            print("Database error:", e)

        finally:
            if cur:
                cur.close()

            if con and con.is_connected():
                con.close()


    def deposit(self):

        con = None
        cur = None

        try:
            amount = int(input("Enter the amount to deposit: "))

            if amount <= 0:
                raise ValueError("Enter a valid amount.")

            con = get_connection()

            if con is None:
                return

            cur = con.cursor()

            query = """
            UPDATE customers
            SET balance = balance + %s
            WHERE id = %s
            """

            cur.execute(query, (amount, self.id))
            con.commit()

            if cur.rowcount > 0:
                self.bal += amount
                print("Deposit Successful")

        except ValueError as e:
            print("Invalid input:", e)

        except mysql.connector.Error as e:
            print("Database error:", e)

        finally:
            if cur:
                cur.close()

            if con and con.is_connected():
                con.close()

    
    def withdrawal(self):

        con = None
        cur = None

        try:
            amount = int(input("Enter the amount to withdraw: "))

            if amount <= 0:
                raise ValueError("Enter a valid amount.")

            con = get_connection()

            if con is None:
                return

            cur = con.cursor()

            query = """
            UPDATE customers
            SET balance = balance - %s
            WHERE id = %s AND balance >= %s
            """

            cur.execute(query, (amount, self.id, amount))
            con.commit()

            if cur.rowcount > 0:
                self.bal -= amount
                print("Withdrawal successful")
            else:
                print("Insufficient balance.")

        except ValueError as e:
            print("Invalid input:", e)

        except mysql.connector.Error as e:
            print("Database error:", e)

        finally:
            if cur:
                cur.close()

            if con and con.is_connected():
                con.close()

    
    def balance(self):

        con = None
        cur = None

        try:
            con = get_connection()

            if con is None:
                return

            cur = con.cursor()

            query = """
            SELECT balance
            FROM customers
            WHERE id = %s
            """

            cur.execute(query, (self.id,))

            result = cur.fetchone()

            if result:
                self.bal = result[0]

                print(
                    f"Your account balance is {self.bal}"
                )

            else:
                print("Account not found.")

        except mysql.connector.Error as e:
            print("Database error:", e)

        finally:
            if cur:
                cur.close()

            if con and con.is_connected():
                con.close()

    
    def dashboard(self):

        while True:

            print(f'''
            Welcome to {self.name}

            Choose your option:

            1. Deposit
            2. Withdrawal
            3. Balance
            4. Exit
            ''')

            try:
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    self.deposit()

                elif choice == 2:
                    self.withdrawal()

                elif choice == 3:
                    self.balance()

                elif choice == 4:
                    print("Thank you for using Python Bank!")
                    break

                else:
                    print("Enter a valid option.")

            except ValueError:
                print("Please enter a number.")



while True:

    print('''
    Welcome to Python Bank

    Choose your option:

    1. Sign-up
    2. Sign-in
    3. Exit
    ''')

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            Bank.signup()

        elif choice == 2:
            Bank.signin()

        elif choice == 3:
            print("Thank you for visiting Python Bank!")
            break

        else:
            print("Enter a valid option.")

    except ValueError:
        print("Please enter a number.")
