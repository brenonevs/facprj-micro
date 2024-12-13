#include "Adafruit_VL53L0X.h"

#include <Adafruit_NeoPixel.h>

#include <Wire.h>
#include <PID_v1.h>

#define LED_PIN 8
#define LED_COUNT 12

//partida controle motor
int MOSFETPin = 5;

double setpoint = 0;  // hauteur cible de la balle (en mm)
double input, output;

double Kp = 0.9;
double Ki = 0.3;
double Kd = 0.0;

PID myPID(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);
// fim do trecho

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int alt_meta = 0;
int alt_bolinha = 0;

unsigned long instanteJogoComecou = 0;
unsigned long ultimoTempoAlteracao = 0;
bool jogoComecou = false;
int tempo_max = 0;
bool apagandoLEDs = false;
int cont_comecou_o_jogo = 0;

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

// Flags para controle de recebimento dos parâmetros
bool recebeuAlturaMeta = false;
bool recebeuTempoMax = false;

bool bolinhaNaMeta = false;
static unsigned long tempoInicioMeta = 0;

bool notaCerta = false;


int altura_bolinha(float dist) {
  int altura = (dist - 1.9) / 1.7;
  return altura + 0.3;
}

void altura(int alt_meta, int alt_bolinha) {
  for (int i = 0; i < LED_COUNT; i++) {
    if (i == alt_bolinha) {
      strip.setPixelColor(i, 50, 0, 0);  // Verde para o LED da bolinha
    } else if (i == alt_meta) {
      strip.setPixelColor(i, 0, 50, 0);  // Vermelho para o LED da meta
    } else {
      strip.setPixelColor(i, 10, 10, 10);  // Branco para os demais LEDs
    }
  }

  strip.show();
}



void tempo_acabando(int alt_meta, int alt_bolinha) {
  if (millis() - ultimoTempoAlteracao >= 100) {
    ultimoTempoAlteracao = millis();  // Atualiza o tempo

    // Alterna entre acender e apagar os LEDs
    if (apagandoLEDs) {
      // Apaga todos os LEDs
      for (int i = 0; i <= LED_COUNT; i++) {
        strip.setPixelColor(i, 0, 0, 0);
      }
      apagandoLEDs = false;  // Altera o estado para acender novamente
    } else {
      altura(alt_meta, alt_bolinha);  // Chama a função altura para reatualizar a fita
      apagandoLEDs = true;            // Altera o estado para apagar novamente
    }

    strip.show();  // Atualiza a fita de LEDs
  }
}

void setup() {
  Serial.begin(115200);
  strip.begin();
  strip.show();
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while (1)
      ;
  }
  // power
  //Serial.println(F("VL53L0X API Simple Ranging example\n\n"));

  pinMode(MOSFETPin, OUTPUT);
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(40, 200);  // Limites de l'output pour contrôler le moteur (0 à 255)
}


void loop() {
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false);
  int distancia = measure.RangeMilliMeter;

  float distance = distancia / 10.0;

  alt_bolinha = altura_bolinha(distance);

  // Affichage des valeurs
  input = measure.RangeMilliMeter;
  float medida_do_sensor = measure.RangeMilliMeter;
  input = input - 233;
  input = -input;
  double erreur = setpoint - input;
  myPID.Compute();
  // Serial.print("Input : ");
  // Serial.print(input);
  // Serial.print(" mm, Erreur : ");
  // Serial.println(erreur);
  // Serial.print(" mm, Medida do sensor : ");
  // Serial.println(medida_do_sensor);



  // ESPAÇO


  unsigned long instanteAgora = millis();

  if (jogoComecou) {
    cont_comecou_o_jogo++;

    if (notaCerta) {
      for (int i = 0; i < LED_COUNT; i++) {
        strip.setPixelColor(i, 0, 255, 0);
      }
      strip.show();

      unsigned long tempoInicioVerde = millis();
      while (millis() - tempoInicioVerde < 2000) {
      }

      for (int i = 0; i < LED_COUNT; i++) {
        strip.setPixelColor(i, 0, 0, 0);
      }
      strip.show();

      unsigned long pausa = millis();
      while (millis() - pausa < 5000) {
      }

      Serial.println("próxima nota");
      jogoComecou = false;
      bolinhaNaMeta = false;
      notaCerta = false;
    }

    altura(alt_meta, alt_bolinha);

    /*
    if (tempo_max <= (instanteAgora - instanteJogoComecou) / 1000) {
      // Acende todos os LEDs na cor vermelha
      for (int i = 0; i < LED_COUNT; i++) {
        strip.setPixelColor(i, 255, 0, 0);
      }
      strip.show();

      unsigned long tempoInicioVermelho = millis();
      while (millis() - tempoInicioVermelho < 1500) {
      }

      for (int i = 0; i < LED_COUNT; i++) {
        strip.setPixelColor(i, 0, 0, 0);
      }
      strip.show();

      unsigned long pausa = millis();
      while (millis() - pausa < 5000) {
      }

      jogoComecou = false;
      Serial.println("próxima nota");
    }
    */
  }

  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    //Serial.println(texto);

    if (texto.startsWith("conectei")) {
      Serial.println("próxima nota");
    }

    if (texto.startsWith("ganhou")) {
      notaCerta = true;
    }

    if (texto.startsWith("altura meta")) {
      alt_meta = (texto.substring(12)).toInt();
      alt_meta = 12 - alt_meta;
      //Serial.println(alt_meta);
      jogoComecou = true;
      instanteJogoComecou = millis();
      apagandoLEDs = false;
      Serial.println("Jogo começou!");
    }

    if (texto.startsWith("setpoint")) {
      setpoint = (texto.substring(8)).toDouble();
    }
  }

  // Contrôler le moteur avec la sortie PID
  analogWrite(MOSFETPin, output);
  // Serial.print("Nouveau setpoint : ");
  // Serial.println(setpoint);


  // Utiliser MOSFETPin pour contrôler le moteur
  // Serial.print("Comande (0-255) : ");
  // Serial.println(output);
}