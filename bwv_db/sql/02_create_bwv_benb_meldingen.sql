CREATE TABLE public.bwv_benb_meldingen
(
    id numeric(20,0),
    identificatie character varying(20) COLLATE pg_catalog."default",
    tijdstip_bericht timestamp without time zone,
    bsn character varying(9) COLLATE pg_catalog."default",
    voorletters character varying(5) COLLATE pg_catalog."default",
    voornamen character varying(30) COLLATE pg_catalog."default",
    naam character varying(50) COLLATE pg_catalog."default",
    woonplaats_naam character varying(50) COLLATE pg_catalog."default",
    straatnaam character varying(50) COLLATE pg_catalog."default",
    postcode character varying(6) COLLATE pg_catalog."default",
    huisnummer character varying(10) COLLATE pg_catalog."default",
    huislet character varying(2) COLLATE pg_catalog."default",
    huistoev character varying(4) COLLATE pg_catalog."default",
    aan_afmeld character varying(1) COLLATE pg_catalog."default",
    datum_melding timestamp without time zone,
    wng_id bigint,
    user_created character varying(30) COLLATE pg_catalog."default",
    date_created timestamp without time zone,
    user_modified character varying(30) COLLATE pg_catalog."default",
    date_modified timestamp without time zone,
    bericht text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
