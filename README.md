# VideoToAudio

Este projeto converte vídeos em arquivos de áudio, transcreve o áudio para texto utilizando o modelo Whisper da OpenAI, e salva a transcrição em um arquivo de texto.

## Funcionalidades
- Conversão automática de vídeo para áudio (usando ffmpeg)
- Transcrição do áudio para texto com barra de progresso (usando Whisper)
- Suporte a múltiplos vídeos na pasta `input/`
- Suporte ao idioma português

## Observações
- O modelo Whisper 'large' é utilizado por padrão para melhor qualidade de transcrição.
- O idioma padrão da transcrição é o português.
- Certifique-se de que o áudio dos vídeos esteja claro para melhores resultados.
