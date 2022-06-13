#include <lmic.h>
#include <hal/hal.h>

/*************************************
 * TODO: Change the following keys
 * NwkSKey: network session key, AppSKey: application session key, and DevAddr: end-device address
 *************************************/
static const u1_t NWKSKEY[16] = {0x9A, 0x6C, 0xE3, 0xF7, 0xE6, 0xF9, 0xC1, 0xE1, 0x15, 0xDD, 0xB4, 0x3B, 0x5A, 0x89, 0xCC, 0x7C};
static const u1_t APPSKEY[16] = {0x1E, 0xA4, 0x83, 0xAD, 0x57, 0x37, 0xCF, 0xBD, 0xE7, 0xE0, 0x8C, 0x20, 0xC1, 0xDA, 0x6B, 0x89};
static const u4_t DEVADDR = 0x260CB760;

#define sensor1 A0
#define sensor2 A1
#define sensor3 A2
#define sensor4 A3

// These callbacks are only used in over-the-air activation, so they are
// left empty here (we cannot leave them out completely unless
// DISABLE_JOIN is set in config.h, otherwise the linker will complain).
void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }

static osjob_t sendjob;

// Schedule TX every this many seconds (might become longer due to duty
// cycle limitations).
const unsigned TX_INTERVAL = 5;

// Pin mapping
const lmic_pinmap lmic_pins = {
  .nss = 10,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 9,
  .dio = {2, 6, 7},
};

void onEvent (ev_t ev) {
  if (ev == EV_TXCOMPLETE) {
    Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
    // Schedule next transmission
    os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
  }
}

void do_send(osjob_t* j){
  // Payload to send (uplink)
  int sensorValue1 = analogRead(sensor1);
  int sensorValue2 = analogRead(sensor2);
  int sensorValue3 = analogRead(sensor3);
  int sensorValue4 = analogRead(sensor4);
  int sensorValues[] = {sensorValue1, sensorValue2, sensorValue3, sensorValue4};
  //int check = 0; //if(all value is zero) then check is 4

  for (byte i = 0; i < 4; i = i + 1) {
//    if (sensorValues[i] < 355) {
//      sensorValues[i] = 0;
//      check++;
//    }
    Serial.print(sensorValues[i]);
    Serial.print(" ");
  }
  Serial.println();
  
//  // send packet
//  if (check == 4) {
//    //counter++;
//    delay(5000);
//    return;
//  }

  String data = "";
  for (byte i = 0; i < 4; i = i + 1) {
    data += (String)sensorValues[i] + " ";
  }
  
  uint8_t message[data.length()+1];
  data.toCharArray(message, data.length()+1);
  //int value = analogRead(A0);
  //message[0] = highByte(value);
  //message[1] = lowByte(value);
 

  // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND) {
    Serial.println(F("OP_TXRXPEND, not sending"));
  } else {
    // Prepare upstream data transmission at the next possible time.
    LMIC_setTxData2(1, message, sizeof(message), 0);
    Serial.println(F("Sending uplink packet..."));
  }
  // Next TX is scheduled after TX_COMPLETE event.
  //delay(60000);//1min delay
}

void setup() {
  Serial.begin(115200);
  Serial.println(F("Starting..."));
  // LMIC init
  os_init();
  // Reset the MAC state. Session and pending data transfers will be discarded.
  LMIC_reset();

  // Set static session parameters.
  LMIC_setSession (0x1, DEVADDR, NWKSKEY, APPSKEY);

  // Disable link check validation
  LMIC_setLinkCheckMode(0);

  // TTN uses SF9 for its RX2 window.
  LMIC.dn2Dr = DR_SF9;

  // Set data rate and transmit power for uplink (note: txpow seems to be ignored by the library)
  LMIC_setDrTxpow(DR_SF7,14);

  // Start job
  do_send(&sendjob);
}

void loop() {
  os_runloop_once();  
}
