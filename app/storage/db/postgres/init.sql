--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4
-- Dumped by pg_dump version 10.4

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO cryptonite;

--
-- Name: article_categories; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.article_categories (
    id character varying(80) NOT NULL,
    name character varying(120) NOT NULL
);


ALTER TABLE public.article_categories OWNER TO cryptonite;

--
-- Name: articles; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.articles (
    id character varying(80) NOT NULL,
    name character varying(120) NOT NULL,
    category_id character varying(80),
    content text
);


ALTER TABLE public.articles OWNER TO cryptonite;

--
-- Name: test_answers; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.test_answers (
    id integer NOT NULL,
    item_id integer NOT NULL,
    result_id integer NOT NULL,
    answer text,
    result boolean NOT NULL,
    "time" timestamp without time zone NOT NULL
);


ALTER TABLE public.test_answers OWNER TO cryptonite;

--
-- Name: test_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: cryptonite
--

CREATE SEQUENCE public.test_answers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_answers_id_seq OWNER TO cryptonite;

--
-- Name: test_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cryptonite
--

ALTER SEQUENCE public.test_answers_id_seq OWNED BY public.test_answers.id;


--
-- Name: test_categories; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.test_categories (
    id character varying(80) NOT NULL,
    name character varying(120) NOT NULL
);


ALTER TABLE public.test_categories OWNER TO cryptonite;

--
-- Name: test_results; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.test_results (
    id integer NOT NULL,
    user_id character varying(80) NOT NULL,
    test_id character varying(80) NOT NULL,
    begin timestamp without time zone NOT NULL,
    "end" timestamp without time zone,
    last_item integer NOT NULL,
    is_finished boolean NOT NULL
);


ALTER TABLE public.test_results OWNER TO cryptonite;

--
-- Name: test_results_id_seq; Type: SEQUENCE; Schema: public; Owner: cryptonite
--

CREATE SEQUENCE public.test_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_results_id_seq OWNER TO cryptonite;

--
-- Name: test_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cryptonite
--

ALTER SEQUENCE public.test_results_id_seq OWNED BY public.test_results.id;


--
-- Name: tests; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.tests (
    id character varying(80) NOT NULL,
    name character varying(120) NOT NULL,
    category_id character varying(80),
    not_before date,
    not_after date,
    max_duration integer
);


ALTER TABLE public.tests OWNER TO cryptonite;

--
-- Name: tests_items; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.tests_items (
    id integer NOT NULL,
    item_no integer NOT NULL,
    test_id character varying(80) NOT NULL,
    content text
);


ALTER TABLE public.tests_items OWNER TO cryptonite;

--
-- Name: tests_items_id_seq; Type: SEQUENCE; Schema: public; Owner: cryptonite
--

CREATE SEQUENCE public.tests_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tests_items_id_seq OWNER TO cryptonite;

--
-- Name: tests_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cryptonite
--

ALTER SEQUENCE public.tests_items_id_seq OWNED BY public.tests_items.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: cryptonite
--

CREATE TABLE public.users (
    id character varying(80) NOT NULL,
    name character varying(80) NOT NULL,
    password character varying(120),
    first_name character varying(120),
    second_name character varying(120),
    last_name character varying(120),
    is_admin boolean NOT NULL
);


ALTER TABLE public.users OWNER TO cryptonite;

--
-- Name: test_answers id; Type: DEFAULT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_answers ALTER COLUMN id SET DEFAULT nextval('public.test_answers_id_seq'::regclass);


--
-- Name: test_results id; Type: DEFAULT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_results ALTER COLUMN id SET DEFAULT nextval('public.test_results_id_seq'::regclass);


