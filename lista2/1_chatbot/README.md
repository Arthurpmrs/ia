# Chatbot de Loja de Roupas

## Passos para Execução

1. Instalar dependência
```
# Ativar ambiente virtual (python 3.10 ou 3.11)
pip install rasa
```

2. Treinar o modelo com base nas regras
```
rasa train
```

3. Executar servidor de ações
```
rasa run actions
```

4. Em outro terminal, iniciar o chatbot
```
rasa shell
```