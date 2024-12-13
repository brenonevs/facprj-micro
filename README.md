# Melody Game

## Sobre o Projeto
O **Melody Game** é um jogo interativo baseado em áudio, inspirado em desafios musicais como os populares vídeos do TikTok. O objetivo principal é cantar a nota correta da melodia apresentada pelo jogo. Para isso, o jogo utiliza detecção de áudio para captar a frequência da voz do usuário, traduzi-la em uma nota musical e compará-la com a nota que deve ser cantada. 

O jogo possui:
- **Três níveis de dificuldade** que variam em:
  - O tempo necessário para sustentar a nota.
  - A tolerância na diferença entre a frequência da voz e a nota correta.
- **Interface no Arduino**, onde o usuário pode:
  - Selecionar a melodia para jogar.
  - Criar sua própria melodia personalizada.
  - Iniciar o jogo.
- **Sistema visual com uma bolinha em um tubo**, controlada por um ventilador que varia a rotação com base na frequência da voz do jogador. A altura da bolinha indica o quão próximo o jogador está da nota correta.

## Como Funciona
1. **Detecção de Áudio:**
   - O microfone capta a voz do jogador.
   - A frequência captada é processada e traduzida para uma nota musical.
   - A nota detectada é comparada com a nota esperada.

2. **Sistema de Pontuação:**
   - O jogador deve cantar a nota correta dentro do tempo estipulado e com a frequência adequada para avançar na melodia.

3. **Feedback Visual:**
   - Um ventilador controla a altura de uma bolinha em um tubo transparente.
   - Quanto mais próxima a frequência da voz do jogador estiver da nota correta, maior a rotação do ventilador e mais alta a bolinha sobe.

4. **Dificuldade:**
   - Fácil: Alta tolerância e menor tempo para sustentar a nota.
   - Médio: Média tolerância e tempo intermediário.
   - Difícil: Baixa tolerância e maior tempo para sustentar a nota.

## Como Reproduzir o Projeto

### Pré-requisitos
1. **Hardware:**
   - Arduino com suporte a tela.
   - Ventilador controlado por PWM.
   - Tubo transparente e bolinha leve (ex.: isopor).
   - Microfone compatível com Arduino.
2. **Software:**
   - IDE Arduino para programação.
   - Python para análise de áudio (opcional para simulações).

### Instalação
1. **Clone este repositório:**
   ```bash
   git clone https://github.com/seu-usuario/melody-game.git
   ```
2. **Carregue o código no Arduino:**
   - Abra a IDE do Arduino.
   - Carregue o arquivo `melody_game.ino` para a placa Arduino.
3. **Monte o circuito:**
   - Conecte o microfone ao Arduino.
   - Conecte o ventilador e o controle PWM.
   - Instale o tubo e a bolinha no ventilador.
   - Conecte a tela ao Arduino.

### Uso
1. **Inicie o jogo:**
   - Use os botões da interface no Arduino para selecionar uma melodia ou criar uma nova.
   - Pressione o botão para começar o jogo.
2. **Cante as notas:**
   - Siga as instruções na tela do Arduino.
   - Observe a bolinha no tubo para ajustar sua voz e alcançar a nota correta.
3. **Avance no jogo:**
   - Complete a melodia correta para ganhar pontos e avançar para as próximas fases.

## Personalização
1. **Criar Melodias Personalizadas:**
   - Use a interface para compor suas próprias sequências de notas.
   - Salve a melodia para jogar depois.

2. **Ajustar Configurações:**
   - Alterar a tolerância e o tempo de sustentação nas configurações.

## Veja o Jogo em Ação
Para entender melhor como o jogo funciona, assista a este vídeo demonstrativo: [Melody Game no YouTube](https://www.youtube.com/watch?v=u3d_ymTR4_k&t=54s)

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias no projeto.

## Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

Divirta-se jogando o Melody Game e aprimorando suas habilidades musicais! 🎶
