import sys
from User.User_Interface import user
from crawler.dispatcher import selectWeb

def main():
    u = user()

    user_data = u.get_info()

    print("=== web1 test ===")
    result = selectWeb("constellation", [user_data[Birth_year],user_data[Birth_month],user_data[Birth_day]])
    print(result)

    print("=== web2 test ===")
    result = selectWeb("name", [user_data[Last_name],user_data[First_name]])
    print(result)

if __name__() == "__main__":
    main()