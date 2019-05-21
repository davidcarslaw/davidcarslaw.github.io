---
date: "2016-04-27T00:00:00Z"
external_link: ""
image:
  caption: openair logo
  focal_point: Smart
links:
- icon: twitter
  icon_pack: fab
  name: Follow
  url: https://twitter.com/davidcarslaw
slides: example
summary: openair R package.
tags:
- openair
- R
title: openair
url_code: ""
url_pdf: ""
url_slides: ""
url_video: ""
---

`openair` is a [<i class="fab fa-r-project"></i>](https://www.r-project.org) package that has been developed for the analysis of air pollution data. It provides many functions that are commonly useful for data analysis ([Carslaw and Ropkins, 2012]({{< ref "/publication/carslaw-2012-b/index.md" >}})). The main development site is available [here](https://github.com/davidcarslaw/openair) on GitHub. There is also detailed information available in a pdf manual --- you can {{% staticref "files/openairManual.pdf" %}}download the openair manual{{% /staticref %}}. 

**Increasingly, information on `openair` will be available through this website and a [bookdown](https://bookdown.org/home/) book will be written**.

Briefly, some of the main functions in `openair` include:

- Import data from air quality networks across the UK. See this [post]({{< ref "/post/2019-05-05-air-quality-data-available-in-openair.html" >}}) for more details.

- Flexibly plot data using a range of conditioning variables such as year, day of week, season --- or any numeric or categorical variable.

- Wind and pollution roses.

- Bivariate polar plots including conditional probability functions and two-pollutant statistics.

- Calendar plots.

- Functions for model evaluation such as Taylor plots and conditional quantiles together with common numeric statistics.

- Functions to plot and process Hysplit back trajectories.