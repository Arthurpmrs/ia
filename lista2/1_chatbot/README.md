# Chatbot de Loja de Roupas - Instruções de Uso

Este é um chatbot desenvolvido com o framework Rasa para uma loja de roupas conforme especificações solicitadas. O chatbot é capaz de processar pedidos de calças ou camisas, coletando informações específicas para cada tipo de produto.

## Estrutura do Projeto

O projeto contém os seguintes arquivos principais:

1. **domain.yml** - Define os intents, entities, slots, responses e actions do chatbot
2. **nlu.yml** - Contém os exemplos de treinamento para reconhecimento de linguagem natural
3. **stories.yml** - Define os fluxos de conversação possíveis
4. **rules.yml** - Estabelece regras específicas para o comportamento do chatbot
5. **actions.py** - Implementa ações personalizadas, como o processamento do pedido
6. **config.yml** - Configurações de pipeline e políticas do Rasa

## Funcionalidades

O chatbot implementa o fluxo solicitado:
- Verifica se o usuário deseja comprar calça ou camisa
- Para calças: pergunta o tamanho (34, 35 ou 36) e o tipo de fit (slim fit, regular fit, skinny fit)
- Para camisas: pergunta o tamanho (P, M ou G) e o tipo de gola (V, redonda ou polo)
- Ao final, informa as opções escolhidas com uma mensagem indicando que o pedido está sendo processado

## Passos para Execução

1. Instale o Rasa e suas dependências:
```
pip install rasa
```

2. Treine o modelo do chatbot na pasta do projeto:
```
rasa train
```

3. Execute o servidor de ações em um terminal:
```
rasa run actions
```

4. Em outro terminal, inicie o chatbot:
```
rasa shell
```

## Exemplo de Conversa

**Usuário**: Olá  
**Bot**: Olá! Bem-vindo à nossa loja de roupas. Como posso ajudar você hoje?  
**Bot**: O que você está procurando hoje? Uma camisa ou uma calça?  
**Usuário**: camisa  
**Bot**: Qual tamanho de camisa você deseja? Temos P, M e G.  
**Usuário**: M  
**Bot**: Qual tipo de gola você prefere? Temos gola V, redonda e polo.  
**Usuário**: gola v  
**Bot**: Seu pedido está sendo processado. Você escolheu: Camisa tamanho M, gola v. Obrigado pela sua compra!  
**Usuário**: Obrigado!  
**Bot**: Obrigado por visitar nossa loja. Até logo!