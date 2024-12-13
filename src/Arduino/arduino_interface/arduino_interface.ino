#include <Adafruit_GFX.h>
#include <JKSButton.h>
#include <TouchScreen.h>
#include <Adafruit_ILI9341.h>

JKSButton botao1, botao2, botao3, botao4, botao5, botao6, botao7, botao8, botao9, botao10;
int painel = 0;
int melodia = 1;
String nivel = "Medio";

Adafruit_ILI9341 tela = Adafruit_ILI9341(8, 10, 9);
TouchScreen touch(25, 26, 27, 9, 300);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  tela.begin();

  menuInicial();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (painel == 0) {
    botao1.process();
    botao2.process();
    botao3.process();
    botao4.process();
  }
  if (painel == 1) {
    botao8.process();
    botao9.process();
    botao10.process();
    botao4.process();
  }
  if (painel == 2) {
    botao4.process();
    botao5.process();
    botao6.process();
    botao7.process();
  }
}

void menuInicial() {
  painel = 0;
  tela.fillScreen(ILI9341_BLACK);

  botao1.init(&tela, &touch, 120, 45, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "Iniciar", 2);
  botao1.setPressHandler(msgIniciar);
  botao2.init(&tela, &touch, 120, 125, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "S. Dific.", 2);
  botao2.setPressHandler(escolherDificuldade);
  botao3.init(&tela, &touch, 120, 205, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "Melodia", 2);
  botao3.setPressHandler(escolherMelodia);
  botao4.init(&tela, &touch, 120, 285, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "C. Melod.", 2);
  botao4.setPressHandler(criarMelodia);
}

void escolherDificuldade() {
  painel = 1;
  tela.fillScreen(ILI9341_BLACK);

  botao8.init(&tela, &touch, 120, 45, 220, 70, ILI9341_WHITE, ILI9341_GREEN, ILI9341_WHITE, "Facil", 2);
  botao8.setPressHandler(msgFacil);
  botao9.init(&tela, &touch, 120, 125, 220, 70, ILI9341_WHITE, ILI9341_ORANGE, ILI9341_WHITE, "Medio", 2);
  botao9.setPressHandler(msgMedio);
  botao10.init(&tela, &touch, 120, 205, 220, 70, ILI9341_WHITE, ILI9341_RED, ILI9341_WHITE, "Dificil", 2);
  botao10.setPressHandler(msgDificil);
  botao4.init(&tela, &touch, 120, 285, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "Voltar", 2);
  botao4.setPressHandler(menuInicial);
}

void escolherMelodia() {
  painel = 2;
  tela.fillScreen(ILI9341_BLACK);

  botao5.init(&tela, &touch, 120, 45, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "1", 2);
  botao5.setPressHandler(msg1);
  botao6.init(&tela, &touch, 120, 125, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "2", 2);
  botao6.setPressHandler(msg2);
  botao7.init(&tela, &touch, 120, 205, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "3", 2);
  botao7.setPressHandler(msg3);
  botao4.init(&tela, &touch, 120, 285, 220, 70, ILI9341_WHITE, ILI9341_BLUE, ILI9341_WHITE, "Voltar", 2);
  botao4.setPressHandler(menuInicial);
}

void criarMelodia(JKSButton& botao) {
  Serial.println("CriarMelodia");
}

void msgIniciar(JKSButton& botao) {
  Serial.println("Iniciar " + nivel + " " + melodia);
}
void msgFacil(JKSButton& botao) {
  nivel = "Facil";
}
void msgMedio(JKSButton& botao) {
  nivel = "Medio";
}
void msgDificil(JKSButton& botao) {
  nivel = "Dificil";
}
void msg1(JKSButton& botao) {
  melodia = 1;
}
void msg2(JKSButton& botao) {
  melodia = 2;
}
void msg3(JKSButton& botao) {
  melodia = 3;
}