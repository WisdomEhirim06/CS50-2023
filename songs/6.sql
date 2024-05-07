--to ouput songs by post malone only--

SELECT name FROM songs WHERE artist_id = (
    SELECT id FROM artists WHERE name = 'Post Malone');