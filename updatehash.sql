# Size of duplicates that can be removed (doesn't count the size of the copy we leave)
select round((B.tot-A.tot)/(1024.*1024.*1024.),2)||' Gb' from (select sum(size) as tot from (select distinct md5,sha1,size from files)) as A, (select sum(size) as tot from (select md5,sha1,size from files)) as B;

# List of duplicates (all copies)
select size,path from files where md5||'#'||sha1||'#'||size in (select md5||'#'||sha1||'#'||size from files group by md5,sha1,size having count(path) > 1) order by size;

# Total count of files and total weight in Gb
select round(sum(size)/(1024.*1024.*1024.),2)||' Gb        '||count(size)||' files' from files;
