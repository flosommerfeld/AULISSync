<div id="top"></div>
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



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/flosommerfeld/IliasSync">
    <img src="img/logo_inkscape.svg" alt="Logo" height="100">
  </a>

<h3 align="center">AULISSync</h3>

  <p align="center">
    AULISSync synchronizes your ILIAS courses to the local hard drive. 
    <br />
    <a href="https://github.com/flosommerfeld/IliasSync"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/flosommerfeld/IliasSync">View Demo</a>
    ·
    <a href="https://github.com/flosommerfeld/IliasSync/issues">Report Bug</a>
    ·
    <a href="https://github.com/flosommerfeld/IliasSync/issues">Request Feature</a>
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
AULISSync was initially created due to my personal preference of having all the univserity course
files locally. It was pretty annoying to always visit the AULIS website, type in the credentials everytime, look for the course, download new course files weekly and then not having these files across all my other devices. AULISSync helps to synchronize all of the files which are distributed by your professor via AULIS. 

It is easily integrateable with other synchronization services, such as [MEGA](https://mega.nz/sync), [Google Drive](https://www.google.com/intl/de/drive/download/), [Dropbox](https://www.dropbox.com/de/), [Microsoft OneDrive](https://onedrive.live.com/about/): just make AULISSync synchronize your courses into a directory which is being synchronized by one of these services.

[![Product Name Screen Shot][product-screenshot]](https://example.com)


<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org)
* [pywebview](https://pywebview.flowrl.com/)
* [ReactJS](https://reactjs.org/)
* [Selenium](https://www.selenium.dev/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an list of things you need to use the software.
* [Python 3](https://www.python.org/downloads/)
* [pip](https://packaging.python.org/tutorials/installing-packages/#install-pip-setuptools-and-wheel) if it is not installed via Python 3 already
* [pipenv](https://pypi.org/project/pipenv/)
    ```
    pip install --user pipenv
    ```
* [npm & Node.js](https://nodejs.org/en/download/)



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/flosommerfeld/IliasSync.git
   ```
2. Install Python packages
   ```sh
   pipenv install
   ```
3. Install npm packages
    ```
    npm install
    ```
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Start the Selenium Standalone Server
   ```sh
   npm start
   ```
2. Bundle & compile JavaScript modules with Webpack
   ```sh
   npm run bundle
   ```
3. Run the Python GUI application
   ```sh
   pipenv run python src/__main__.py
   ```
   or
    ```sh
   python src/__main__.py
   ```

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] GUI for authentication
- [ ] Configuration of download paths
- [x] Save user credentials locally
- [ ] Ask the user what to sync before starting the sync process
- [ ] Display download information
- [x] Modernize GUI


See the [open issues](https://github.com/flosommerfeld/IliasSync/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



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

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Florian Sommerfeld - [@flosommerfeld](https://twitter.com/twitter_handle) - help.flosommerfeld@gmail.com

Project Link: [https://github.com/flosommerfeld/IliasSync](https://github.com/flosommerfeld/IliasSync)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/flosommerfeld/IliasSync.svg?style=for-the-badge
[contributors-url]: https://github.com/flosommerfeld/IliasSync/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/flosommerfeld/IliasSync.svg?style=for-the-badge
[forks-url]: https://github.com/flosommerfeld/IliasSync/network/members
[stars-shield]: https://img.shields.io/github/stars/flosommerfeld/IliasSync.svg?style=for-the-badge
[stars-url]: https://github.com/flosommerfeld/IliasSync/stargazers
[issues-shield]: https://img.shields.io/github/issues/flosommerfeld/IliasSync.svg?style=for-the-badge
[issues-url]: https://github.com/flosommerfeld/IliasSync/issues
[license-shield]: https://img.shields.io/github/license/flosommerfeld/IliasSync.svg?style=for-the-badge
[license-url]: https://github.com/flosommerfeld/IliasSync/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
