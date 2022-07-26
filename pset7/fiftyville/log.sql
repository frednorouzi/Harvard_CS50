-- Keep a log of any SQL queries you execute as you solve the mystery.
-- The theft took place on July 28, 2020 and that it took place on Chamberlin Street.
SELECT description FROM crime_scene_reports
WHERE  month = 7 AND day = 28 AND year = 2020 AND street = "Chamberlin Street" ;
/* description
Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
Interviews were conducted today with three witnesses who were present at the time
— each of their interview transcripts mentions the courthouse.
*/
SELECT transcript FROM interviews
WHERE month = 7 AND day = 28 AND year = 2020 AND transcript like "%courthouse%";
/*
transcript
Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away.
If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the
ATM on Fifer Street and saw the thief there withdrawing some money.
As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say
that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone
to purchase the flight ticket.
*/
-- List of suspects name based on 10 minutes timeframe according on license plates of car exiting the courthouse
SELECT name FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE month = 7 AND day = 28 AND year = 2020 AND hour = 10 AND minute >= 15 AND minute < 25 AND activity = "exit";

-- List of suspects name who made a withdrawal that day on Fifer Street.
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE month = 7 AND day = 28 AND year = 2020 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";

-- List of people that who made a call less than minute on that day.
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60 ;

-- The names of people where they took the first flight on day after crime
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = (
        SELECT id FROM flights
        WHERE month = 7 AND day = 29 AND year = 2020
        ORDER BY hour, minute LIMIT 1);

-- Intersection of all cases in order to get the name of the thief
SELECT name FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE month = 7 AND day = 28 AND year = 2020 AND hour = 10 AND minute >= 15 AND minute < 25 AND activity = "exit"
INTERSECT
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE month = 7 AND day = 28 AND year = 2020 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"
INTERSECT
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60
INTERSECT
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = (
        SELECT id FROM flights
        WHERE month = 7 AND day = 29 AND year = 2020
        ORDER BY hour, minute LIMIT 1);

-- Get the thief destination
SELECT city FROM airports
WHERE id = (
            SELECT destination_airport_id FROM flights
            WHERE month = 7 AND day = 29 AND year = 2020
            ORDER BY hour, minute LIMIT 1);

-- Finding the accomplice
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE day = "28" AND month = "7" AND year = "2020"  AND duration < "60"
    AND caller = (SELECT phone_number FROM people WHERE name = "Ernest");