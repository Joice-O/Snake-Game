# Snake Game

Jogo da cobrinha desenvolvido em Python com Pygame. O objetivo é coletar maçãs, aumentar a pontuação e evitar colisões com as bordas ou com o próprio corpo.

## Funcionalidades

- Movimentação pelas setas do teclado.
- Crescimento da cobra e acréscimo de um ponto por maçã.
- Pausa e retomada da partida.
- Tela de fim de jogo com pontuação e opção de reiniciar.

## Tecnologias

Python 3, Pygame e o módulo `random` da biblioteca padrão.

## Como executar

É necessário ter Python 3 instalado e um ambiente com interface gráfica.

```bash
git clone https://github.com/Joice-O/Snake-Game.git
cd Snake-Game
python -m venv .venv
```

Ative o ambiente virtual:

- Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
- Linux/macOS: `source .venv/bin/activate`

Instale a dependência e inicie o jogo:

```bash
python -m pip install pygame
python snakegame.py
```

Se o comando Python do seu sistema for `python3`, utilize-o no lugar de `python`. Não são necessários banco de dados ou arquivos de imagem externos.

## Controles

| Tecla | Ação |
| --- | --- |
| Setas | Mover a cobra |
| P | Pausar ou retomar |
| R | Reiniciar na tela de fim de jogo |
| Q | Sair durante a pausa ou na tela de fim de jogo |

Também é possível sair fechando a janela.

## Organização

- `snakegame.py`: lógica, interface, controles, pontuação e colisões.
- `README.md`: apresentação e instruções de execução.

## Autoria

Projeto disponível no perfil de [Joice Oliveira Jardim](https://github.com/Joice-O). O histórico de commits registra as contribuições ao código.

## Limitações atuais

A pontuação é mantida apenas durante a execução; não há ranking persistente. O projeto não possui suíte de testes automatizados.

