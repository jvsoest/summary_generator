docker volume create ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

python run.py $args[0]

docker stop ollama
docker rm ollama