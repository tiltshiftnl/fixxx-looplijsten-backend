CREATE TABLE public.bwv_hotline_melding
(
    id integer,
    wng_id integer,
    volgnr_melding integer,
    wvg_nr smallint,
    melding_datum timestamp without time zone,
    mdw_code character varying(6) COLLATE pg_catalog."default",
    overtreding_code character varying(4) COLLATE pg_catalog."default",
    melder_anoniem character varying(1) COLLATE pg_catalog."default",
    melder_naam character varying(40) COLLATE pg_catalog."default",
    melder_emailadres character varying(40) COLLATE pg_catalog."default",
    melder_telnr character varying(16) COLLATE pg_catalog."default",
    situatie_schets character varying(1500) COLLATE pg_catalog."default",
    user_created character varying(30) COLLATE pg_catalog."default",
    date_created timestamp without time zone,
    user_modified character varying(30) COLLATE pg_catalog."default",
    date_modified timestamp without time zone
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
