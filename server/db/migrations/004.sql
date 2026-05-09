start transaction;

alter table element_types drop column width;
alter table element_types drop column length;
alter table element_types add column vertices int[];
alter table projects drop column width;
alter table projects drop column length;
alter table projects add column vertices int[];

commit transaction;