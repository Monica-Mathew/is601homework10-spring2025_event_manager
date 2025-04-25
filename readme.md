# Event Manager Company: Software QA Analyst/Developer Onboarding Assignment

Welcome to the Event Manager Company! As a newly hired Software QA Analyst/Developer and a student in software engineering, you are embarking on an exciting journey to contribute to our project aimed at developing a secure, robust REST API that supports JWT token-based OAuth2 authentication. This API serves as the backbone of our user management system and will eventually expand to include features for event management and registration.

## Assignment Objectives

1. **Familiarize with REST API functionality and structure**: Gain hands-on experience working with a REST API, understanding its endpoints, request/response formats, and authentication mechanisms.

2. **Implement and refine documentation**: Critically analyze and improve existing documentation based on issues identified in the instructor videos. Ensure that the documentation is up-to-date and accurately reflects the current state of the software.

3. **Engage in manual and automated testing**: Develop comprehensive test cases and leverage automated testing tools like pytest to push the project's test coverage towards 90%. Gain experience with different types of testing, such as unit testing, integration testing, and end-to-end testing.

4. **Explore and debug issues**: Dive deep into the codebase to investigate and resolve issues related to user profile updates and OAuth token generation. Utilize debugging tools, interpret error messages, and trace the flow of execution to identify the root cause of problems.

5. **Collaborate effectively**: Experience the power of collaboration using Git for version control and GitHub for code reviews and issue tracking. Work with issues, branches, create pull requests, and merge code while following best practices.

## Setup and Preliminary Steps

