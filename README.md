<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

See project_tree.txt for the directory layout

<h3 align="center">Repair Shop DB</h3>

  <p align="center">
Documentation:
Utilizing Flask-Swagger and Flask-Swagger-UI Document Each Route of your API. Each Route Requires:

Path:
Endpoint
Type of request (post, get, put, delete)
tag (category for the route)
summary
description
security: Points to the security definition (Only need this for token authenticated routes)
parameters: Information about what the data the route requires(Only required for POST and PUT request)
responses: Information about what the data  route returns (Should include examples)
Definition(s):
PayloadDefinition: Defines the "Shape" of the incoming data (Only required for POST and PUT requests)
ResponseDefinitions: Defines the "Shape" of the outgoing data 
Testing:

Utilizing the built-in unittest library:
Create a tests folder inside you project folder
Create a test file for each of your blueprints (test_mechanics.py, test_customers.py, etc.) inside the tests folder
Create one test for every route in your API.
incorporate negative tests in your testing.
run your tests with: 

Windows: python -m unittest discover tests
Mac: : python -m unittest discover tests

Check out the API documentation by running the app:
```sh
  python a

Presenting
All students who joined Coding Temple February and onward need to present there project either on Thursdays or Friday live sessions, or you can schedule a 1-on-1 with Dylan to present.
For Pre-February students you are still encouraged to present as it is a great way to build you Tech-Communication skills which are a must.


    <br />
    <a href="https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck">View Demo</a>
    &middot;
    <a href="https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Python, MySQL workbench and server, Postman.
Implimented: SQLAlchemy, Flask, Marshmallow

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck.git
   ```
2. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin Slim-Beatnik/backend_module02_knowledgeCheck
   git remote -v # confirm the changes
   ```
3. Create a virtual environment
   ```sh
   python -m venv venv
   python3 -m venv venv
   ```
4. Install dependencies:
  pip: ```sh
    pip install -r requirements.txt
  ```
  OR
  uv: ```sh
        uv sync
      ```
5. run app on windows or mac
  pip:
   ```sh
   venv\\Scripts\\Activate
   source venv/bin/activate
  ```
  Windows:
  ```sh
   python app.py
   ```
  Mac:
  ```sh
   python3 app.py
  ```

OR

  uv:
  ```sh
   uv run app.py
```
  Postman setup:
  repair_shop_db.postman_collection.json must run in the db_test_environment.postman_environment.json
  - if you're out of free collection runs -
  Open a terminal and input the following command and navigate to the correct directory for the project.
  Then:
  ```sh
    postman collection run repair_shop_db.postman_collection.json -e db_test_environment.postman_environment.json
  ```

  then use uv run app.py

6. Verify paths in Postman:
  import repairshop_db.postman_collection.json
  You can then run all, or split up your run by folder.
  There is a main folder for creation:
  C___
  And another folder for read, update and delete:
  _RUD

8. 
  Open a browser and go to [/api/docs](http://127.0.0.1:5000/api/docs/)
  This will open the swagger doc and show api calls based on their tags:
  Customer, Inventory, Mechanics, ServiceTickets, Method Protection → Customer Token, and Method Protection → Mechanic Token

  *If visit this site before running the postman document, remember to create customers, inventory items, mechanics and service tickets before attempting to use any other methods.
  **Note - it won't break anything, IT WILL simply return 4xx response codes.

Notes:
  several deletes are soft-deletes with intent -
  The idea behind it also includes columns in the inventory, specifically the recalled and recallable. It's important to keep records of any recallable services to serve your customers properly, if not legally. Further, service tickets should probably be kept until the end of the current tax year.

  There are also web storefront routes, /inventory/shop allows front-end to get all products for showcase or shopping purposes. They are also available by ~shop/\<id\>, or searched by ~shop/search.

  Customers can look up their tickets via service_tickets/my-tickets
  Similarly, mechanics can look their assigned tickets via service_tickets/assigned-tickets/search

  Both Mechanics and Inventory objects can be associated with a service ticket with add and remove id_lists


Features and heartbreak:

1.  Creating a flushed out version of the app with testing has lead to some interesting issues.
The ServiceTicket class Model is now created without the constraint.
MySQL vs. sqlite, has a unique response while using sqlalchemy's CheckConstraint.
MySQL uses CHAR_LENGTH() while sqlite uses LENGTH()

  The work around was to add a conditional helper function within the models.py file, import it into the __init__.py file, where the create_app function lives.
  Once the app is created we can use app_context to extract the different versions of database handling using db.engine.dialect.name
  From there it plugs in the helper function and uses the conditional to append_constraint to the table allowing the appropriate function for the CheckConstraint function.

2. The assignment was set up in such a way that it makes me feel like I'm being shown what not to do as much as I am being shown how to do it properly.
  With the appropriate planning, I would have created routes, created tests, and the swagger documentation simultaneously.
  Instead the assignment build out every route before, for this knowledge check, simultaneously writing the documentation and testing, all while refactoring the weaker functions.
  This is a valuable lesson, but further, infuriating.
  
  I submit myself to more rigorous creation and planning going forward.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Slim-Beatnik/backend_module02_knowledgeCheck" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - totem64@gmail.com.com

Project Link: [https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck](https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Slim-Beatnik/backend_module02_knowledgeCheck.svg?style=for-the-badge
[contributors-url]: https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Slim-Beatnik/backend_module02_knowledgeCheck.svg?style=for-the-badge
[forks-url]: https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/network/members
[stars-shield]: https://img.shields.io/github/stars/Slim-Beatnik/backend_module02_knowledgeCheck.svg?style=for-the-badge
[stars-url]: https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/stargazers
[issues-shield]: https://img.shields.io/github/issues/Slim-Beatnik/backend_module02_knowledgeCheck.svg?style=for-the-badge
[issues-url]: https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/issues
[license-shield]: https://img.shields.io/github/license/Slim-Beatnik/backend_module02_knowledgeCheck.svg?style=for-the-badge
[license-url]: https://github.com/Slim-Beatnik/backend_module02_knowledgeCheck/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/3dkylehill
[product-screenshot]: images/screenshot.png
