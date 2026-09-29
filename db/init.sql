-- Runs ONLY the first time the database volume is created (empty volume).
CREATE TABLE IF NOT EXISTS items (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    category   VARCHAR(50)  NOT NULL,
    available  BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS borrows (
    id            SERIAL PRIMARY KEY,
    item_id       INT          NOT NULL REFERENCES items(id),
    borrower_name VARCHAR(100) NOT NULL,
    borrow_date   DATE         NOT NULL,
    due_date      DATE         NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'borrowed',
    returned_at   TIMESTAMP
);

INSERT INTO items (name, category) VALUES
    ('Arduino Uno Starter Kit', 'Microcontroller'),
    ('Raspberry Pi 4',          'Single-board computer'),
    ('Digital Multimeter',      'Measuring tool'),
    ('RJ45 Crimping Tool',      'Networking');
