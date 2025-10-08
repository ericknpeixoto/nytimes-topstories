from datetime import datetime, timedelta

def table_exists(spark, catalog, schema_name, table_name):
    spark.catalog.setCurrentCatalog(catalog)
    return spark.catalog.tableExists(f'{schema_name}.{table_name}')


def get_first_partition(spark, catalog, schema_name, table_name, partition):
    spark.catalog.setCurrentCatalog(catalog)
    return spark.sql(f'SHOW PARTITIONS {catalog}.{schema_name}.{table_name}').orderBy(f'{partition}').limit(1).collect()[0][0]

def get_last_partition(spark, catalog, schema_name, table_name, partition):
    spark.catalog.setCurrentCatalog(catalog)
    return spark.sql(f'SHOW PARTITIONS {catalog}.{schema_name}.{table_name}').orderBy(f'{partition}', ascending = False).limit(1).collect()[0][0]
