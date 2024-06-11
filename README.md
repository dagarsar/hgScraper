# Pokémon HeartGold Location Scraper

This repository contains a Python script to scrape the best locations of Pokémon in the HeartGold version of the Generation 4 Pokémon games. The script gathers data from Serebii.net and compiles it into a CSV file.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

To run this project, you need Python 3.x and some additional Python packages. You can install the required packages using pip:

```bash
pip install beautifulsoup4 pandas
```

## Usage

To use the script, simply run the `main.py` file. This script will scrape the necessary data and save it into a CSV file named `hgDex.csv`.

```bash
python main.py
```

## Project Structure

- `main.py`: The main script that performs the web scraping and data compilation.
- `hgDex.csv`: The output file containing the compiled Pokémon location data.

## Dependencies

- `urllib`: A module for fetching data across the web.
- `BeautifulSoup4`: A library for parsing HTML and XML documents.
- `pandas`: A data manipulation and analysis library.