1. **Fork the Project Repository**: Fork the [project repository](https://github.com/yourusername/event_manager) to your own GitHub account. This creates a copy of the repository under your account, allowing you to work on the project independently.

2. **Clone the Forked Repository**: Clone the forked repository to your local machine using the `git clone` command. This creates a local copy of the repository on your computer, enabling you to make changes and run the project locally.

3. **Verify the Project Setup**: Follow the steps in the instructor video to set up the project using [Docker](https://www.docker.com/). Docker allows you to package the application with all its dependencies into a standardized unit called a container. Verify that you can access the API documentation at `http://localhost/docs` and the database using [PGAdmin](https://www.pgadmin.org/) at `http://localhost:5050`.

## Testing and Database Management

1. **Explore the API**: Use the Swagger UI at `http://localhost/docs` to familiarize yourself with the API endpoints, request/response formats, and authentication mechanisms. Swagger UI provides an interactive interface to explore and test the API endpoints.

2. **Run Tests**: Execute the provided test suite using pytest, a popular testing framework for Python. Running tests ensures that the existing functionality of the API is working as expected. Note that running tests will drop the database tables, so you may need to manually drop the Alembic version table using PGAdmin and re-run migrations to ensure a clean state.

3. **Increase Test Coverage**: To enhance the reliability of the API, aim to increase the project's test coverage to 90%. Write additional tests for various scenarios and edge cases to ensure that the API handles different situations correctly.

## Collaborative Development Using Git

1. **Enable Issue Tracking**: Enable GitHub issues in your repository settings. [GitHub Issues](https://guides.github.com/features/issues/) is a powerful tool for tracking bugs, enhancements, and other tasks related to the project. It allows you to create, assign, and prioritize issues, facilitating effective collaboration among team members.

2. **Create Branches**: For each issue or task you work on, create a new branch with a descriptive name using the `git checkout -b` command. Branching allows you to work on different features or fixes independently without affecting the main codebase. It enables parallel development and helps maintain a stable main branch.

3. **Pull Requests and Code Reviews**: When you have completed work on an issue, create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to merge your changes into the main branch. Pull requests provide an opportunity for code review, where your team members can examine your changes, provide feedback, and suggest improvements. Code reviews help maintain code quality, catch potential issues, and promote knowledge sharing among the team.

## Specific Issues to Address

In this assignment, you will identify, document, and resolve five specific issues related to:

1. **Username validation**: Investigate and resolve any issues related to username validation. This may involve handling special characters, enforcing length constraints, or ensuring uniqueness. Proper username validation is essential to maintain data integrity and prevent potential security vulnerabilities.

2. **Password validation**: Ensure that password validation follows security best practices, such as enforcing minimum length, requiring complexity (e.g., a mix of uppercase, lowercase, numbers, and special characters), and properly hashing passwords before storing them in the database. Robust password validation protects user accounts and mitigates the risk of unauthorized access.

3. **Profile field edge cases**: Test and handle various scenarios related to updating profile fields. This may include updating the bio and profile picture URL simultaneously or individually. Consider different combinations of fields being updated and ensure that the API handles these cases gracefully. Edge case testing helps uncover potential issues and ensures a smooth user experience.

Additionally, you will resolve a sixth issue demonstrated in the instructor video. These issues will test various combinations and scenarios to simulate real-world usage and potential edge cases. By addressing these specific issues, you will gain experience in identifying and resolving common challenges in API development.

## Submission:

 ### Issues
  - [Issue 1 - Password Validation](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/issues/3) 
      Added validations to the password to make it strong, pydantic data model support custom validations to have password being 8 chars, special chars etc - [app/schemas/user_schemas.py](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/4/files#diff-b9e87a0161370245e876813f8f9823be535b73da8fbbba7ac126986a2c6a9cb7)

  - [Issue 2 -  Email validation](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/issues/9)
      In this project, the email is used as username, hence we check if the email is already registered in the system (uniqueness) and we have validations to make sure the username is a valid username -  [app/schemas/user_schemas.py](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/10/files#diff-b9e87a0161370245e876813f8f9823be535b73da8fbbba7ac126986a2c6a9cb7)

  - [Issue 3 - Profile fields update validation function](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/issues/11)
      Added validations for the profile field update - put endpoint - to make sure all fields can be updated, and if update is made with no inputs, validtion error would be thrown back - [app/services/user_service.py](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/12/files#diff-8e8622b7fd5979ba58404f96e1fd81c5512208dee6dbe0e28390d706055864e6)

   - [Issue 4 - Profile fields update edge cases tests](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/issues/7)
        Added tests to cover for the edge cases for profile fields updation, and updated the validations accordingly 
        [app/schemas/user_schemas.py](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/8/files#diff-b9e87a0161370245e876813f8f9823be535b73da8fbbba7ac126986a2c6a9cb7) and [tests/test_services/test_user_service.py](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/8/files#diff-e3f3da0661632e0add5f28cb40266e4bfbd6e0c1a23cdb5f5e8813af69cf1d5c)

  -  [Issue 5 - Updated smtp credentials and fixed tests](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/issues/17)
      Created mailtrap account, and added credentials to the .env file and completed the UI testing. For unit tests, added mocks to stimulate the smtp mock behavior - [tests/test_services/test_user_service.py](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/18/files#diff-e3f3da0661632e0add5f28cb40266e4bfbd6e0c1a23cdb5f5e8813af69cf1d5c)

  -  [Issue mentioned in the demo](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/issues/13) 
        Tried out with LoginRequest pydantic model, and we could fix the issue by prefilling data, but it causes issue with oauth2_scheme for authorization endpoint for admin/managers. Hence continued using OAuth2PasswordRequestForm to capture email and password. Added desciptive for login - [app/routers/user_routes.py](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/14/files#diff-3f00ec2c24998d185e23313c030b5256c01c3b3e611ffb10c3c9437d4fa9cf77)
  
  -  Github action pass and dependency issues
        Updated [flaky tests](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/18/files#diff-e52e4ddd58b7ef887ab03c04116e676f6280b824ab7469d5d3080e5cba4f2128) which were intermittently failing and medium/ critical severity vulnerabilities [dependencies](https://github.com/Monica-Mathew/is601homework10-spring2025_event_manager/pull/18/files#diff-4d7c51b1efe9043e44439a949dfd92e5827321b34082903477fd04876edb7552)

  ### Dockerhub image
  - Link to project image deployed to Dockerhub.
      [Dockerhub image - monicamathew/is601homework10](https://hub.docker.com/layers/monicamathew/is601homework10/688404ce97f69abbe53226ce206edfffb739461c/images/sha256-b2d49a53b89f8efd2f59ed019e919ccbb69037ee88b90014ef4a52f5c70175bf)

  ### Reflection
  This assignment was absolutely a great learning experience. As not having much experience with Python web development, usage of FastAPI and user authentication systems was a game changer. I was able to get hands on experience on all key components of a full stack project, including Postgres backend database for storing the CRUD operations data, and usage of Mailtrap for testing email services give insights on production level work. Working with Pydantic and Alembic helped me to paint a better picture of FastAPI application. Alembic made it easy to apply database version updates through migration strategy, and Pydantic enforced data validations for user inputs and respones. This helped in enforcing strict username/email and password validations and contributes to secure application.
  
  As for the end to end development, using comprehensive unit test to understand the edge cases which may not be caught by manual testing on UI, and the importance of writing clean and testable code. I myself found writing test cases as a difficult task for the code, but edge test cases would help to pinpoint how much efficent and robust the code is. Overall I find this assignment very interesting and gave me full exposure to the Python web api development.

## Grading Rubric

| Criteria                                                                                                                | Points |
|-------------------------------------------------------------------------------------------------------------------------|--------|
| Resolved 5 issues related to username validation, password validation, and profile field edge cases                      | 30     |
| Resolved the issue demonstrated in the instructor video                                                                 | 20     |
| Increased test coverage to 90% by writing comprehensive test cases                                                      | 20     |
| Followed collaborative development practices using Git and GitHub (branching, pull requests, code reviews)              | 15     |
| Submitted a well-organized GitHub repository with clear documentation, links to closed issues, and a reflective summary | 15     |
| **Total**                                                                                                               | **100**|

## Resources and Documentation

- **Instructor Videos and Important Links**:
 - [Introduction to REST API with Postgres](https://youtu.be/dgMCSND2FQw) - This video provides an overview of the REST API you'll be working with, including its structure, endpoints, and interaction with the PostgreSQL database.
 - [Assignment Instructions](https://youtu.be/TFblm7QrF6o) - Detailed instructions on your tasks, guiding you through the assignment step by step.
 - [Git Command Reference I created and some explanation for collaboration with git](git.md)
 - [Docker Commands and Running The Tests in the Application](docker.md)
 - Look at the code comments:
    - [Test Configuration and Fixtures](tests/conftest.py)
    - [API User Routes](app/routers/user_routes.py)
    - [API Oauth Routes - Connection to HTTP](app/routers/oauth.py)
    - [User Service - Business Logic - This implements whats called the service repository pattern](app/services/user_service.py)
    - [User Schema - Pydantic models](app/schemas/user_schemas.py)
    - [User Model - SQl Alchemy Model ](app/models/user_model.py)
    - [Alembic Migration - this is what runs to create the tables when you do alembic upgrade head](alembic/versions/628adcb2d60e_initial_migration.py)
    - See the tests folder for all the tests

 - API Documentation: `http://localhost/docs` - The Swagger UI documentation for the API, providing information on endpoints, request/response formats, and authentication.
 - Database Management: `http://localhost:5050` - The PGAdmin interface for managing the PostgreSQL database, allowing you to view and manipulate the database tables.

- **Code Documentation**:
 The project codebase includes docstrings and comments explaining various concepts and functionalities. Take the time to read through the code and understand how different components work together. Pay attention to the structure of the code, the naming conventions used, and the purpose of each function or class. Understanding the existing codebase will help you write code that is consistent and integrates well with the project.

- **Additional Resources**:
 - [SQLAlchemy Library](https://www.sqlalchemy.org/) - SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of tools for interacting with databases, including query building, database schema management, and data serialization. Familiarize yourself with SQLAlchemy's documentation to understand how it is used in the project for database operations.
 - [Pydantic Documentation](https://docs.pydantic.dev/latest/) - Pydantic is a data validation and settings management library for Python. It allows you to define data models with type annotations and provides automatic validation, serialization, and deserialization. Consult the Pydantic documentation to understand how it is used in the project for request/response validation and serialization.
 - [FastAPI Framework](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance) Python web framework for building APIs. It leverages Python's type hints and provides automatic API documentation, request/response validation, and easy integration with other libraries. Explore the FastAPI documentation to gain a deeper understanding of its features and how it is used in the project.
 - [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/index.html) - Alembic is a lightweight database migration tool for usage with SQLAlchemy. It allows you to define and manage database schema changes over time, ensuring that the database structure remains consistent across different environments. Refer to the Alembic documentation to learn how to create and apply database migrations in the project.

These resources will provide you with a solid foundation to understand the tools, technologies, and concepts used in the project. Don't hesitate to explore them further and consult the documentation whenever you encounter challenges or need clarification.

## Conclusion

This assignment is designed to challenge you, help you grow as a developer, and prepare you for the real-world responsibilities of a Software QA Analyst/Developer. By working on realistic issues, collaborating with your team, and focusing on testing and quality assurance, you will gain valuable experience that will serve you throughout your career.

Remember, the goal is not just to complete the assignment but to embrace the learning journey. Take the time to understand the codebase, ask questions, and explore new concepts. Engage with your team members, seek feedback, and learn from their experiences. Your dedication, curiosity, and willingness to learn will be the key to your success in this role.

We are excited to have you on board and look forward to seeing your contributions to the project. Your fresh perspective and skills will undoubtedly make a positive impact on our team and the quality of our software.

If you have any questions or need assistance, don't hesitate to reach out to your mentor or team lead. We are here to support you and ensure that you have a rewarding and enriching experience.

Once again, welcome to the Event Manager Company! Let's embark on this exciting journey together and create something remarkable.

Happy coding and happy learning!
