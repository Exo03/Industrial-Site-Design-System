start transaction;

alter table element_types add column width int;
alter table element_types add column length int;
alter table element_types drop column points;
alter table projects add column width int;
alter table projects add column length int;
alter table projects drop column points;

commit transaction;