import pyodbc

##############################################################################################
#  Writes given fields to a sql database. Designed to write one row at a time.               #
#  First runs an update query, then an insert query if criteria of update query aren't met.  #
#  Script was used to connect to instance of microsoft sql database                          # 
##############################################################################################

def write_to_sql(var1 :str, var2 :str, var3 :str, var4 :str, var_date :str) -> None:
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=<SQL Server Name or IP address>\\<Database Instance>;'
                    'Database=<Database name>;'
                    'Trusted_Connection=yes;')
        cursor = conn.cursor()
        table_name = "<Your Table Name>"
        #--Update query to update rows matching the listed WHERE paramaters--#
        update_query = f"UPDATE {table_name} SET var1 = '{var1}', var2='{var2}', var_date='{var_date}' WHERE var3='{var3}' AND var4='{var4}';"
        results = cursor.execute(update_query)
        cursor.commit()

        if results.rowcount >= 1:
            #Insert desired conditions if the row does update
            ...

        #--If row doesn't update, run insert query--#
        if results.rowcount == 0:
            values = f"('{var1}', '{var2}', '{var3}', '{var4}', '{var_date}')"
            insert_query = f"INSERT INTO {table_name} (var1, var2, var3, var4, var_date) VALUES {values};"
            cursor.execute(insert_query)
            cursor.commit()
        conn.close()

    except Exception as e:
        function_name = 'write_to_sql'
        error_title = f'Exception in {script_name} {function_name}'
        error_msg = f'Exception in {function_name}: {str(e)}'
        
        #--Use logging function and email function for error notification in production--#
        write_to_appLog(error_msg)
        send_email(error_title, error_msg)
        print(f'Error: {str(e)}')