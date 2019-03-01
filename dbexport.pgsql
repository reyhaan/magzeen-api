--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: trigger_set_timestamp(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trigger_set_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.trigger_set_timestamp() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    password character varying NOT NULL,
    user_id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    type character varying(255),
    company_name character varying(255),
    domain_name character varying(800),
    email character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (password, user_id, created_at, updated_at, first_name, last_name, type, company_name, domain_name, email) FROM stdin;
pbkdf2:sha256:50000$wMdsHYKY$cef5783d61d426687bc293fd08c5ff5b51e434250af799e86f90e9ca7c0f1266	10	2019-02-19 16:18:35.583098+05:30	2019-02-19 16:18:35.583098+05:30	\N	\N	\N	\N	\N	rehaan1@email.com
pbkdf2:sha256:50000$HFdTVhll$79d61b6e48825e1d47da601aaeb47e19168caf5cbd83f2e10d35519aeb529e5b	11	2019-02-19 16:19:25.342582+05:30	2019-02-19 16:19:25.342582+05:30	\N	\N	\N	\N	\N	rehaan2@email.com
pbkdf2:sha256:50000$6oF85W9L$25be48cc38eee8d2440d26f8547fa5538695d68350db314deec0aca762a3aed6	9	2019-02-19 16:09:44.246992+05:30	2019-02-22 03:22:22.593385+05:30	Rehaan	Wow	admin	wingify	magzeen.io	rehaan@email.com
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 15, true);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users on_update; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER on_update BEFORE INSERT OR UPDATE OF password, user_id, first_name, last_name, type, company_name, domain_name, email ON public.users FOR EACH ROW EXECUTE PROCEDURE public.trigger_set_timestamp();


--
-- PostgreSQL database dump complete
--

