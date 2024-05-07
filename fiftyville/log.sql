-- Keep a log of any SQL queries you execute as you solve the mystery.

--to obtain the description of the crime scene
SELECT description FROM crime_scene_reports WHERE day = 28 AND street = 'Humphrey' AND month = 'July' AND year = 2021;

--TO catch the thief
SELECT people.name FROM people
WHERE people.id IN (
    SELECT people.id FROM people
    WHERE people.license_plate IN (
        --to obtain query of the license plates
        SELECT license_plate FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
        AND minute >= 15 and minute <=25 AND activity = 'exit'
    )
)

AND people.id IN(
    SELECT people.id FROM people
    WHERE people.phone_number IN(
        --to obtain callers that called same day
        SELECT caller FROM phone_calls
        WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
    )
)

AND people.id IN(
    SELECT people.id FROM people
    WHERE people.id IN(
        SELECT person_id FROM bank_accounts
        WHERE account_number IN(
            --to view all bank transactions and account number
            SELECT account_number FROM atm_transactions
            WHERE year = 2021 AND month = 7 AND day = 28
            AND atm_location = "Leggett Street"
            AND transaction_type = 'withdraw'
        )
    )
)

AND people.id IN (
    SELECT people.id
    FROM people
    WHERE people.passport_number IN (
        SELECT passengers.passport_number
        FROM people
        JOIN passengers
        ON people.passport_number = passengers.passport_number
        JOIN flights
        --to see passengers who flew during this period
        ON passengers.flight_id = flights.id
        WHERE flights.year = 2021
        AND flights.month = 7 AND flights.day = 29
        AND flights.hour = 8  AND flights.minute = 20
    )
);



-- To find his accomplice
--Best we use the phone call he made
SELECT people.name FROM people
WHERE people.phone_number IN(
    --to get the receiving end of the call
    SELECT receiver FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
    AND caller = (
        SELECT people.phone_number FROM people
        WHERE people.name = "Bruce"
)
);



--To find the planned destination
SELECT DISTINCT airports.city
FROM flights
JOIN airports
ON airports.id = (
    --query for passengers on that day
	SELECT flights.destination_airport_id FROM people
    JOIN passengers
    ON people.passport_number = passengers.passport_number
    JOIN flights
    ON passengers.flight_id = flights.id
    WHERE flights.year = 2021
    AND flights.month = 7 AND flights.day = 29
    AND people.name = "Bruce"
);