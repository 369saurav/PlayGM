# PLAY-GM


**PLAY-GM** is an innovative chess application that allows users to play against top grandmasters by mimicking their unique strategies and playing styles. Whether you're a casual chess enthusiast or a serious player looking to challenge yourself, PLAY-GM offers an immersive and educational chess experience.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Data Collection and Processing](#data-collection-and-processing)
- [Future Plans](#future-plans)
- [Challenges](#challenges)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Play with Legends**: Choose from a roster of top grandmasters and experience their unique playing styles.
- **Realistic Move Suggestions**: Advanced algorithms analyze thousands of grandmaster games to suggest moves that reflect their strategies.
- **Interactive Gameplay**: A user-friendly interface that makes it easy to follow games and learn from grandmaster strategies.
- **Data-Driven Insights**: Utilizes extensive data from chess games to accurately replicate grandmaster moves.

## Technologies Used

- ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white) **Python**: Core language used for backend development and data processing.
- ![Docker](https://img.shields.io/badge/Docker-Containerization-blue?logo=docker&logoColor=white) **Docker**: Containerization of the application for easy deployment and scalability.
- ![TiDB](https://img.shields.io/badge/TiDB-Serverless%20Database-orange?logo=tidb&logoColor=white) **TiDB**: Serverless database for efficient storage and retrieval of vectorized chess data.
- ![React](https://img.shields.io/badge/React-Frontend-blue?logo=react&logoColor=white) **React**: Frontend framework for building the interactive user interface.
- ![GCP](https://img.shields.io/badge/GCP-Cloud%20Platform-green?logo=google-cloud&logoColor=white) **Google Cloud Platform (GCP)**: Hosting and cloud services for scalability and performance.

## Getting Started

To get started with PLAY-GM, you will need to clone the repository and install the necessary dependencies.

### Prerequisites

- Python 3.8 or higher
- Git
- Docker
- Access to a terminal or command prompt
- Basic knowledge of chess and Python programming

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/369saurav/PlayGM.git
    cd PLAY-GM
    git checkout master
    ```

2. **Install the dependencies**:

    It's recommended to use a virtual environment. You can create one using `venv` or `conda`.

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:

    ```bash
    docker-compose up
    ```

## Usage

- **Selecting a Grandmaster**: Choose a grandmaster to play against from the list provided in the app.
- **Making Moves**: Use the interactive chessboard to make your moves. The app will provide feedback based on the grandmaster’s style.
- **Learning from Strategies**: As you play, observe the move suggestions and learn the strategic nuances of top grandmasters.

## Data Collection and Processing

PLAY-GM collects extensive data from chess websites like chess365.com. The games are downloaded in PGN format and converted into FEN notation to capture the exact board state. This data is then vectorized and stored in a TiDB serverless database, allowing for quick retrieval and analysis during gameplay.

### Data Flow

1. **Data Scraping**: Extracting game data from online sources.
2. **Data Conversion**: Converting PGN files to FEN notation for precise board representation.
3. **Vectorization**: Transforming the data into numerical vectors representing grandmaster strategies.
4. **Storage**: Storing the vectorized data in a TiDB serverless database for efficient access.

## Future Plans

- **Additional Grandmasters**: Expanding the roster of grandmasters available in the app.
- **Game Analysis**: Introducing detailed game analysis features to provide insights into strategies and move effectiveness.
- **Advanced AI**: Developing an AI that combines strategies from multiple grandmasters to compete against top chess engines like AlphaZero.

## Challenges

Developing PLAY-GM involved overcoming various challenges, such as integrating diverse data formats, ensuring accurate replication of grandmaster strategies, and creating a seamless user experience. These challenges were met with innovative solutions and robust application design.

## Contributing

We welcome contributions to improve PLAY-GM. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear messages.
4. Push to your branch and create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **TiDB**: For providing the serverless database solution.
- **chess365.com**: For the extensive chess game data.
- **Community**: Thanks to all the contributors and users for their feedback and support.

---

Thank you for checking out PLAY-GM! We hope you enjoy challenging yourself against the strategies of top grandmasters.
