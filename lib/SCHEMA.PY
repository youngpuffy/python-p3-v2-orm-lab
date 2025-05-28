🧠 How Did That Happen?
Your current code always does this:

Creates a user (or reuses them if they exist).

Adds a new payment.

Starts a new WiFi session with status 'active'.

# But it does not mark previous sessions as inactive, so the database keeps adding more sessions marked as 'active' every time you run the script