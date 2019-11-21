CREATE TABLE public.bwv_hotline_bevinding
(
    id integer,
    wng_id integer,
    volgnr_bevinding integer,
    wvg_nr smallint,
    bevinding_datum timestamp without time zone,
    toez_hdr1_code character varying(6) COLLATE pg_catalog."default",
    toez_hdr2_code character varying(6) COLLATE pg_catalog."default",
    bevinding_tijd character varying(5) COLLATE pg_catalog."default",
    hit character varying(1) COLLATE pg_catalog."default",
    opmerking character varying(250) COLLATE pg_catalog."default",
    user_created character varying(30) COLLATE pg_catalog."default",
    date_created timestamp without time zone,
    user_modified character varying(30) COLLATE pg_catalog."default",
    date_modified timestamp without time zone
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
