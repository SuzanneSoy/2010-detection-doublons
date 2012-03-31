# Size of duplicates that can be removed (doesn't count the size of the copy we leave)
select round((B.tot-A.tot)/(1024.*1024.*1024.),2)||' Gb' from (select sum(size) as tot from (select distinct md5,sha1,size from files)) as A, (select sum(size) as tot from (select md5,sha1,size from files)) as B;

# List of duplicates (all copies)
select size,path from files where md5||'#'||sha1||'#'||size in (select md5||'#'||sha1||'#'||size from files group by md5,sha1,size having count(path) > 1) order by size;

# Total count of files and total weight in Gb
select round(sum(size)/(1024.*1024.*1024.),2)||' Gb        '||count(size)||' files' from files;

# find files not in folder A which have a duplicate in folder A.
update files set tag = 'A' where path like './A/%';
create table hashesA(id, hash);
insert into hashesA select rowid,size||'#'||md5||'#'||sha1 from files where tag == 'A';
create table hashesother(id, hash);
insert into hashesother select rowid,size||'#'||md5||'#'||sha1 from files where tag != 'A';
create index i_hashesA_hash on hashesA(hash);
create index i_hashesother_hash on hashesother(hash);
# find files not in folder A which have a duplicate in folder A.
select (select path from files where rowid == hashesother.id) from hashesother where hashesother.hash in (select hash from hashesA);
# find files not in folder A associated with one of their duplicates in folder A.
select (select path from files where rowid == hashesother.id),(select (select path from files where rowid == hashesA.id) from hashesA where hashesA.hash == hashesother.hash) from hashesother where hashesother.hash in (select hash from hashesA);

# Rename (prepend ".% to file name) files not in folder A which have a duplicate in folder A.
[ -e hashes.db ] && sqlite3 hashes.db "select (select path from files where rowid == hashesother.id) from hashesother where hashesother.hash in (select hash from hashesA);" > dup.lst
pv -l dup.lst | while read ab; do file="${ab##*/}"; dir="${ab%/*}"; dest="${dir}/.%${file}"; if [ -e "$ab" ]; then [ "$file" != "${file#.%}" ] || [ -e "$dest" ] || mv -i -- "$ab" "$dest"; fi; done
