CONTINIOUS DEPLOYMENT
---------------------

### Development Methodology

1. Start new feature by creating new branch
2. Finish your feature by covering it with unit/integration tests
3. Launch your tests if all of them passed go to phase (4)
4. Launch your app if app is launched go to phase 5
5. Create a pull request to long-lasting branch (develop or master, depending on case)
6. Mark your task as fixed in youtrack


###``Remember``

1. Push to master only if:
   * you successfully build the project at your feature branch
   * you successfully passed the unit tests
2. Check that build is successfully built in Travis-CI before going home


Launching Software
------------------

## Component-by-Component

1. Celery: `celery -A natr worker -l debug`
2. 


## Using Docker

1. Run the whole project with `docker-compose up -d`
2. Check that everything is started ok `docker-compose ps`

