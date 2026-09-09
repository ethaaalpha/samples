# Excel Agent
This project is about an AI Agent using Excel files to interact with coorporate data in a more easier way.

## Installation
To install the project you will need `uv` to be available in your path.  
Then just run `uv sync --locked`.

## Usage
To use the program: `uv run excel-agent`.  
The `--help` flag is available and detailed.

## Informations
The *WebUI* is experimental and more a Proof-Of-Concept than something else.  
Feel free to enhance the code.  

> [NOTE]
> The project was tested with an RTX 5090 running `nvidia/Gemma-4-26B-A4B-NVFP4` with vLLM.

> [TIP]
> We tried CPU only models but for the moment (Sept 2026), the results are not that good and we suggest to use an OpenAI standard API.