--
-- Name: tests_items id; Type: DEFAULT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.tests_items ALTER COLUMN id SET DEFAULT nextval('public.tests_items_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.alembic_version (version_num) FROM stdin;
eadf76995996
\.


--
-- Data for Name: article_categories; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.article_categories (id, name) FROM stdin;
zaschita-konfidentsialnosti     Защита конфиденциальности
\.


--
-- Data for Name: articles; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.articles (id, name, category_id, content) FROM stdin;
novyj-material  Новый материал  zaschita-konfidentsialnosti     Здесь располагается материал по определенному курсу.\n----------------------------------------------------\n\nСодержимое можно редактировать\n\n![](data:image/png;base64,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)
\.


--
-- Data for Name: test_answers; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.test_answers (id, item_id, result_id, answer, result, "time") FROM stdin;
1       2       1       ПЕРВЫЙ вопрос\n=============\n\nСодержание вопроса.\n\nВарианты ответов:\n\n*   ( ) Да\n*   ( ) Нет\n*   (*) Наверное\n*   ( ) Все и сразу      t       2018-05-27 15:20:08.820889
2       3       1       Другой вопрос\n=============\n\nСодержание вопроса.\n\nВарианты ответов:\n\n*   [x] Да\n*   [x] Нет\n*   [ ] Наверное\n*   [ ] Все и сразу      f       2018-05-27 15:20:11.453236
\.


--
-- Data for Name: test_categories; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.test_categories (id, name) FROM stdin;
kriptografija   Криптография
\.


--
-- Data for Name: test_results; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.test_results (id, user_id, test_id, begin, "end", last_item, is_finished) FROM stdin;
1       admin   novyj-test      2018-05-27 15:19:51     2018-05-27 15:20:11.477895      3       t
\.


--
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.tests (id, name, category_id, not_before, not_after, max_duration) FROM stdin;
novyj-test      Новый тест      kriptografija   2018-05-01      2018-06-10      60
\.


--
-- Data for Name: tests_items; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.tests_items (id, item_no, test_id, content) FROM stdin;
2       1       novyj-test      ПЕРВЫЙ вопрос\n=============\n\nСодержание вопроса.\n\nВарианты ответов:\n\n*   ( ) Да\n*   ( ) Нет\n*   (*) Наверное\n*   ( ) Все и сразу
3       2       novyj-test      Другой вопрос\n=============\n\nСодержание вопроса.\n\nВарианты ответов:\n\n*   [x] Да\n*   [ ] Нет\n*   [x] Наверное\n*   [x] Все и сразу
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: cryptonite
--

COPY public.users (id, name, password, first_name, second_name, last_name, is_admin) FROM stdin;
admin   admin   pbkdf2:sha256:50000$Fmy3TVfK$b5b49cb1dc79e0fe676857c446dc89361e17f8ad2f841fbce76fcc479001897c   Преподаватель   Кафедры ИБ      t
student student pbkdf2:sha256:50000$g00vk1IN$f9cd694463175fb2137f57e9730ce18d57b8c2b5ab6837acce3a03ee40928f5f   Студент НИУ     МИЭТ    f
\.


--
-- Name: test_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cryptonite
--

SELECT pg_catalog.setval('public.test_answers_id_seq', 2, true);


--
-- Name: test_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cryptonite
--

SELECT pg_catalog.setval('public.test_results_id_seq', 1, true);


--
-- Name: tests_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cryptonite
--

SELECT pg_catalog.setval('public.tests_items_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: article_categories article_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.article_categories
    ADD CONSTRAINT article_categories_pkey PRIMARY KEY (id);


--
-- Name: articles articles_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT articles_pkey PRIMARY KEY (id);


--
-- Name: test_answers test_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_answers
    ADD CONSTRAINT test_answers_pkey PRIMARY KEY (id);


--
-- Name: test_categories test_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_categories
    ADD CONSTRAINT test_categories_pkey PRIMARY KEY (id);


--
-- Name: test_results test_results_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_results
    ADD CONSTRAINT test_results_pkey PRIMARY KEY (id);


--
-- Name: tests_items tests_items_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.tests_items
    ADD CONSTRAINT tests_items_pkey PRIMARY KEY (id);


--
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_article_categories_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE UNIQUE INDEX ix_article_categories_name ON public.article_categories USING btree (name);


--
-- Name: ix_articles_category_id; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_articles_category_id ON public.articles USING btree (category_id);


--
-- Name: ix_articles_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE UNIQUE INDEX ix_articles_name ON public.articles USING btree (name);


--
-- Name: ix_test_answers_item_id; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_test_answers_item_id ON public.test_answers USING btree (item_id);


--
-- Name: ix_test_answers_result; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_test_answers_result ON public.test_answers USING btree (result);


--
-- Name: ix_test_answers_result_id; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_test_answers_result_id ON public.test_answers USING btree (result_id);


--
-- Name: ix_test_categories_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE UNIQUE INDEX ix_test_categories_name ON public.test_categories USING btree (name);


--
-- Name: ix_test_results_is_finished; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_test_results_is_finished ON public.test_results USING btree (is_finished);


--
-- Name: ix_test_results_last_item; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_test_results_last_item ON public.test_results USING btree (last_item);


--
-- Name: ix_test_results_test_id; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_test_results_test_id ON public.test_results USING btree (test_id);


--
-- Name: ix_test_results_user_id; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_test_results_user_id ON public.test_results USING btree (user_id);


--
-- Name: ix_tests_category_id; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_tests_category_id ON public.tests USING btree (category_id);


--
-- Name: ix_tests_items_item_no; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_tests_items_item_no ON public.tests_items USING btree (item_no);


--
-- Name: ix_tests_items_test_id; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_tests_items_test_id ON public.tests_items USING btree (test_id);


--
-- Name: ix_tests_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE UNIQUE INDEX ix_tests_name ON public.tests USING btree (name);


--
-- Name: ix_users_first_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_users_first_name ON public.users USING btree (first_name);


--
-- Name: ix_users_is_admin; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_users_is_admin ON public.users USING btree (is_admin);


--
-- Name: ix_users_last_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_users_last_name ON public.users USING btree (last_name);


--
-- Name: ix_users_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE UNIQUE INDEX ix_users_name ON public.users USING btree (name);


--
-- Name: ix_users_second_name; Type: INDEX; Schema: public; Owner: cryptonite
--

CREATE INDEX ix_users_second_name ON public.users USING btree (second_name);


--
-- Name: articles articles_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT articles_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.article_categories(id);


--
-- Name: test_answers test_answers_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_answers
    ADD CONSTRAINT test_answers_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.tests_items(id);


--
-- Name: test_answers test_answers_result_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_answers
    ADD CONSTRAINT test_answers_result_id_fkey FOREIGN KEY (result_id) REFERENCES public.test_results(id);


--
-- Name: test_results test_results_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_results
    ADD CONSTRAINT test_results_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id);


--
-- Name: test_results test_results_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.test_results
    ADD CONSTRAINT test_results_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tests tests_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.test_categories(id);


--
-- Name: tests_items tests_items_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cryptonite
--

ALTER TABLE ONLY public.tests_items
    ADD CONSTRAINT tests_items_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id);


--
-- PostgreSQL database dump complete
--
