# Melody Game

## Sobre o Projeto
O **Melody Game** é um jogo interativo e divertido, inspirado nos desafios musicais que você talvez já tenha visto no TikTok. A ideia é simples: você precisa cantar a nota certa da melodia que o jogo apresenta. Mas como saber se está indo bem? O jogo detecta a frequência da sua voz, transforma isso em uma nota musical e compara com a nota que você deveria cantar.

Além disso, você recebe um feedback visual: uma bolinha em um tubo transparente. Quanto mais perto da nota certa, mais a bolinha sobe, graças a um ventilador que ajusta sua rotação de acordo com sua voz!

O jogo tem três níveis de dificuldade e permite que você crie suas próprias melodias para desafiar amigos ou se divertir ainda mais.

## Como Funciona
1. **Detecção de Áudio:**
   - O microfone escuta sua voz e identifica a frequência.
   - Essa frequência é traduzida para uma nota musical.
   - O jogo compara sua nota com a nota esperada e diz se você acertou ou não.

2. **Sistema de Pontuação:**
   - Para passar, você precisa sustentar a nota certa pelo tempo definido no nível escolhido.

3. **Feedback Visual:**
   - A bolinha no tubo sobe e desce com base na sua voz. Acerte a nota certa e veja a bolinha subir no tubo!

4. **Níveis de Dificuldade:**
   - Fácil: tolerância alta para pequenas variações e menor tempo.
   - Médio: tolerância intermediária e tempo médio.
   - Difícil: baixa tolerância e maior tempo necessário para segurar a nota.

## Como Reproduzir o Projeto

### O que Você Precisa
1. **Hardware:**
   - Arduino com tela.
   - Ventilador que possa ser controlado por PWM.
   - Tubo transparente e bolinha leve (tipo isopor).
   - Microfone.
2. **Software:**
   - IDE Arduino para programar a placa.
   - Python para analisar o áudio no computador.

### Montagem e Configuração
1. Clone este repositório no seu computador:
   ```bash
   git clone https://github.com/seu-usuario/melody-game.git
   ```
2. Abra a IDE do Arduino e carregue o arquivo `melody_game.ino` na placa.
3. Monte o circuito:
   - Ligue o ventilador com controle PWM.
   - Monte o tubo e posicione a bolinha dentro.
   - Conecte a tela para interação.

### Jogando
1. Na tela do Arduino, escolha entre:
   - Jogar uma melodia pronta.
   - Criar sua própria melodia para jogar depois.
2. Pressione o botão de iniciar e comece a cantar as notas que aparecem.
3. Use a bolinha no tubo como guia para ajustar sua voz e acertar a nota certa.
4. Complete todas as notas da melodia para avançar e ganhar pontos.

## Veja o Jogo em Ação
Ainda está em dúvida de como é o jogo? Dá uma olhada neste vídeo para entender melhor: [Melody Game no YouTube](https://www.youtube.com/watch?v=u3d_ymTR4_k&t=54s)

## Personalize seu Jogo
- **Crie suas próprias melodias:**
  Use a interface para gravar novas sequências de notas e desafiar amigos.
- **Ajuste as configurações:**
  Mude o tempo e a tolerância para deixar o jogo mais fácil ou mais difícil.
---

Aproveite o Melody Game e divirta-se enquanto melhora suas habilidades musicais! 🎶
