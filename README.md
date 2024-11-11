Simple Login GUI with an intergrated Database used for storing User Information ( Username and Password )

Users have the option after creating an account and logging in (all local, no cloud data) to test their password against 2 simple password cracking algorithms

  One being a Brute Force Attack, that checks every possibility given the passswords length (for simplicity)
  The other being a Dictionary Attack that utilizes a dictionary file as its source of knowledge

The program is meant to assume that the raw password is known and can be found and tested using these methods.
  However inside the database these passwords are hashed so that no raw passwords would have ever been saved.

Both Attack algorithms are limited to a small period of time to crack the password before quiting and asking the user to move on.
