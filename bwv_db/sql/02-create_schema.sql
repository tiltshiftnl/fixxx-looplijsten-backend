create table bwv_benb_meldingen (
  datum_melding timestamp without time zone,
  wng_id        bigint
);

create table bwv_hotline_bevinding (
  wng_id           integer,
  volgnr_bevinding integer,
  bevinding_datum  timestamp without time zone,
  toez_hdr1_code   character varying(6),
  toez_hdr2_code   character varying(6),
  bevinding_tijd   character varying(5),
  hit              character varying(1),
  opmerking        character varying(250)
);

create table bwv_hotline_melding (
  wng_id            integer,
  melding_datum     timestamp without time zone,
  melder_anoniem    character varying(1),
  melder_naam       character varying(40),
  melder_emailadres character varying(40),
  melder_telnr      character varying(16),
  situatie_schets   character varying(1500),
  id                integer
);

create table import_adres (
  wng_id        numeric(64,0),
  adres_id      numeric(64,0),
  sttnaam       character varying(64),
  hsnr          bigint,
  hsltr         character varying(1),
  toev          character varying(16),
  postcode      character varying(6),
  landelijk_bag character varying(64),
  sbw_omschr    character varying(64),
  kmrs          numeric(17,1),
  wzs_lon       double precision,
  wzs_lat       double precision,
  inwnrs        double precision,
  a_dam_bag     character varying(14),
  pvh_omschr    character varying(50),
  sbv_omschr    character varying(50)
);

create table import_stadia (
  adres_id   numeric(64,0),
  sta_nr     numeric(64,0),
  begindatum date,
  peildatum  date,
  einddatum  date,
  sta_oms    character varying(64),
  stadia_id  character varying(32),
  wvs_nr     smallint
);

create table import_wvs (
  adres_id              numeric(64,0),
  wvs_nr                numeric(64,0),
  beh_oms               character varying(64),
  afs_code              character varying(64),
  nuttig_woonoppervlak  numeric(64,0),
  vloeroppervlak_totaal numeric(64,0),
  zaak_id               character varying(32),
  mededelingen          character varying(2000),
  begindatum            date,
  einddatum             timestamp without time zone,
  afs_oms               character varying(50),
  eigenaar              character varying(30),
  kamer_aantal          smallint,
  afg_code_beh          character varying(10),
  beh_code              character varying(10),
  bedrag_huur           integer
);

create table bwv_medewerkers (
  code        character varying(6),
  naam        character varying(30),
  printernaam character varying(40)
);

create table bwv_personen (
  id                integer,
  ads_id_wa         integer,
  geslacht          character varying(1),
  voorletters       character varying(5),
  geboortedatum     timestamp without time zone,
  naam              character varying(30),
  gezinsverhouding  character varying(10)
);

create table bwv_personen_hist (
 pen_id                integer,
 ads_id                integer,
 vertrekdatum_adres    timestamp without time zone,
 vestigingsdatum_adres timestamp without time zone,
 overlijdensdatum      timestamp without time zone,
 vertrekdatum_adam     timestamp without time zone
);

create table bwv_vakantieverhuur (
  datum_aanvang_verhuur timestamp without time zone,
  datum_einde_verhuur   timestamp without time zone,
  wng_id                bigint,
  annuleer_date         timestamp without time zone
);
