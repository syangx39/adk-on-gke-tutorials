# Ray ADK Tutorial

This project demonstrates the integration of Ray Serve with vLLM for efficient LLM serving and ADK (Agent Development Kit) for building intelligent agents. The project consists of two main components:

## Components

### 1. Ray Serve vLLM Service
Located in `ray_serve_vllm/`, this component provides a scalable LLM serving solution using Ray Serve and vLLM. It offers:
- FastAPI-based REST API endpoints
- OpenAI-compatible chat completion interface
- Streaming response support
- Health check endpoint
- Configurable model parameters and chat templates

### 2. ADK Agent
Located in `adk_agent/`, this component implements an intelligent agent using Google's Agent Development Kit. Features include:
- FastAPI-based web interface
- Session management with SQLite database
- CORS support
- Configurable web interface serving

## Prerequisites

- Python 3.8+
- Docker
- Kubernetes cluster (for deployment)
- Google Cloud Platform account (for ADK)

## Setup and Installation

### 1. Ray Serve vLLM Service

```bash
cd ray_serve_vllm
pip install -r requirements.txt
```

Key environment variables:
- `MODEL_ID`: The model to use (default: "meta-llama/Llama-3.1-8B-Instruct")
- `TENSOR_PARALLELISM`: Number of GPUs for tensor parallelism (default: 2)
- `MAX_MODEL_LEN`: Maximum model context length (default: 4096)
- `VLLM_ENABLE_AUTO_TOOL_CHOICE`: Enable automatic tool choice (default: true)
- `TOOL_PARSER_NAME`: Tool parser to use (default: llama3_json)
- `CHAT_TEMPLATE_PATH`: Path to custom chat template (optional)

### 2. ADK Agent

```bash
cd adk_agent
pip install -r requirements.txt
```

Key environment variables:
- `PORT`: Port to run the service on (default: 8080)

## Deployment

### Using Docker

Both components include Dockerfiles for containerization:

```bash
# Build and run Ray Serve vLLM
cd ray_serve_vllm
docker build -t ray-serve-vllm .
docker run -p 8000:8000 ray-serve-vllm

# Build and run ADK Agent
cd adk_agent
docker build -t adk-agent .
docker run -p 8080:8080 adk-agent
```

### Kubernetes Deployment

The `ray-service.yaml` file provides a Kubernetes deployment configuration for the Ray Serve vLLM service.

## API Endpoints

### Ray Serve vLLM Service
- `POST /v1/chat/completions`: OpenAI-compatible chat completion endpoint
- `GET /-/healthz`: Health check endpoint

### ADK Agent
- Web interface available at the configured port (default: 8080)
- Additional endpoints as configured in the agent implementation
