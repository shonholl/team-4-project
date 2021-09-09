import connection
import pandas as pd


def payments(data):

    connection = conn.connection()
    cursor = connection.cursor()

    cafe_data = pd.DataFrame(data)

    orders = pd.read_sql_query("SELECT * FROM orders;", connection)
    payments = pd.read_sql_query("SELECT payment_id FROM payments;", connection)

    values = []

    merged_data = pd.merge(cafe_data, orders, on="order_timestamp")
    merged_dict = merged_data.to_dict('records')

    for each in merged_dict:
        if each["order_id"] not in payments.values:
            values.append(f"('{each['order_id']}', '{each['payment_method']}', '{each['card_type']}', '{each['payment_total']}')")
            
    if values:
        cursor.execute(f"INSERT INTO payments (payment_id, payment_method, card_type, payment_total) VALUES {' ,'.join(values)};")
        connection.commit()
    cursor.close()
    connection.close()
    