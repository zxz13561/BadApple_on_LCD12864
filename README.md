# Bad Apple on LCD12864 module
MCU Board coding practice and coding language performance comparison


- ## TL; DR

| Board | Code Lang. | LCD Mode | FPS  | Scan Mode |
|:-----:|:----------:|:--------:|:----:|:-----:|
| STM32F103 | C/C++(HAL) | SPI | 10.3 | Progressive |
| ESP32 | Micropython | SPI | 3.x  | Progressive |
| Pi Pico W | Micropython | Parallel | 4.22 | Progressive |
| Pi Pico W | Micropython | Parallel | 8.13 | Interlaced |

- ## Basic Concept:
   - Send frame bytes from PC via UART, then MCU board show result
![BasicConcept.png](Document/Image/BasicConcept.png)
