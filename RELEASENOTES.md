## Version 1.0.3 - 2024-11-03

#### Fixed
- The game details graph now only displays completed legs or sets, omitting the current ones.
- Improved the display of the checkout rate in the Player Modal on the Database Details Pages.

#### Added
- A message indicating "No data available" is now shown if no leg is finished in the game details graph.
- The checkout text now displays "N/A" instead of "0%" if no checkout dart was thrown.
- A message indicating "No games in database" is now shown if there are no games in the database.

## Version 1.0.2 - 2024-10-24

#### Fixed
- Resolved routing issue to the database page.
- Fixed bug where the graph on the details database game page was not updated at leg or set win until the first dart of the next leg was thrown.
- Corrected buggy view of thrown darts on the scoreboard page.

#### Added
- Introduced router configuration class in the backend for better management.


## Version 1.0.1 - 2024-10-23

#### Added
- Release note functionality to keep track of changes and updates.

#### Removed
- Database-related feature to limit database entries for improved performance.

#### Notes
- The repository is optimized for speed, making extensive database entries unnecessary.
- Future updates will replace the pickle-based database with a more efficient solution.

## Version 1.0.0 - 2024-10-17

Welcome to the initial release of DartsCounter!

DartsCounter is a comprehensive tool designed to enhance your dart-playing experience. With DartsCounter, you can:

- Track scores for multiple players in real-time.
- View detailed past game results and statistics.
- Manage user profiles with personalized settings.
- Enjoy a user-friendly interface tailored for both casual and competitive play.

#### Features
- **Score Tracking**: Keep accurate scores for all players.
- **Game History**: Access past game results and performance statistics.
- **User Profiles**: Create and manage profiles with custom settings.
- **Intuitive Interface**: Easy-to-use design for seamless gameplay.