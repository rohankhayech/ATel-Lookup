select reports.atel_num, title 
from reports 
right join object_refs on reports.atel_num=object_refs.atel_num 
inner join objects on objects.obj_id=object_refs.obj_id 
where aliases::text like '%"aut"%'