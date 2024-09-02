# Web Crawler

This project implements a simple web crawler service with a server and client component. The server receives requests from a client to crawl a URL and sends the sitemap back to the client. The crawler is limited to one domain and builds a sitemap showing the links between pages.

## Features

- Asynchronous crawling for improved performance
- Domain-limited crawling (doesn't follow external links)
- Sitemap generation in a tree-like structure
- Error handling and retry mechanism
- Unit tests for core functionality

## Requirements

- Python 3.7+
- aiohttp
- beautifulsoup4

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/rashid2608/web-crawler.git
   cd web-crawler
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```
   python server.py
   ```
   The server will start running on `http://localhost:8080`.

2. In a separate terminal, run the client:
   ```
   python client.py
   ```

3. When prompted, enter the URL you want to crawl (e.g., `https://example.com`).

4. The client will send a request to the server and print the resulting sitemap in a tree-like structure.

## Running Tests

To run the unit tests:

1. Ensure you're in the project root directory.
2. Activate your virtual environment if you're using one.
3. Run the following command:
   ```
   python -m unittest discover tests
   ```

This command will automatically discover and run all test files in the `tests` directory.

For more detailed test output, use the verbose flag:
```
python -m unittest discover tests -v
```

## Project Structure

```
web_crawler/
├── server.py
├── client.py
├── requirements.txt
├── README.md
└── tests/
    └── test_crawler.py
```

- `server.py`: Contains the server-side logic, including the Crawler class and request handling.
- `client.py`: Implements the client-side logic for sending crawl requests and displaying results.
- `requirements.txt`: Lists all Python dependencies for the project.
- `tests/test_crawler.py`: Contains unit tests for the crawler functionality.

## Design Decisions and Trade-offs

1. Asynchronous Programming: We used Python's asyncio and aiohttp for asynchronous crawling, allowing for concurrent requests and improved performance.

2. Domain Limitation: The crawler is restricted to a single domain to prevent unintended crawling of external sites.

3. Error Handling: Basic error handling and a retry mechanism are implemented to improve resilience.

4. In-Memory Storage: The sitemap is stored in memory, which is fast but could be a limitation for extremely large sites.

5. Simple Tree-like Output: The sitemap is presented in a simple tree-like text format for easy readability.

## Limitations and Potential Improvements

1. The crawler doesn't respect robots.txt files.
2. There's no limit on crawling depth, which could be an issue for large sites.
3. The crawler doesn't handle JavaScript-rendered content.
4. No persistent storage of crawl results.
5. The client-server communication could be improved for real-time updates.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.