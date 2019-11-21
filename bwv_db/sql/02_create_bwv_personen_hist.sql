CREATE TABLE public.bwv_personen_hist
(
    pen_id integer,
    ads_id integer,
    vertrekdatum_adam timestamp without time zone,
    vertrekdatum_adres timestamp without time zone,
    vestigingsdatum_adam timestamp without time zone,
    vestigingsdatum_adres timestamp without time zone,
    overlijdensdatum timestamp without time zone,
    volgnr_pen integer,
    huisnummer character varying(5) COLLATE pg_catalog."default",
    huisletter character varying(1) COLLATE pg_catalog."default",
    pee_code character varying(4) COLLATE pg_catalog."default",
    postcode character varying(6) COLLATE pg_catalog."default",
    locatie character varying(55) COLLATE pg_catalog."default",
    gem_code character varying(4) COLLATE pg_catalog."default",
    lnd_code character varying(4) COLLATE pg_catalog."default",
    geheim_adres character varying(1) COLLATE pg_catalog."default",
    geheim character varying(1) COLLATE pg_catalog."default",
    user_created character varying(30) COLLATE pg_catalog."default",
    date_created timestamp without time zone,
    user_modified character varying(30) COLLATE pg_catalog."default",
    date_modified timestamp without time zone
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
