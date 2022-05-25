[![TECOLOGYxyz - FlowerTracking](https://img.shields.io/static/v1?label=TECOLOGYxyz&message=FlowerTracking&color=blue&logo=github)](https://github.com/TECOLOGYxyz/FlowerTracking "Go to GitHub repo")


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/TECOLOGYxyz/FlowerTracking">
    <img src="tracking_logo.png" "https://github.com/TECOLOGYxyz/FlowerTracking" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Track Individual Flowers in Images</h3>

  <p align="center">
    Get flowering phenology for individual flowers using an automatic tracking algorithm..
    <br />
    <a href="https://github.com/TECOLOGYxyz/TrackingFlowers"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://share.streamlit.io/tecologyxyz/flowertracking/main/webapp.py">Try it out</a>
    ·
    <a href="https://github.com/TECOLOGYxyz/TrackingFlowers/issues">Report Bug</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This repository supports the paper *Towards individual-based pollination ecology: Automatic tracking of life histories of individual flowers*.

The paper present a tracking algorithm developed for fast and accurate tracking of individual flowers in time-lapse image series.

The algorithm includes a set of user-defined parameters for optimizing tracking performance:

The maximum number of frames a detection can be lost before new points are forced into a new track is set by **max gap**.
The number of frames for calculating the running mean of the position of an object is set by **running mean**. If there are less than this number of frames currently in the track, a mean over what is in the track will be used.
Simple centroid tracking algortihms will associate any two points between the current and the previus frame, disregarding the absolute distance between them, as long as they are the closest. In our algorithm, points that have a distance to tracked objects higher than **max_distance_threshold** will be forced into new tracks. If set to 0, this parameter will be ignored.

The tracking algorithm can be applied to any objects and can be used both offline (on detection output already produced) or online (in realtime, frame by frame, as detections are made).

The speed of the tracking algorithm depends on the computational power available and the number of object being tracked. The method is fast, however. Tracking of a series containing 85 objects ran at 0.02 seconds per frame.


<!-- GETTING STARTED -->
## Getting Started

To use the tracking algorithm and associated tools, follow the steps below.

1. Clone the repo
   ```sh
   git clone https://github.com/TECOLOGYxyz/TrackingFlowers.git
   ```
2. Install nessecary packages
   ```sh
   pip install -a requirements.txt
   ```
3. Run tracking on object detection output with 
   ```sh
   run.py
   ```





<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- CONTACT -->
## Contact

[@HjalteMann](https://twitter.com/@HjalteMann) - mann@ecos.au.dk - http://tecology.xyz/

[https://github.com/TECOLOGYxyz/TrackingFlowers](https://github.com/TECOLOGYxyz/TrackingFlowers)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TECOLOGYxyz/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/TECOLOGYxyz/TrackingFlowers/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TECOLOGYxyz/repo.svg?style=for-the-badge
[forks-url]: https://github.com/TECOLOGYxyz/TrackingFlowers/network/members
[stars-shield]: https://img.shields.io/github/stars/TECOLOGYxyz/repo.svg?style=for-the-badge
[stars-url]: https://github.com/TECOLOGYxyz/TrackingFlowers/stargazers
[issues-shield]: https://img.shields.io/github/issues/TECOLOGYxyz/repo.svg?style=for-the-badge
[issues-url]: https://github.com/TECOLOGYxyz/TrackingFlowers/issues
[license-shield]: https://img.shields.io/github/license/TECOLOGYxyz/repo.svg?style=for-the-badge
[license-url]: https://github.com/TECOLOGYxyz/TrackingFlowers/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/TECOLOGYxyz