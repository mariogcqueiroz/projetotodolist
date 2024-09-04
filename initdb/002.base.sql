--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

-- Started on 2020-04-12 18:08:01

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;



CREATE TABLE public.tasks
(
    id serial,
    titulo text,
    descricao text,
    stat text,
    datacriacao timestamp,
    CONSTRAINT pk_fb PRIMARY KEY (id)
)
    WITH (
        OIDS=FALSE
    );
