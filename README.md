# Bad Apple on LCD12864 module
MCU Board coding practice and coding language performance comparison


- ## TL; DR

|   Board   | Code Lang.  | LCD Mode | Baud-rate |  Scan Mode  | Avg. FPS |
|:---------:|:-----------:|:--------:|:---------:|:-----------:|:--------:|
| STM32F103 | C/C++(HAL)  |   SPI    |  230400   | Progressive |   10.3   |
| STM32H753 | C/C++(HAL)  |   SPI    |  460800   | Progressive |   13.5   |
|   ESP32   | Micropython |   SPI    |  230400   | Progressive |   3.4    |
| Pi Pico W | Micropython | Parallel |  230400   | Progressive |   4.22   |
| Pi Pico W | Micropython | Parallel |  230400   | Interlaced  |   8.13   |
   - Note: LCD pixels response time is not fast enough, it has terrible image sticking.
   - The best display FPS is around ~10 FPS

- ## Basic Concept:
   - Send frame bytes from PC via UART, then MCU board show result
![BasicConcept.png](Document/Image/BasicConcept.png)
