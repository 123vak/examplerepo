from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
import json
from django.core.files.storage import default_storage
import pandas as pd
from django.conf import settings
import os

def branchview(request):
    data = []
    if request.session.get('loginid'): 
        if request.method == "POST":
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                try:
                    jsonbody = json.loads(request.body)
                    branchname = jsonbody.get('branchname')
                    branchcode = jsonbody.get('branchcode')
                    connection.close()
                    with connection.cursor() as cur2:
                        cur2.callproc("Get_Branch_New", [branchname, branchcode])
                        all_results = []

                        # Loop through all result sets
                        while True:
                            # Fetch the current result set
                            result = cur2.fetchall()
                            
                            if result:
                                columns = [col[0] for col in cur2.description]  
                                rows = [dict(zip(columns, row)) for row in result]  
                                all_results.append(rows)
                            
                            # Move to the next result set, or break if there are no more
                            if not cur2.nextset():
                                break

                        print("All Results:", all_results)  # Debug: view all result sets

                        # Return the results as JSON
                        return JsonResponse({"data": all_results})

                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=500)

        # If not an AJAX request, render the HTML page
        return render(request, 'Master/branchview.html', {'data': data})
    
    else:
        return redirect('login')
    
    
def fileupload(request):
    if request.method == "POST" and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']
        filename = excel_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, filename)  # Save file in MEDIA_ROOT
        print(file_path)
        print("filename: ",filename)
        try:
            # Save the file to the system
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)
                    
            # Read the CSV file into a DataFrame
            df = pd.read_excel(file_path)
            
            # #--------------- 1 way to bulk insert ---------------
            columns = df.columns.tolist() 
            print(columns)
            table_name = 'clientdata'  
            placeholders = ', '.join(['%s'] * len(columns))  
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            data_to_insert = df.values.tolist() 
            
            # Execute the bulk insert using raw SQL
            with connection.cursor() as cursor:
                cursor.executemany(insert_query, data_to_insert)
            
            # # ----------------- other way to bulk insert in sql server ---------------
            # csv_file_path = file_path.replace('.xlsx', '.csv')
            # df.to_csv(csv_file_path, index=False)

            # # Construct the BULK INSERT query
            # table_name = 'clientdata'
            # bulk_insert_query = f"""
            #     BULK INSERT {table_name}
            #     FROM '{csv_file_path}'
            #     WITH (
            #         FIELDTERMINATOR = ',',
            #         ROWTERMINATOR = '\\n',
            #         FIRSTROW = 2  
            #     )
            # """
            # # Perform the BULK INSERT with raw SQL
            # with connection.cursor() as cursor:
            #     cursor.execute(bulk_insert_query)

            return JsonResponse({"message": "Bulk insert successful"})
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    else:
        return JsonResponse({"error": "No file provided"}, status=400)
        
    # pass
    
