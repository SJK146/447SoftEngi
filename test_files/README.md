for selenium tests most of the test are run on port 8000 when creating 
an instance to use for testing run command

flask --app main run --port 8000

this was done due to some conflicts selenium can have with overriding port
permissions as it had done so with some previous work

an additional note many tests require the use of a test account
the credentials for the account are name = test, email = test, password = test


Also additional note for some of the add study tests selenium does not like
the hover over feature and it seems to trip it up when trying to input
studies so when it runs you just need to move the cursor over
the add studies button