#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "esp_adc/adc_continuous.h"

#define BULB_GPIO           8 // The GPIO triggers transistor to enable/disable bulb
#define TEMP_ADC            CONFIG_TEMP_ADC // ADC for sampling LM335 voltage
#define ADC_UNIT            ADC_UNIT_1
#define ADC_CONV_MODE       ADC_CONV_SINGLE_UNIT_1
#define ADC_ATTEN           ADC_ATTEN_DB_12
#define ADC_BIT_WIDTH       SOC_ADC_DIGI_MAX_BITWIDTH
#define READ_LEN            256

static uint8_t s_bulb_state = 0;
float temp;

void app_main(void)
{
    ESP_LOGI(TAG, "Mmmmm, bread!");
    gpio_reset_pin(BULB_GPIO);
    gpio_set_direction(BULB_GPIO, GPIO_MODE_OUTPUT);

    while (1) {
        // Measure temp
        temp = 
        // if > x degrees turn of light
        if{
            s_bulb_state = 0;
        }
        // if < x degrees turn on light
        {
            s_bulb_state = 1;
        }
        gpio_set_level(BULB_GPIO, s_bulb_state);

        // Sleep for 1000 milliseconds
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}
