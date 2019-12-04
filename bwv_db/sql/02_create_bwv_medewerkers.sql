CREATE TABLE public.bwv_medewerkers
(
    code character varying(6) COLLATE pg_catalog."default",
    afg_code character varying(6) COLLATE pg_catalog."default",
    naam character varying(30) COLLATE pg_catalog."default",
    status_hist character varying(1) COLLATE pg_catalog."default",
    user_created character varying(30) COLLATE pg_catalog."default",
    date_created timestamp without time zone,
    user_modified character varying(30) COLLATE pg_catalog."default",
    date_modified timestamp without time zone,
    printernaam character varying(40) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.bwv_medewerkers
    OWNER to postgres;
