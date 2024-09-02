# Web Crawler

This project implements a simple web crawler service with a server and client component. The server receives requests from a client to crawl a URL and sends the sitemap back to the client.

## Requirements

- Python 3.7+
- aiohttp
- beautifulsoup4

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/web-crawler.git
   cd web-crawler
   ```

2. Install the required packages:
   ```
   pip install aiohttp beautifulsoup4
   ```

## Running the Server

1. Start the server:
   ```
   python server.py
   ```
   The server will start running on `http://localhost:8080`.

## Running the Client

1. In a separate terminal, run the client:
   ```
   python client.py
   ```

2. When prompted, enter the URL you want to crawl (e.g., `https://redhat.com`).

3. The client will send a request to the server and print the resulting sitemap.

## Limitations and Future Improvements

1. The crawler is limited to one domain and does not follow external links.
2. Error handling could be improved for better resilience.
3. The crawler does not handle rate limiting or respect robots.txt files.
4. Parallel crawling could be implemented for improved performance on larger sites.
5. A more sophisticated sitemap format could be implemented (e.g., XML sitemap).

## Testing

To run the tests:

```
python -m unittest discover tests
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.