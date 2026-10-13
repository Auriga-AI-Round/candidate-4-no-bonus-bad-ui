-- PostgreSQL schema dump — hospital management (core).
SET client_encoding = 'UTF8';

CREATE TABLE patient (
    id     SERIAL PRIMARY KEY,
    name   VARCHAR(200) NOT NULL,
    phone  VARCHAR(20),
    email  VARCHAR(254)
);
CREATE INDEX patient_name_idx ON patient (name);

CREATE TABLE doctor (
    id             SERIAL PRIMARY KEY,
    name           VARCHAR(200) NOT NULL,
    specialization VARCHAR(120),
    fee            DOUBLE PRECISION DEFAULT 0
);

CREATE TABLE appointment (
    id         SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patient (id),
    doctor_id  INTEGER NOT NULL REFERENCES doctor (id),
    start_time TIMESTAMP NOT NULL,
    end_time   TIMESTAMP NOT NULL,
    status     VARCHAR(20) DEFAULT 'booked'
);
CREATE INDEX appointment_doctor_start_idx ON appointment (doctor_id, start_time);
