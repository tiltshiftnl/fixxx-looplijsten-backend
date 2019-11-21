CREATE TABLE public.import_stadia
(
    adres_id numeric(64,0),
    wvs_nr numeric(64,0),
    sta_nr numeric(64,0),
    afg_co character varying(64) COLLATE pg_catalog."default",
    sta_code character varying(64) COLLATE pg_catalog."default",
    sta_oms character varying(64) COLLATE pg_catalog."default",
    afg_code_stad character varying(6) COLLATE pg_catalog."default",
    afs_code character varying(10) COLLATE pg_catalog."default",
    afs_oms character varying(50) COLLATE pg_catalog."default",
    afg_code_afs character varying(6) COLLATE pg_catalog."default",
    resultaat character varying(2) COLLATE pg_catalog."default",
    mdr_code character varying(4) COLLATE pg_catalog."default",
    user_created character varying(32) COLLATE pg_catalog."default",
    user_modified character varying(32) COLLATE pg_catalog."default",
    begindatum date,
    peildatum date,
    einddatum date,
    date_created date,
    date_modified date,
    wzs_id bigint NOT NULL DEFAULT nextval('import_stadia_wzs_id_seq'::regclass),
    stadia_id character varying COLLATE pg_catalog."default",
    wzs_update_datumtijd timestamp without time zone,
    CONSTRAINT import_stadia_pkey PRIMARY KEY (wzs_id)
)
WITH (
    OIDS = TRUE
)
TABLESPACE pg_default;
