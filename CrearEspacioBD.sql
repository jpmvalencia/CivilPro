connect system/0000

show con_name

ALTER SESSION SET CONTAINER=CDB$ROOT;
ALTER DATABASE OPEN;

DROP TABLESPACE civilpro INCLUDING CONTENTS and DATAFILES;
    
CREATE TABLESPACE civilpro LOGGING
DATAFILE 'C:\BDOracle\lamarquesa.dbf' size 50M
extent management local segment space management auto; 
 
alter session set "_ORACLE_SCRIPT"=true; 
 
drop user civilproadmin cascade;
SELECT tablespace_name FROM dba_tablespaces WHERE tablespace_name = 'civilpro';
    
CREATE user civilproadmin profile 
default identified by 31415926
default tablespace civilpro 
temporary tablespace temp 
account unlock;     

--privilegios
grant connect, resource,dba to civilproadmin; 

connect civilproadmin/31415926

show user