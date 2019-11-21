CREATE TABLE public.import_wvs
(
    adres_id numeric(64,0),
    wvs_nr numeric(64,0),
    begindatum timestamp without time zone,
    einddatum timestamp without time zone,
    beh_code character varying(64) COLLATE pg_catalog."default",
    beh_oms character varying(64) COLLATE pg_catalog."default",
    afg_code_beh character varying(64) COLLATE pg_catalog."default",
    afs_code character varying(64) COLLATE pg_catalog."default",
    afs_oms character varying(64) COLLATE pg_catalog."default",
    afg_code_afs character varying(64) COLLATE pg_catalog."default",
    kamer_aantal numeric(64,0),
    nuttig_woonoppervlak numeric(64,0),
    vloeroppervlak_totaal numeric(64,0),
    bedrag_huur numeric(64,0),
    eigenaar character varying(64) COLLATE pg_catalog."default",
    wzs_id bigint NOT NULL DEFAULT nextval('import_wvs_wzs_id_seq'::regclass),
    zaak_id character varying COLLATE pg_catalog."default",
    wzs_update_datumtijd timestamp with time zone,
    mededelingen character varying(5012) COLLATE pg_catalog."default",
    CONSTRAINT import_wvs_pkey PRIMARY KEY (wzs_id)
)
WITH (
    OIDS = TRUE
)
TABLESPACE pg_default;
