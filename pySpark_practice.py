from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType


# In this file I'm just playing with different aspects of PySpark to get a better understanding of how it works.
# It's not really trying to do anything. Just a sandbox. 

# Create a spark session
my_spark = SparkSession.builder.appName("my_spark").getOrCreate()

# Switch to do different sets of operations
dataType = "csv_with_header" 
    # csv_with_header - Get some data, do some calculations
    # csv_no_header  - Get data, define a header, do some cleaning, add some columns, run spark SQL queries against it, crunch in Pandas Dataframe. Make RDD.
    # json - Pull in some JSON data, do some filtering
    # dataframe - 

if dataType == "csv_with_header": 

    # Load a CSV file into a DataFrame
    salaries_df =spark.read.csv("salaries.csv", header=True, inferSchema=True)

    # Count the total number of rows
    row_count = salaries_df.count()
    print(f"Total rows: {row_count}")

    # Group by and calculate the sum of sales
    salaries_df.groupBy("company_size").agg({"salary_in_usd": "avg"}).show()
    salaries_df.show()

    # Average salary for entry level in Canada
    CA_jobs = salaries_df.filter(salaries_df["company_location"] == "CA").filter(ca_salaries_df['experience_level'] == "Entry Level").groupBy().avg("salary_in_usd")

    # Show the result
    CA_jobs.show()


elif dataType == "csv_no_header":

    # Define the schema explicitly
    schema = StructType([StructField("age",IntegerType()),
                        StructField("education_num",IntegerType()),
                        StructField("marital_status",StringType()),
                        StructField("occupation",StringType()),
                        StructField("income",StringType()),
                        ])

    # Read in the CSV, using the schema defined above
    salaries_df = spark.read.csv("adult_reduced_100.csv", sep=',', header=False, schema=schema)

    # Print out the schema
    salaries_df.printSchema()

    # Drop rows with null values
    salaries_df_cleaned = salaries_df.na.drop()

    # Sort by salary in descending order
    salaries_sorted = salaries_df_cleaned.sort("salary", ascending=False)

    # Create a new column 'weekly_salary'
    salaries_sorted_weekly = salaries_sorted.withColumn("weekly_salary", salaries_sorted["income"]/52)

    # Rename the 'age' column to 'years'
    salaries_sorted_weekly = salaries_sorted_weekly.withColumnRenamed("age", "years")

    # Show the result
    salaries_sorted_weekly.show()

    # Create a temporary queryable view of salaries_table
    salaries_sorted_weekly.createOrReplaceTempView('salaries_table')

    # Construct a "query"
    query = '''SELECT job_title, salary_in_usd FROM salaries_table WHERE company_location == "CA"'''

    # Apply the SQL "query"
    canada_titles = spark.sql(query)

    # Generate basic statistics
    canada_titles.describe().show()

    # New Query
    query = ''' SELECT * FROM salaries_table WHERE marital_status = "Married" '''
    married_adults = spark.sql(query)

    # Convert the results to a pandas DataFrame
    pd_married = married_adults.toPandas()
    print(pd_married.head())

    # Define a Pandas UDF that adds 10 to each element in a vectorized way
    @pandas_udf(DoubleType())
    def add_ten_pandas(column):
        return column + 10

    pd_married_in_ten = pd_married.withColumn("age_in_10Y", add_ten_pandas(pd_married["age"]))
    print(pd_married_in_ten.head())

    # Create an RDD from the df_salaries
    rdd_salaries = salaries_df.rdd

    # Collect and print the results
    print(rdd_salaries.collect())

    # Group by experience level and calculate the average salary and show the results
    dataframe_results = salaries_df.select("experience_level", "salary_in_usd").agg({"salary_in_usd": 'max'})

    dataframe_results.show()


elif dataType == "json": 
    # Load dataframe
    census_df = spark.read.json("adults.json")

    # Filter rows based on salary condition
    salary_filtered_census = census_df.filter(census_df['age']>40)

    # Show the result
    salary_filtered_census.show()


elif dataType == "dataframe": 

    # Create Dataframe
    data = [("HR", "3000"), ("IT", "4000"), ("Finance", "3500")]
    columns = ["Department", "Salary"]
    df = spark.createDataFrame(data, schema=columns)

    # Map the DataFrame to an RDD
    rdd = df.rdd.map(lambda row: (row["Department"], row["Salary"]))

    # Apply a lambda function to get the sum of the DataFrame
    rdd_aggregated = rdd.reduceByKey(lambda x, y: x + y)

    # Show the collected Results
    print(rdd_aggregated.collect())

else:

    print("I didn't do that one yet. Try again later.")