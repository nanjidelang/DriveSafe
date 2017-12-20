drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    Heartrate text not null,
    SpO2 text not null
);