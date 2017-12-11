from athena2pyspark.athena_sql import querybyByName
u'''
Created on 27-11-2017

@author: lnjofre

El problema fundamental del mantenimiento de un programa es que arreglar un defecto tiene una sustancial 
(20-50%) probabilidad de introducir otro. Por tanto, el proceso completo es dar dos pasos adelante y uno hacia atras 
-- Fred Brooks

El testing de componentes puede ser muy efectivo para mostrar la presencia de errores, pero absolutamente inadecuado para demostrar su ausencia
-- Edsger Dijkstra
'''
import unittest
from athena2pyspark import get_dataframe, run_query, get_ddl, run_create_table
from athena2pyspark.config import getLocalSparkSession

spark = getLocalSparkSession()

class Test(unittest.TestCase):
    
    def test_empty_folder(self):
        '''
        lanza la excepción cuando uno quiere guardar archivos en carpetas no vacias. las
        carpetas no vacias pueden generar porblemas en athena
        '''
        pass
    
    def test_0_getByName(self):
        query = querybyByName("sql/afinidad_marca")
        s3_output = "s3://leonardo.exalitica.com/boto3/query_1/"
        query = run_query(query=query, database="prod_jumbo", s3_output=s3_output, spark=spark)
        
        pass
    
    def test_afinidad_de_marcas(self):
        
        from athena2pyspark.athena_sql.dinamicas import afinidad_de_marcas
        
        query = afinidad_de_marcas()
        
        s3_output = "s3://leonardo.exalitica.com/boto3/query_1/"
        
        path_location = run_query(query=query, database="prod_easy", s3_output=s3_output, spark=spark)
        
        # df = get_dataframe(path_query = path_location, spark=spark)
        
        return query, s3_output, path_location

    def test_RunQuery(self):
        s3_output = "s3://leonardo.exalitica.com/boto3/query_1/"
        df = run_query(query = "select * from baul_2 limit 1000", 
                       database = "ljofre", 
                       s3_output = s3_output, 
                       spark=spark)
        return df
    
    def test_GetDDL(self):
        s3_output = "s3://leonardo.exalitica.com/boto3/query_1/"
        file_location = run_query(query = "select * from baul_2 limit 1000", database = "ljofre", s3_output = s3_output, spark=spark)
        df = get_dataframe(file_location, spark=spark)
        ddl_create_database, ddl_create_table = get_ddl(df=df, database="ljofre", table="test_table",s3_input=s3_output)
        return ddl_create_database, ddl_create_table
    
    def test_CreateTable(self):
        """ crea la tabla a partir de la informacion existente en la carpeta dada: deben existir
        ciertas validaciones importantes, como lo son, que todos los archivos tengan la misma estructura
        , que no existan archivos de metadata"""
        
        s3_output = "s3://leonardo.exalitica.com/boto3/query_1/"
        file_location = run_query(query = "select * from baul_2 limit 1000", 
                                  database = "ljofre", 
                                  s3_output = s3_output, 
                                  spark=spark)
        
        df = get_dataframe(file_location, spark=spark)
        _, ddl_create_table = get_ddl(df=df, database="ljofre", table="test_table_2",s3_input=s3_output)
        run_create_table(query = ddl_create_table, database = "ljofre", s3_output=s3_output)