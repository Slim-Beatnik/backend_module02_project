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
  <a href="https://github.com/Slim-Beatnik/backend_module02_project">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

See project_tree.txt for the directory layout

<h3 align="center">Repair Shop DB</h3>

  <p align="justify">
    Deployment and CI/CD Pipeline
    <br/>
    Follow along with the videos in Lesson 5 to:
    Host a database to Render
    Create your production config
    Install gunicorn psycopg2 python-dotenv (freeze to your requirements.txt and manually remove python-dotenv)
    Store sensitive information as an environmental variable in your .env file (database uri and secret key)
    add .env to your .gitignore
    Use the os package to retrieve those environmental variable
    Rename app.py to flask_app.py
    Pass your ProductionConfig into your create_app function inside flask_app.py
    Remove app.run() from flask_app.py
    Push to your github repository
    Deploy a Web Service on Render using the link to your github repository (make sure to add your environment variables during the deploy process).
    After successful deployment adjust your swagger documentation host from 127.0.0.1:5000 to the base url of your live API (base url should not include https://)
    Change your swagger schemes from http to https
    <br/>
    CI/CD Pipline:
    Create .github folder with a workflows folder inside
    Create a main.yaml file inside the workflows folder.
    In the main.yaml file create a workflow including:
    ---- name: name of workflow
    ---- on: trigger for workflow
    ---- jobs: Create the build and test jobs 
    Store the Render SERVICE_ID and RENDER_API_KEY as secrets in your github repository
    Set up the deploy job in your .github/workflows/main.yaml and make it dependant on the test job needs: test
    Submission:
    After deploying submit the link to your deployed service as well as the the link to your github repository.
    <br/>
    Presenting
    All students who joined Coding Temple February and onward need to present there project either on Thursdays or Friday live sessions, or you can schedule a 1-on-1 with Dylan to present.
    For Pre-February students you are still encouraged to present as it is a great way to build you Tech-Communication skills which are a must.
    <br />
    <a href="https://github.com/Slim-Beatnik/backend_module02_project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Slim-Beatnik/backend_module02_project">View Demo</a>
    &middot;
    <a href="https://github.com/Slim-Beatnik/backend_module02_project/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Slim-Beatnik/backend_module02_project/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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

1. 
  No need to get the repo, unless you're that sort of nerd.

  Open a browser and go to [/api/docs](https://backend-module02-project.onrender.com/api/docs) - link updated to live onrender site. The site gets sleepy, so it takes about 23 seconds to go live. From there you can do whatever.
  This will open the swagger doc and show api calls based on their tags:
  Customer, Inventory, Mechanics, ServiceTickets, Method Protection → Customer Token, and Method Protection → Mechanic Token

  Feel free to mess around

Notes:
  several deletes are soft-deletes with intent -
  The idea behind it also includes columns in the inventory, specifically the recalled and recallable. It's important to keep records of any recallable services to serve your customers properly, if not legally. Further, service tickets should probably be kept until the end of the current tax year.

  There are also web storefront routes, /inventory/shop allows front-end to get all products for showcase or shopping purposes. They are also available by ~shop/\<id\>, or searched by ~shop/search.

  Customers can look up their tickets via service_tickets/my-tickets
  Similarly, mechanics can look their assigned tickets via service_tickets/assigned-tickets/search

  Both Mechanics and Inventory objects can be associated with a service ticket with add and remove id_lists


<p align="right">(<a href="#readme-top">back to top</a>)</p>
Features:
  1. I was able to create the CI configuration with uv, and I added an additional setup action.yaml that is used to install uv that I can simply refere to in every action that requires it.





<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Slim-Beatnik/backend_module02_project/issues) for a full list of proposed features (and known issues).

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

<a href="https://github.com/Slim-Beatnik/backend_module02_project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Slim-Beatnik/backend_module02_project" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Kyle Hill - totem64@gmail.com

Project Link: [https://github.com/Slim-Beatnik/backend_module02_project](https://github.com/Slim-Beatnik/backend_module02_project)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Slim-Beatnik/backend_module02_project.svg?style=for-the-badge
[contributors-url]: https://github.com/Slim-Beatnik/backend_module02_project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Slim-Beatnik/backend_module02_project.svg?style=for-the-badge
[forks-url]: https://github.com/Slim-Beatnik/backend_module02_project/network/members
[stars-shield]: https://img.shields.io/github/stars/Slim-Beatnik/backend_module02_project.svg?style=for-the-badge
[stars-url]: https://github.com/Slim-Beatnik/backend_module02_project/stargazers
[issues-shield]: https://img.shields.io/github/issues/Slim-Beatnik/backend_module02_project.svg?style=for-the-badge
[issues-url]: https://github.com/Slim-Beatnik/backend_module02_project/issues
[license-shield]: https://img.shields.io/github/license/Slim-Beatnik/backend_module02_project.svg?style=for-the-badge
[license-url]: https://github.com/Slim-Beatnik/backend_module02_project/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/3dkylehill
[product-screenshot]: images/screenshot.png
