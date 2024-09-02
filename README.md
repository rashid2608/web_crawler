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

2. Create and activate a virtual environment:
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
│
├── src/
│   ├── server.py
│   ├── client.py
│   └── requirements.txt
│
├── tests/
│   └── test_crawler.py
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── hpa.yaml
│
├── Dockerfile
└── README.md
```

- `server.py`: Contains the server-side logic, including the Crawler class and request handling.
- `client.py`: Implements the client-side logic for sending crawl requests and displaying results.
- `requirements.txt`: Lists all Python dependencies for the project.
- `tests/test_crawler.py`: Contains unit tests for the crawler functionality.


#Deploying with Minikube

Start Minikube:
Copyminikube start

Enable the ingress addon (optional):
Copyminikube addons enable ingress

Set your terminal to use Minikube's Docker daemon:
Copyeval $(minikube docker-env)  # For Unix-based systems
# OR
minikube docker-env | Invoke-Expression  # For Windows PowerShell

Build your Docker image:
Copydocker build -t web-crawler:latest .

Apply the Kubernetes configurations:
Copykubectl apply -f k8s/

Verify the deployment:
Copykubectl get deployments
kubectl get pods
kubectl get services

Access the service:
Copyminikube service web-crawler

(Optional) For debugging, use the Minikube dashboard:
Copyminikube dashboard


Troubleshooting
HorizontalPodAutoscaler Issues
If you encounter an error related to the HorizontalPodAutoscaler when applying the Kubernetes configurations, try the following:

Check your Kubernetes version:
Copykubectl version --short

Update the k8s/hpa.yaml file to use a compatible API version:

For Kubernetes 1.23+: Use apiVersion: autoscaling/v2
For Kubernetes 1.18-1.22: Use apiVersion: autoscaling/v2beta2
For older versions: Use apiVersion: autoscaling/v1


Ensure the metrics server is enabled in Minikube:
Copyminikube addons enable metrics-server

If issues persist, you can temporarily skip applying the HPA:
Copykubectl apply -f k8s/configmap.yaml -f k8s/deployment.yaml -f k8s/service.yaml


Other Common Issues

If pods are not starting, check their status and logs:
Copykubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>

Ensure your Dockerfile is correctly set up and the application runs properly as a container.
Verify that your service is correctly configured to expose the application.

Stopping and Cleaning Up
When you're done testing:

Delete the Kubernetes resources:
Copykubectl delete -f k8s/

Stop Minikube:
Copyminikube stop

To completely remove the Minikube cluster:
Copyminikube delete


Running Tests
To run the unit tests:
Copypython -m unittest discover tests
For verbose output:
Copypython -m unittest discover tests -v


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
